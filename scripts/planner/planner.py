import os 
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("API_KEY")



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
                    {"role": "user", "content": query}
                ],
                )
            self.chat =self.res.choices[0].message.content
            return self.chat
        except Exception as e : 
            print("error happen", e)

if __name__ ==  "__main__":
    inst=Planner()
    print(inst.paln("What is capital of india "))
