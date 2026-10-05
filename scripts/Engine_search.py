from googlesearch import search
import requests
from ddgs import DDGS
import warnings 
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
        warnings.warn(" You will get the error page don't use its redundent ")
        return 
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
        pass 
    def ddg(self):
        with DDGS() as ddgs:
            results = list(ddgs.text(self.query, max_results=self.n_results))
            self.res = results
            # for r in results:    
            #     print(r['title'], r['href'])
            return self.res
            
    
    def parse(self,res):
        self.soup = BeautifulSoup(res, "html.parser")
        print(self.soup)
        results = []

        for result in self.soup.select("div.MjjYud"):
           
            title_tag = result.select_one("h3")

            if not title_tag:
                continue

            title = title_tag.get_text(" ", strip=True)

            link_tag = title_tag.find_parent("a")

            if not link_tag:
                continue

            url = link_tag.get("href")

            description_tag = result.select_one(
                "div.VwiC3b"
            )

            description = (
                description_tag.get_text(" ", strip=True)
                if description_tag
                else ""
            )
            print(description)

            results.append({
                "title": title,
                "url": url,
                "description": description
            })
        pass 
        return results
        
    
    def google_ran(self):
        warnings.warn(" You will get the error page don't use its redundent ")
       
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
    # print(res)
    parsed = gggl.parse(res=res)
    print(parsed)
    # sg = Search(pry,1)
    # print(sg.ddg())