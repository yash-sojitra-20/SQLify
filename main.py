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


#sample_query solution using chain
from langchain.chains import create_sql_query_chain
db_chain = create_sql_query_chain(llm, db)

# correct -1
print("qns 1")
qns1 = db_chain.invoke({"question": "How many t-shirts do we have left for nike in extra small size and white color?"})
print(qns1)
ans1=db.run(qns1)
print(ans1)

# correct-2
qns2 = "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'"
ans2=db.run(qns2)
print(ans2)
