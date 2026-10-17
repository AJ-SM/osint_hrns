import requests
from bs4 import BeautifulSoup
from bs4.exceptions import ParserRejectedMarkup


def strip(link):
    try:
        res = requests.get(
            link,
            timeout=10,
            headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
        )

        res.raise_for_status()

        # Check what the server actually returned
        content_type = res.headers.get("Content-Type", "").lower()

        if "text/html" not in content_type:
            print(f" \033[91m[SKIP] Non-HTML content:\033[0m {content_type}")
            return None

        try:
            soup = BeautifulSoup(res.content, "html.parser")

        except ParserRejectedMarkup:
            print(f" \033[91m[TIMEOUT]\033[0m  BeautifulSoup rejected markup: {link}")
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

        print(f"\033[92m[Success]\033[0m", link)
        return soup.get_text(
            separator=" ",
            strip=True
        )
    except requests.exceptions.Timeout as e:
        print(f" \033[91m[TIMEOUT]\033[0m  {link}: {e}")

    except requests.exceptions.RequestException as e:
        
        print(f" \033[91m[REQUEST ERROR]\033[0m  {link}: {e}")

    except Exception as e:
        print(f" \033[91m[UNKNOWN ERROR] \033[0m  {link}: {e}")
       

    return None
