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
        self.kw = self.data["research_tasks"][0]["keyword"]
        print("Seraching For Keywords : ", self.kw)
        self.hints = self.data["research_tasks"][0]["retrieval_hints"]
        print("Query Limitation Setup : ",self.hints)
   
        

        for i in self.kw:
            print("Seraching For Keywords : ",i)
            engine = self.search(i,5)
            res = engine.ddg()
            for lk in res:
                
                self.href.append(lk['href'])
        return self.href,self.hints


class fetch:
    def __init__(self,links:list,strip:callable=strip):
        self.link = links
        self.results = []
        self.strip = strip
        
    
    def information(self):
        for planLink in self.link:
            self.results.append(str(self.strip(link=planLink)))
        return self.results
        



