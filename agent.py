import os
import sqlite3
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

load_dotenv()

if not Path("shop.db").exists():
    import create_db

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.environ.get("GROQ_API_KEY")
)

def csv_to_sqlite(uploaded_file) -> str:
    """Convert an uploaded CSV file into a temporary SQLite database."""
    df = pd.read_csv(uploaded_file)
    db_path = "user_upload.db"
    conn = sqlite3.connect(db_path)
    table_name = Path(uploaded_file.name).stem.replace(" ", "_").lower()
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    return db_path

def get_db_uri(source: str, uploaded_file=None) -> str:
    """Return the correct database URI based on the source the user picked."""
    if source == "demo":
        return "sqlite:///shop.db"
    elif source == "upload" and uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            db_path = csv_to_sqlite(uploaded_file)
            return f"sqlite:///{db_path}"
        elif uploaded_file.name.endswith(".db"):
            db_path = "user_upload.db"
            with open(db_path, "wb") as f:
                f.write(uploaded_file.read())
            return f"sqlite:///{db_path}"
    elif source == "url":
        return None  # URL is passed directly
    return "sqlite:///shop.db"

def ask(question: str, db_uri: str, max_retries: int = 3):
    """Ask a plain English question against any database URI."""

    try:
        db = SQLDatabase.from_uri(db_uri)
        execute_query = QuerySQLDataBaseTool(db=db)
    except Exception as e:
        return {
            "question": question,
            "sql": "",
            "raw_result": None,
            "answer": f"Could not connect to the database. Error: {str(e)}",
            "attempts": 0
        }

    sql = ""
    error = ""

    for attempt in range(max_retries):
        try:
            if attempt == 0:
                # First try: generate SQL from the question
                prompt = f"""Given the following SQLite database schema:

{db.get_table_info()}

Write a SQL query to answer this question: {question}

Return ONLY the SQL query, nothing else. Do not include backticks or formatting."""
                sql = llm.invoke(prompt).content
            else:
                # Retry: ask LLM to fix the broken SQL
                fix_prompt = f"""
The following SQL query failed with this error:

SQL: {sql}
Error: {error}

The original question was: {question}
The database has these tables: {db.get_table_info()}

Write a corrected SQL query. Return ONLY the SQL, nothing else.
"""
                sql = llm.invoke(fix_prompt).content

            # Clean up the SQL (sometimes LLM adds extra text)
            sql = sql.strip()
            if "```sql" in sql:
                sql = sql.split("```sql")[1].split("```")[0].strip()
            elif "```" in sql:
                sql = sql.split("```")[1].split("```")[0].strip()

            # Try running it
            result = execute_query.invoke(sql)

            # Ask LLM to explain the result in plain English
            explain_prompt = f"""
Question: {question}
SQL used: {sql}
Raw result: {result}

Give a clear, friendly answer to the question based on the result.
Keep it to 2-3 sentences max.
"""
            answer = llm.invoke(explain_prompt).content

            return {
                "question": question,
                "sql": sql,
                "raw_result": result,
                "answer": answer,
                "attempts": attempt + 1
            }

        except Exception as e:
            error = str(e)
            if attempt == max_retries - 1:
                return {
                    "question": question,
                    "sql": sql,
                    "raw_result": None,
                    "answer": f"Sorry, I couldn't answer that after {max_retries} attempts. Last error: {error}",
                    "attempts": attempt + 1
                }

# Quick test
if __name__ == "__main__":
    result = ask("How many customers do we have?", "sqlite:///shop.db")
    print("Answer:", result["answer"])
    print("SQL used:", result["sql"])
