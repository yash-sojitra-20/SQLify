#this is experimental file

#palm llm integration using langchain
import os
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get('GOOGLE_API_KEY')
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key)
# print(llm.invoke("suggest me one indian hotel name"))


#Database connection 
# from langchain.utilities import SQLDatabase
from langchain_community.utilities import SQLDatabase
username = "postgres" 
password = "yps20" 
host = "localhost" 
port = "5432"
mydatabase = "tshirts"

pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
db = SQLDatabase.from_uri(pg_uri)
# print(db.table_info)


#sample_query solution using chain
from langchain.chains import create_sql_query_chain
db_chain = create_sql_query_chain(llm, db)

# correct -1
# print("qns 1")
qns1 = db_chain.invoke({"question": "How many t-shirts do we have left for nike in extra small size and white color?"})
# print(qns1)
ans1=db.run(qns1)
# print(ans1)

# correct-2
qns2 = "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'"
ans2=db.run(qns2)
# print(ans2)


#Extra_sample_query solution using chain
# incorrect-3
# print("qns 3")
# qns3 = db_chain.invoke({"question": "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue our store will generate (post discounts)?"})
# print(qns3)
# print(db.run(qns3))

# correct-3
qns3 = """
select sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """
ans3=db.run(qns3)
# print(ans3)

#correct-4
qns4 = "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'"
ans4=db.run(qns4)
# print(ans4)

#incorret-5 --> forgate to sum val...
# print("qns 5")
# qns5 = db_chain.invoke({"question": "How many white color Levi's t shirts we have available?"})
# print(qns5)
# print(db.run(qns5))

# correct-5
qns5 = "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'"
ans5=db.run(qns5)
# print(ans5)


#Few_shots creation
few_shots = [
    {'Question' : "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer' : ans1},
    
    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': ans2},
    
    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer': ans3} ,
    
     {'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
      'SQLResult': "Result of the SQL query",
      'Answer' : ans4},
    
    {'Question': "How many white color Levi's shirt I have?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : ans5}
]


#Embedding using HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
# e = embeddings.embed_query("How many white color Levi's shirt I have?")
# e[:5]


#Vectorize sample_query_values for SemanticSearch
from langchain.prompts import SemanticSimilarityExampleSelector
to_vectorize = [" ".join(example.values()) for example in few_shots]
# print(to_vectorize)


#Store vectorize data to vector_Database
#Use Chroma as vector_Database
from langchain_community.vectorstores import Chroma
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
)


#Generates Query using SemanticSearch
example_selector.select_examples({"Question": "How many Adidas T shirts I have left in my store?"})
#Generated queries example
# [{'Answer': "SELECT stock_quantity FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
#   'Question': 'How many t-shirts do we have left for Nike in XS size and white color?',
#   'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
#   'SQLResult': 'Result of the SQL query'},
#  {'Answer': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
#   'Question': 'If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?',
#   'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
#   'SQLResult': 'Result of the SQL query'}]


#Bound the model with some constrain
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt

#Generated prompts
# 1
# print(_mysql_prompt)
# You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
# Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
# Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
# Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
# Pay attention to use CURDATE() function to get the current date, if the question involves "today".

# Use the following format:

# Question: Question here
# SQLQuery: SQL Query to run
# SQLResult: Result of the SQLQuery
# Answer: Final answer here

# 2
# print(PROMPT_SUFFIX)
# Only use the following tables:
# {table_info}
# Question: {input}


#Creation of FewShotPromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
)


#Establised connection between GooglePalm (llm) and vector_Database
#When model get confused it looks in to vector_Database for SemanticSearch
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=_mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
)


#NewChain creation with FewShotPromptTemplate
new_chain = create_sql_query_chain(llm, db, prompt=few_shot_prompt)


#sample_query solution using NewChain

# print("newqns1")
newqns1 = new_chain.invoke({"question": "How many white color Levi's shirt I have?"})
newans1 = db.run(newqns1)
# print(newqns1)
# SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'
# print(newans1)
# [(None,)]

# print("newqns2")
newqns2 = new_chain.invoke({"question": "How much is the price of the inventory for all small size t-shirts?"})
newans2 = db.run(newqns2)
# print(newqns2)
# SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'
# print(newans2)
# [(2000,)]

# print("newqns3")
newqns3 = new_chain.invoke({"question": "How much is the price of all white color levi t shirts?"})
newans3 = db.run(newqns3)
# print(newqns3)
# SELECT sum(price*stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'
# print(newans3)
# [(None,)]

# print("newqns4")
newqns4 = new_chain.invoke({"question": "if we have to sell all the Van Heuson T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?"})
newans4 = db.run(newqns4)
# print(newqns4)
# SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
# (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Van Huesen'
# group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
# print(newans4)
# [(Decimal('3495.00000000000000000000'),)]

# print("newqns5")
newqns5 = new_chain.invoke({"question": "How much revenue  our store will generate by selling all Van Heuson TShirts without discount?"})
newans5 = db.run(newqns5)
# print(newqns5)
# SELECT SUM(price*stock_quantity) FROM t_shirts WHERE brand = 'Van Huesen'
# print(newans5)
# [(4775,)]

#######################################################################################
