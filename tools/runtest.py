from scripts.Engine_search import Search
from scripts.planner import Planner
from scripts.evidence.fetcher import collect



ip_query = input("Enter your target word : ")
collectr = collect(search=Search,planner=Planner,query=ip_query)
print(collectr.searcher())



