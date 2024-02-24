#palm llm integration using langchain
import os
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get('GOOGLE_API_KEY')
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key)
# print(llm.invoke("suggest me one indian hotel name"))


#Database connection 
from langchain.utilities import SQLDatabase
username = "postgres" 
password = "yps20" 
host = "localhost" 
port = "5432"
mydatabase = "tshirts"

pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
db = SQLDatabase.from_uri(pg_uri)
print(db.table_info)
