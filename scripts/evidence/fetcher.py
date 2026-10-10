from scripts.Engine_search import Search
from scripts.planner import Planner
from scripts.stripper import strip

## Get the seraching urls 

test_url = "https://www.scaler.com/topics/artificial-intelligence-boon-or-bane/"
class collect:
    def __init__(self,search,planner,query):
        self.query= query
        self.search=search
        self.planner=planner()
        self.href=[]

    def searcher(self):
        self.data = self.planner.paln(query=str(self.query))
        print("AI Response ------")
        print(self.data)
        self.kw = self.data["research_tasks"][0]["keyword"]

        for i in self.kw:
            engine = self.search(self.query,5)
            res = engine.ddg()
            for lk in res:
                # print(f"Search Results :{i} =  ", lk['href'])
                self.href.append(lk['href'])
        return self.href


class fetch:
    def __init__(self,links:list,strip:callable=strip):
        self.link = links
        self.results = ""
        self.strip = strip
        
    
    def information(self):
        for planLink in self.link:
      
            self.results += self.strip(link=planLink)
            self.results+='\n'
        return self.results
        



