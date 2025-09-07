# Import the required libraries

import streamlit as st
from PIL import Image
import sqlite3
from langchain_community.utilities import SQLDatabase
from typing import Literal
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent

# get secrets and initialize LLM
openai_key = st.secrets["openai"]["api_key"]

# LLM setup
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, api_key=openai_key)

# Connect to the database
#db = sqlite3.connect('shop.db')
db = SQLDatabase.from_uri("sqlite:///shop.db")

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

image = Image.open("sample_data.jpg")
st.image(image, caption="List of Tables availble on database")

# Input field
user_input = st.text_input("Type your natural language sql query here...")

# Submit button
if st.button("Submit"):
    if user_input:
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
        #result = agent.invoke({"input": user_input})
        #print(result['messages'][-1].content)
        st.write(result['messages'][-1].content)
    else:
        st.warning("Please enter a query before submitting.")


