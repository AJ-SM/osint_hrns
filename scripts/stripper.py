import requests
from bs4 import BeautifulSoup
from bs4.exceptions import ParserRejectedMarkup


def strip(link):
    try:
        res = requests.get(
            link,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        res.raise_for_status()

        # Check what the server actually returned
        content_type = res.headers.get("Content-Type", "").lower()

        if "text/html" not in content_type:
            print(f"[SKIP] Non-HTML content: {content_type}")
            return None

        try:
            soup = BeautifulSoup(res.content, "html.parser")

        except ParserRejectedMarkup:
            print(f"[SKIP] BeautifulSoup rejected markup: {link}")
            return None

        # Remove obvious junk
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript"
        ]):
            tag.decompose()

        return soup.get_text(
            separator=" ",
            strip=True
        )

    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] {link}")

    except requests.exceptions.RequestException as e:
        print(f"[REQUEST ERROR] {link}: {e}")

    except Exception as e:
        print(f"[UNKNOWN ERROR] {link}: {e}")

    return None