# SQLify 🚀

Introducing SQLify, our AI-powered tool designed to seamlessly bridge the gap between human language and complex database queries. Revolutionizing data retrieval, SQLify enables users to effortlessly pose questions in natural language, transforming them into precise SQL queries for efficient database interrogation.

## Overview 🌐

This is an end-to-end LLM project based on Google Palm and Langchain. We are building a system that can talk to SQL databases. Users ask questions in natural language, and the system generates answers by converting those questions into an SQL query and then executing that query on an SQL database.

## Project Highlights 🌟

- We will build an LLM-based question and answer system using:
  - Google Palm LLM 🌴
  - Hugging Face embeddings 🤗
  - Streamlit for UI 🚀
  - Langchain framework 🛠️
  - Chromadb as a vector store 🧬
  - Few-shot learning 📚

In the UI, users can ask questions in natural language, and SQLify will produce the answers.




## Installation

1.Clone this repository to your local machine using:

```bash
  git clone https://github.com/yash-sojitra-20/SQLify.git
```
2.Navigate to the project directory:

```bash
  cd DataBase_Creation
```
3. Install the required dependencies using pip:

```bash
  pip install -r requirements.txt
```
4.Acquire an api key through makersuite.google.com and put it in .env file

```bash
  GOOGLE_API_KEY="your_api_key_here"
```
5. For database setup, run database/DataBase_Creation.sql in your PostgreSQL workbench

## Usage

1. Run the Streamlit app by executing:
```bash
streamlit run SQLify_Frontend.py


```

2.The web app will open in your browser where you can ask questions

## Sample Questions
  - How many total t shirts are left in total in stock?
  - How many t-shirts do we have left for Nike in XS size and white color?
  - How much is the total price of the inventory for all S-size t-shirts?
  - How much sales amount will be generated if we sell all small size adidas shirts today after discounts?
    
 ## Project Structure
  - SQLify_Frontend.py: Frontend logic for the Streamlit app.
  - SQLify_Backend.py:Backend logic for processing natural language queries into SQL.
  - SQLify_try.py: Experimental file for testing functionalities.
  - requirements.txt: A list of required Python packages for the project.
  - .env: Configuration file for storing your Google API key. 

    ![SQLify in Action](https://media.wired.com/photos/641337bd5e3ab3be4fe3e789/master/w_1600%2Cc_limit/sql_normal.gif)
