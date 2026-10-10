from scripts.Engine_search import Search
from scripts.planner import Planner
from scripts.evidence.fetcher import collect
from scripts.stripper import strip


ip_query = input("Enter your target word : ")
collectr = collect(search=Search,planner=Planner,query=ip_query)
res = collectr.searcher()
results = ""
for i,link in enumerate(res):
    print(f"------------------ Search Results {i}-----------")
    print("For LINK : ",link)
    print()
    results+=str(strip(link=link))
    results += "-----------------------"



with open("output.txt", "w",encoding="utf-8") as f : 
    f.write(results)


