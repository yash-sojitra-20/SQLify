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
password = "postgres" 
host = "localhost" 
port = "5432"
mydatabase = "atliq_tshirts"

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
print(ans3)

qns4 = "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'"
ans4=db.run(qns4)
print(ans4)

#incorret-5 -- forgate to sum val...
# print("qns 5")
# qns5 = db_chain.invoke({"question": "How many white color Levi's t shirts we have available?"})
# print(qns5)
# print(db.run(qns5))

# correct-5
qns5 = "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'"
ans5=db.run(qns5)
print(ans5)

few_shots = [
    {'Question' : "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer' : qns1},
    
    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': qns2},
    
    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer': qns3} ,
    
     {'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
      'SQLResult': "Result of the SQL query",
      'Answer' : qns4},
    
    {'Question': "How many white color Levi's shirt I have?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : qns5}
]