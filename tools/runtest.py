from scripts.Engine_search import Search
from scripts.planner import Planner
from scripts.evidence.fetcher import collect
from scripts.stripper import strip
from scripts.evidence.fetcher import fetch

ip_query = input("Enter your target word : ")
collectr = collect(search=Search,planner=Planner,query=ip_query)
res = collectr.searcher()
ftch = fetch(strip=strip,links=res)
results = ftch.information()
print(results)
