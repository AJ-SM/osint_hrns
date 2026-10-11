from scripts.Engine_search import Search
from scripts.planner import Planner
from scripts.evidence.fetcher import collect
from scripts.stripper import strip
from scripts.evidence.fetcher import fetch
from scripts.evidence.collector import Collected
from scripts.evidence.extractor import Evidence






# V3 --- gr8 1 

ip_query = input("Enter your target word : ")
get = Evidence(querry=ip_query)
get.ranState()






# V2
# collectr = collect(search=Search,planner=Planner,query=ip_query)
# res,hits = collectr.searcher()
# ftch = fetch(strip=strip,links=res)
# results = ftch.information()
# clt = Collected(doc=results,query=hits[0])
# k= clt.find()
# print(" FOUndd best matched Results ..... ")
# print(k.argsort())



# V1
# for i in results:
#     ans+=i
#     ans+="------------------ --------------- --------- end search ----"

# with open("output.txt","w",encoding="utf=8") as f : 
#     f.write(ans)
