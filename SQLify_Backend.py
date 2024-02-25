import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
from db_specifications import dbusername,dbpass,dbhost,dbport,databasename

few_shots = [
    {'Question' : "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer' : ''},
    
    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': '[(2000,)]'},
    
    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer': "[(Decimal('2960.00000000000000000000'),)]"
} ,
    
     {'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
      'SQLResult': "Result of the SQL query",
      'Answer' : '[(4200,)]'},
    
    {'Question': "How many white color Levi's shirt I have?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : '[(None,)]'},
    
    {'Question': "show price of blue tshirt of levis with after applying discount.",
     'SQLQuery' : "SELECT price - (price * pct_discount / 100) AS discounted_price FROM t_shirts JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id WHERE brand = 'Levi' AND color = 'Blue'",
     'SQLResult': "Result of the SQL query",
     'Answer' : '[(21.2500000000000000,),(18.0000000000000000,),(22.0000000000000000,)]'}
]

username = dbusername
password = dbpass
host = dbhost 
port = dbport
mydatabase = databasename
pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
db = SQLDatabase.from_uri(pg_uri)

def get_chain():
  load_dotenv()
  api_key = os.environ.get('GOOGLE_API_KEY')
  llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key)


  embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

  to_vectorize = [" ".join(example.values()) for example in few_shots]

  vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)

  example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
  )
  example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
  )
  few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=_mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
  )
  new_chain = create_sql_query_chain(llm, db, prompt=few_shot_prompt)
  return new_chain


#######################################################################################
