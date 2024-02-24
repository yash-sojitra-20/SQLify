import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get('GOOGLE_API_KEY')
from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key)
print(llm.invoke("suggest me one indian hotel name" ))