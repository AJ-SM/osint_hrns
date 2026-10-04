from googlesearch import search
import requests
from ddgs import DDGS 
import time 
from bs4 import BeautifulSoup
from urllib.error import HTTPError

class Search:
    def __init__(self, query: str,n_results:int,lang="en", engine:any=None):
        self.engine = engine
        self.query = query
        self.n_results = n_results
        self.lang = lang
        self.res = []

    def google(self):
        try:
            print(search.__module__)
            results = search(
                self.query,
                num=self.n_results,
                lang=self.lang,
                user_agent="Mozilla/5.0")
            
            for result in results:
                print(result)
                # time.sleep(4)
        except HTTPError  as e :
            print("Error Occured ") 
            print('Code', e.code)
            print('Reason ', e.reason)
    
    def ddg(self):
        with DDGS() as ddgs:
            results = list(ddgs.text(self.query, max_results=self.n_results))
            self.res = results
            for r in results:    
                print(r['title'], r['href'])
            
    
    def parser(self,res):
        soup = BeautifulSoup(res, 'html.parser') 
        print(soup)
        for result in soup.select("div.MjjYud"):
            print(result.get_text(" ", strip=True))
        
    
    def google_ran(self):
        url = "https://www.google.com/search"

        params = {
            "q": self.query,
            "hl": self.lang,
            "num": self.n_results
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(
            url,
            params=params,
            headers=headers
        )
        return r.text
        # print(r.text)

pry="INDIA"


if __name__=="__main__":

    print("Running in debug mode \n")
    gggl = Search(pry,1)
    res = gggl.google_ran()
    gggl.parser(res=res)
    # sg = Search(pry,1)
    # print(sg.ddg())