from scripts.Engine_search import Search
from scripts.planner import Planner
from scripts.evidence.fetcher import collect
from scripts.stripper import strip
from scripts.evidence.fetcher import fetch
from scripts.evidence.collector import Collected
ip_query = input("Enter your target word : ")
collectr = collect(search=Search,planner=Planner,query=ip_query)
res,hits = collectr.searcher()
# print(hits)
# print(res)
ftch = fetch(strip=strip,links=res)
results = ftch.information()
ans=""

clt = Collected(doc=results,query=hits[0])
k= clt.find()
# print(k)
print(" FOUndd best matched Results ..... ")
# print(results[k.argmax()])
print(k.argsort())

# for i in results:
#     ans+=i
#     ans+="------------------ --------------- --------- end search ----"

# with open("output.txt","w",encoding="utf=8") as f : 
#     f.write(ans)
