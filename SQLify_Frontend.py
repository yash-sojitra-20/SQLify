import streamlit as st
from SQLify_Backend import get_chain, db

# Set Streamlit page configuration
st.set_page_config(
    page_title="SQLify App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set a custom theme using Streamlit themes
st.markdown(
    """
    <style>
    body {
        background-color: #f8f9fa; 
        font-family: 'Arial', sans-serif; 
    }
    .st-bw {
        color: #007BFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add a title with a stylish header
st.title("SQLify: Talk to your Database🗄️")
st.markdown("---")

# Input for the user's question
question = st.text_input("Ask a Question:", "")

# Display the question and answer
if question:
    # Invoke the backend and run the query
    chain = get_chain()
    qns = chain.invoke({"question": question})
    response = db.run(qns)

    # Display the query and answer with styled headers
    st.markdown("### Query:")
    st.code(qns, language="sql")

    st.markdown("### Answer:")
    st.code(response, language="sql")
