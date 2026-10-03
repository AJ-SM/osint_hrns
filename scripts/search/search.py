from googlesearch import search
from ddgs import DDGS 
import time 
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


pry = "INDIA"



if __name__=="__main__":
    res = search(
                pry,
                num=1,
                lang="en",
                user_agent="Mozilla/5.0")
    for i in res:

        print(i)
    print("Running in debug mode \n")
    # sg = Search(pry,1)
    # print(sg.google())