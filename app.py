# Import the required libraries

import streamlit as st
import sqlite3
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langgraph.prebuilt import ToolNode
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent

# get secrets and initialize LLM

api_key = st.secrets["gemini"]["api_key"]
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

# Connect to the database
db = sqlite3.connect('shop.db')

# Initialize SQLDatabaseToolkit 
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

# Create react agent

system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
"""

agent = create_react_agent(
    llm,
    tools,
    prompt=system_prompt,
)


# Set page config
st.set_page_config(page_title="Natural Language to SQL", layout="centered")

# Title
st.title("NLP2SQL")

# Input field
user_input = st.text_input("Type your message...")

# Submit button
if st.button("Submit"):
    if user_input:
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
        print(result['messages'][-1].content)
        st.write(result['messages'][-1].content)
    else:
        st.warning("Please enter a message before submitting.")
