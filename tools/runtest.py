from scripts.Engine_search import Search
from scripts.planner import Planner





ip_query = input("Enter your target word : ")
engine = Search(ip_query,20)
res = engine.ddg()
for i,seraches in enumerate(res):
    print(f"Search Results :{i} =  ", seraches['href'])

