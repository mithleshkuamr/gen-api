# # import streamlit as st
# # import sqlite3
# # import google.generativeai as genai

# # # Provide your Genai api Key
# # genai.configure(api_key="AIzaSyC6rZAdSL6sRuxceXsKYREVRRxttNSzT0E")

# # def get_gemini_response(question,prompt):
# #     model=genai.GenerativeModel('gemini-pro')
# #     response=model.generate_content([prompt[0],question])
# #     return response.text

# # def read_sql_query(sql,db):
# #     conn=sqlite3.connect(db)
# #     cur=conn.cursor()
# #     cur.execute(sql)
# #     rows=cur.fetchall()
# #     conn.commit()
# #     conn.close()
# #     for row in rows:
# #         print(row)
# #     return rows

# # ## Define Your Prompt
# # prompt=[
# #     """
# #     You are an expert in converting English questions to SQL query!
# #     The SQL database has the name Naresh_it_employee and has the following columns - employee_name, 
# #     employee_role, employee_salary \n\nFor example,\nExample 1 - How many entries of records are present?, 
# #     the SQL command will be something like this SELECT COUNT(*) FROM Naresh_it_employee ;
# #     \nExample 2 - Tell me all the employees working in Data Science role?, 
# #     the SQL command will be something like this SELECT * FROM Naresh_it_employee 
# #     where employee_role="Data Science"; 
# #     also the sql code should not have ``` in beginning or end and sql word in output

# #     """


# # ]

# # ## Streamlit App

# # st.set_page_config(page_title="I can Retrieve Any SQL query")
# # st.header("Gemini App To Retrieve SQL Data")

# # question=st.text_input("Input: ",key="input")

# # submit=st.button("Ask the question")

# # # if submit is clicked
# # if submit:
# #     response=get_gemini_response(question,prompt)
# #     print(response)
# #     response=read_sql_query(response,"Naresh_it_employee.db")
# #     st.subheader("The Response is")
# #     for row in response:
# #         print(row)
# #         st.header(row)

# import streamlit as st
# import sqlite3
# import google.generativeai as genai

# # Provide your Genai API Key
# genai.configure(api_key="AIzaSyC6rZAdSL6sRuxceXsKYREVRRxttNSzT0E")

# def get_gemini_response(question, prompt):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([prompt[0], question])
    
#     # Remove any code block markers from the response
#     cleaned_response = response.text.replace('```sql', '').replace('```', '').strip()
    
#     return cleaned_response

# def read_sql_query(sql, db):
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     conn.commit()
#     conn.close()
#     return rows

# # Define Your Prompt
# prompt = [
#     """
#     You are an expert in converting English questions to SQL query!
#     The SQL database has the name Naresh_it_employee and has the following columns - employee_name, 
#     employee_role, employee_salary.
#     """
# ]

# st.set_page_config(page_title="I can Retrieve Any SQL query")

# # Handling API calls via query parameters
# query_params = st.query_params

# if 'question' in query_params:
#     question = query_params['question'][0]
#     response = get_gemini_response(question, prompt)
#     result = read_sql_query(response, "Naresh_it_employee.db")
#     st.json(result)  # Returns the result in JSON format
# else:
#     # Regular Streamlit interface
#     st.header("Gemini App To Retrieve SQL Data")
#     question = st.text_input("Input: ", key="input")
#     submit = st.button("Ask the question")

#     if submit:
#         response = get_gemini_response(question, prompt)
#         result = read_sql_query(response, "Naresh_it_employee.db")
#         st.subheader("The Response is")
#         for row in result:
#             st.write(row)



import streamlit as st
import sqlite3
import google.generativeai as genai
import json
import os

# Provide your Genai API Key
genai.configure(api_key="AIzaSyC6rZAdSL6sRuxceXsKYREVRRxttNSzT0E")

# Path to the history file
history_file = "history.json"

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    
    # Remove any code block markers from the response
    cleaned_response = response.text.replace('```sql', '').replace('```', '').strip()
    
    return cleaned_response

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

def load_history():
    """Load history from the JSON file."""
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    """Save history to the JSON file."""
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)

# Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Naresh_it_employee and has the following columns - employee_name, 
    employee_role, employee_salary.
    """
]

st.set_page_config(page_title="I can Retrieve Any SQL query")

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = load_history()

# Check if running in API mode
query_params = st.query_params

if 'question' in query_params:
    question = query_params['question'][0]
    response = get_gemini_response(question, prompt)
    result = read_sql_query(response, "Naresh_it_employee.db")
    
    # Extract only the employee names
    employee_names = [row[0] for row in result]
    
    # Add to history
    entry = {'question': question, 'response': employee_names}
    st.session_state.history.append(entry)
    save_history(st.session_state.history)
    
    st.json(employee_names)  # Return the result in JSON format
else:
    # Regular Streamlit interface
    st.header("Gemini App To Retrieve SQL Data")
    
    question = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")

    if submit:
        response = get_gemini_response(question, prompt)
        result = read_sql_query(response, "Naresh_it_employee.db")
        
        # Extract only the employee names
        employee_names = [row[0] for row in result]
        
        # Add to history
        entry = {'question': question, 'response': employee_names}
        st.session_state.history.append(entry)
        save_history(st.session_state.history)
        
        st.subheader("The Response is")
        st.write(employee_names)

    # Display history
    if st.session_state.history:
        st.subheader("Query History")
        for entry in st.session_state.history:
            st.write(f"**Question:** {entry['question']}")
            st.write(f"**Response:** {entry['response']}")


# import streamlit as st
# import sqlite3
# import google.generativeai as genai
# import json
# import os

# # Provide your Genai API Key
# genai.configure(api_key="AIzaSyC6rZAdSL6sRuxceXsKYREVRRxttNSzT0E")

# # Path to the history file
# history_file = "history.json"

# def get_gemini_response(question, prompt):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([prompt[0], question])
    
#     # Remove any code block markers from the response
#     cleaned_response = response.text.replace('```sql', '').replace('```', '').strip()
    
#     return cleaned_response

# def read_sql_query(sql, db):
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     conn.commit()
#     conn.close()
#     return rows

# def load_history():
#     """Load history from the JSON file."""
#     if os.path.exists(history_file):
#         with open(history_file, "r") as f:
#             return json.load(f)
#     return []

# def save_history(history):
#     """Save history to the JSON file."""
#     with open(history_file, "w") as f:
#         json.dump(history, f, indent=4)

# # Define Your Prompt
# prompt = [
#     """
#     You are an expert in converting English questions to SQL query!
#     The SQL database has the name Naresh_it_employee and has the following columns - employee_name, 
#     employee_role, employee_salary.
#     """
# ]

# st.set_page_config(page_title="I can Retrieve Any SQL query")

# # Initialize session state for history
# if 'history' not in st.session_state:
#     st.session_state.history = load_history()
# if 'selected_question' not in st.session_state:
#     st.session_state.selected_question = None

# # Check if running in API mode
# query_params = st.query_params

# if 'question' in query_params:
#     question = query_params['question'][0]
#     response = get_gemini_response(question, prompt)
#     result = read_sql_query(response, "Naresh_it_employee.db")
    
#     # Extract only the employee names
#     employee_names = [row[0] for row in result]
    
#     # Add to history
#     entry = {'question': question, 'response': employee_names}
#     st.session_state.history.append(entry)
#     save_history(st.session_state.history)
    
#     st.json(employee_names)  # Return the result in JSON format
# else:
#     # Regular Streamlit interface
#     st.header("Gemini App To Retrieve SQL Data")
    
#     question = st.text_input("Input: ", key="input")
#     submit = st.button("Ask the question")

#     if submit:
#         response = get_gemini_response(question, prompt)
#         result = read_sql_query(response, "Naresh_it_employee.db")
        
#         # Extract only the employee names
#         employee_names = [row[0] for row in result]
        
#         # Add to history
#         entry = {'question': question, 'response': employee_names}
#         st.session_state.history.append(entry)
#         save_history(st.session_state.history)
        
#         st.subheader("The Response is")
#         st.write(employee_names)

#     # Display history
#     if st.session_state.history:
#         st.subheader("Query History")
#         for i, entry in enumerate(st.session_state.history):
#             if st.button(f"Show result for query {i+1}:", key=i):
#                 st.session_state.selected_question = entry['question']
#                 response = get_gemini_response(entry['question'], prompt)
#                 result = read_sql_query(response, "Naresh_it_employee.db")
                
#                 # Extract only the employee names
#                 employee_names = [row[0] for row in result]
                
#                 st.subheader("The Response is")
#                 st.write(employee_names)
