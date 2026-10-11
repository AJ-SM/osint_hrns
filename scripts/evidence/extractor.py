from scripts.Engine_search import Search
from scripts.planner import Planner
from scripts.evidence.fetcher import collect
from scripts.stripper import strip
from scripts.evidence.fetcher import fetch
from scripts.evidence.collector import Collected
from dataclasses import dataclass


@dataclass
class evidenceData:
    task_id: str
    toVerify:str
    url:str
    title:str
    passage:str
    score:str

# Response Format 

''' 

'''

class Evidence:
    def __init__(self,querry):
        # self.evidence=evidenceData
        self.collection = Collected
        self.ftch = fetch
        self.clt=collect
        self.strip=strip
        self.querry = querry
        self.serach = Search
        self.planner=Planner
        self.resScore=[]
        self.resSearch=[]
    
    def ranState(self):        
        collectr = collect(search=Search,planner=Planner,query=self.querry)
        res,hits,tasks = collectr.searcher()
        ftch = fetch(strip=strip,links=res)
        results = ftch.information()
        self.resSearch=results
        # We are only taking the hits @ 0 inddex 

        print("Only Seraching Forr : ", hits[0])
        # We are only taking the task 1 we have to parse through it 
        clt = Collected(doc=results,query=hits[0])
        k = clt.find()
        self.resScore= k
        
        tasks = tasks[0],
        # This should goo in LOOP 
        evad1 = evidenceData(
            task_id=tasks[0]["id"],
            toVerify=tasks[0]["claim_to_verify"],
            url=res[k.argsort()[-1]],
            title=tasks[0]["objective"],
            passage=results[k.argsort()[-1]],
            score=float(k[k.argsort()[-1]])
        )

        print(evad1)
        return evad1




        # print(" FOUndd best matched Results ..... ")
        # print( " Seraches args : " , k)
        # print( " Seraches args : " , results)
        




