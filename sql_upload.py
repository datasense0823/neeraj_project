import sqlite3
import pandas as pd

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('employee_database.db')
cursor = conn.cursor()

# Step 1: Define table creation queries for both tables
create_employee_info_table = '''
CREATE TABLE IF NOT EXISTS Employee_Info (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    age INTEGER,
    department TEXT,
    hire_date TEXT,
    salary REAL
);
'''

create_employee_projects_table = '''
CREATE TABLE IF NOT EXISTS Employee_Projects (
    project_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    project_name TEXT,
    project_start_date TEXT,
    project_end_date TEXT,
    role TEXT,
    FOREIGN KEY (employee_id) REFERENCES Employee_Info(employee_id)
);
'''

# Step 2: Execute the table creation queries
cursor.execute(create_employee_info_table)
cursor.execute(create_employee_projects_table)

# Step 3: Read CSV files into Pandas DataFrames
employee_info_df = pd.read_csv('/Users/fnusatvik/Desktop/neeraj_project/employee_info.csv')
employee_projects_df = pd.read_csv('/Users/fnusatvik/Desktop/neeraj_project/employee_projects.csv')

# Step 4: Insert data from DataFrames into SQLite tables
employee_info_df.to_sql('Employee_Info', conn, if_exists='append', index=False)
employee_projects_df.to_sql('Employee_Projects', conn, if_exists='append', index=False)

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data has been successfully uploaded to the SQLite database.")
