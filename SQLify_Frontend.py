import streamlit as st
from SQLify_Backend import get_chain,db

st.title("T Shirts: Database Q&A 👕")

question = st.text_input("Question: ")

if question:
    chain = get_chain()
    qns = chain.invoke({"question": question})
    response = db.run(qns)

    st.header("Answer")
    st.write(response)