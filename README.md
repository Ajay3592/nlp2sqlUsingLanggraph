# 🧠 Natural Language SQL Query App with LangGraph + Gemini + Streamlit

This Streamlit application allows users to query a SQLite database using natural language. It leverages the power of **LangGraph**, **Gemini 2.0 Flash**, and **LangChain's SQLDatabaseToolkit** to interpret user questions and generate accurate SQL queries.

---

## 🚀 Features

- 🔍 Query any SQLite database using plain English
- 🧠 Powered by Google's Gemini 2.0 Flash LLM
- 🛠️ Uses LangGraph and LangChain's `create_react_agent` for dynamic tool-based reasoning
- 📊 Automatically lists tables, checks queries, and fetches schema
- 🖼️ Streamlit UI for interactive exploration

---

## 🧰 Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Gemini 2.0 Flash](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [SQLite](https://www.sqlite.org/index.html)

---

## 🧪 How It Works

The app uses LangChain's `SQLDatabaseToolkit`, which includes the following tools:

- `sql_db_list_tables`: Lists all tables in the database
- `sql_db_schema`: Retrieves schema for a given table
- `sql_db_query`: Executes SQL queries
- `sql_db_query_checker`: Validates SQL syntax before execution

These tools are passed to `create_react_agent`, which builds a ReAct-style agent capable of reasoning and tool usage.

--

## 🔮 Future Improvements
Tool Restriction via LangGraph Currently, the agent has access to all tools provided by SQLDatabaseToolkit. Using LangGraph, you can define a custom state machine to restrict tool usage based on context, user role, or query type. This allows for:

Controlled access to sensitive operations (e.g., write queries)

Role-based tool permissions

Dynamic tool routing based on query intent

Multi-DB Support Extend the app to support multiple database backends (PostgreSQL, MySQL, etc.) using LangChain's SQLDatabase abstraction.

Query History & Export Add support for saving query history and exporting results to CSV or Excel.

Authentication & Access Control Integrate user login and permission layers to secure database access.