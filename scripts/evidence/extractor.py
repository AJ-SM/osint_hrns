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



class Evidence:
    def __init__(self,querry):
        self.evidence=evidenceData
        self.collection = Collected
        self.ftch = fetch
        self.clt=collect
        self.strip=strip
        self.querry = querry
        self.serach = Search
        self.planner=Planner
    
    def ranState(self):        
        collectr = collect(search=Search,planner=Planner,query=self.querry)
        res,hits = collectr.searcher()
        ftch = fetch(strip=strip,links=res)
        results = ftch.information()
        print("Only Seraching Forr : ", hits[0])
        clt = Collected(doc=results,query=hits[0])
        k= clt.find()
        print(" FOUndd best matched Results ..... ")
        print(k.argsort())




