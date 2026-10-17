import os 
from dotenv import load_dotenv
from google import genai
import json 
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("API_KEY")
MAX_TOKEN = os.getenv("MAX_TOKEN")
TEMP =  os.getenv("TEMP")
test_query= "What is capital of india "


SYSTEM_PROMPT = """You are the research planner for an evidence-grounded claim verification tool.
Create exactly ONE research task for the user's complete query. Keep all relevant
aspects of the query within that task; do not decompose it into separate claims.
Do not answer the query, assert a verdict, search, or invent sources.

Return only valid JSON with this structure:
{
  "research_tasks": [{
    "id": "task_001",
    "keyword": ["concise search terms"],
    "objective": "Verify the user's complete query",
    "claim_to_verify": "the complete user query, preserving its meaning",
    "claim_type": "factual | comparative | quantitative | temporal | interpretive",
    "priority": "critical",
    "parallelizable": false,
    "preferred_sources": ["appropriate source types"],
    "supporting_evidence_plan": {
      "objective": "Find evidence supporting the complete query",
      "search_queries": ["targeted neutral web searches"],
      "retrieval_hints": ["short claim-specific phrases"]
    },
    "opposing_evidence_plan": {
      "objective": "Find contradictions, limits, exceptions, or missing conditions",
      "search_queries": ["targeted neutral web searches"],
      "retrieval_hints": ["short claim-specific phrases"]
    },
    "requires_independent_verification": true,
    "requires_primary_source": false,
    "dependencies": []
  }]
}
Use targeted searches on both sides. Keep the task broad enough to cover the
whole query, while making each search query specific enough to find useful sources.
"""
class Planner:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.aicredits.in/v1",
            api_key=API_KEY,
            )
        
        
    def paln(self,query):
        try:
            self.res = self.client.chat.completions.create(
                model="openai/gpt-6-luna",
                messages=[
                           {
                                "role": "system",
                                "content": SYSTEM_PROMPT
                            },
                            {
                                "role": "user", 
                                "content": query
                            }
                    ],           
                )
            
            chat =self.res.choices[0].message.content
            return json.loads(chat)
        except Exception as e : 
            print("error happen", e)



if __name__ ==  "__main__":
    inst=Planner()
    res=inst.paln(test_query)
    data = (res)
    print(type(data))
    print(data)
