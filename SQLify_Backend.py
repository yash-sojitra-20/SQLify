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
from FewShots import few_shots

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
