import sqlite3
from dotenv import load_dotenv
import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_ollama import ChatOllama
import re

load_dotenv()

# Initialize GPT-based LLM via OpenAI
#llm = ChatOllama(temperature=0, model="llama3.2")
llm=ChatOllama(temperature=0, model="llama3.2")

# Updated prompt template to ensure only SQL query is returned
prompt_template = """
You are an intelligent assistant that helps convert natural language queries into SQL queries. 
Your task is to take a natural language question and return only the SQL query. Do not provide any explanations, just return the query.

IMPORTANT:
- Only return the SQL query.
- Do not include any text, explanations, or commentary before or after the SQL query.
- Ensure the SQL query is clean and without any additional symbols, text, or commentary.

You are working with two related tables:

Table Name: Employee_Info

1. employee_id: Integer. The unique ID for each employee.
2. first_name: String. First name of the employee.
3. last_name: String. Last name of the employee.
4. age: Integer. Age of the employee.
5. department: String. Department in which the employee works (e.g., "HR", "IT").
6. hire_date: Date. The date the employee was hired (e.g., "2020-05-15").
7. salary: Float. The employee's salary in currency units (e.g., 50000.75).

Table Name: Employee_Projects

1. project_id: Integer. The unique ID for each project.
2. employee_id: Integer. ID referencing the employee in Employee_Info.
3. project_name: String. Name of the project (e.g., "Customer Management System").
4. project_start_date: Date. Start date of the project (e.g., "2021-01-10").
5. project_end_date: Date. End date of the project (e.g., "2022-03-30").
6. role: String. The role of the employee in the project (e.g., "Developer").

Now, based on the information provided, convert the following natural language question into an SQL query.

Ensure that you return only the SQL query, with no additional explanations, commentary, or noise.

Question: {question}
"""


# Define the prompt template using Langchain's PromptTemplate class
prompt = PromptTemplate(
    input_variables=["question"],
    template=prompt_template
)

# Create a Langchain pipeline that takes a natural language query and converts it to SQL

nl_to_sql_chain = prompt | llm

response=nl_to_sql_chain.invoke({"question":"Retrieve the names of all employees who were hired before 2020 and list their project names and roles."})

sql_query = response.content
print(sql_query)

db_conn = sqlite3.connect('employee_database.db')

# Function to execute SQL and return results in a Pandas DataFrame
def execute_sql_and_return_df(sql_query, db_conn):
    # Execute the SQL query
    result = pd.read_sql_query(sql_query, db_conn)
    return result

result_df = execute_sql_and_return_df(sql_query, db_conn)
print(result_df)