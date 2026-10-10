import requests
from bs4 import BeautifulSoup

def strip(link):
    test_url =link
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    res = requests.get(test_url, headers=headers)

    # print(res.status_code)
    # print(res.url)
    # print(res.text)

    soup = BeautifulSoup(res.text, "html.parser")
    article = soup.select_one("section.main")

  

    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(" ", strip=True)
    return text 


