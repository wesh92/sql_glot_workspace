import streamlit as st
import sqlglot
import re
from sqlglot.dialects.dialect import Dialects

st.set_page_config(
    page_title="SQL Interactive Transpiler",
    page_icon=r"🉑",
    layout="wide",
)

col1, col2 = st.columns(2)

# Create a form with the key "my_form" and a submit button with the text "Submit".
with col1.form("my_form"):

    # Create a text input box for the user to enter their SQL query.
    sql_query = st.text_area("Enter your SQL query here:", height=40)

    # Create a dropdown menu for the user to select the origin SQL dialect.
    dialect_values = [attr for attr in dir(Dialects) if not attr.startswith("__")]
    origin_dialect = st.selectbox("Select the origin SQL dialect:", dialect_values).lower()

    # Create a dropdown menu for the user to select the output SQL dialect.
    output_dialect = st.selectbox("Select the output SQL dialect:", dialect_values).lower()

    # Create a checkbox for the user to select whether or not to format the output SQL query.
    format_checkbox = st.checkbox("Format output SQL query?")

    temp_table_replacements = {}
    # If the origin SQL dialect is TSQL, find all temp tables in the SQL query and create a text input for each.
    if origin_dialect == "tsql":
        temp_tables = set(re.findall(r"#\w+", sql_query))  # Extract temp table names using regex.
        for temp_table in temp_tables:
            temp_table_replacements[temp_table] = st.text_input(f"Enter the replacement name for the temp table {temp_table}:")

    # Create a submit button.
    submit_button = st.form_submit_button("Submit")

    # If the user has clicked the submit button, do something.
    if submit_button:
        # Check if SQL query is not empty
        if sql_query.strip() == "":
            st.error("Please enter a SQL query.")
        else:
            # If the origin SQL dialect is TSQL, replace all temp tables in the SQL query with the provided replacement names.
            if origin_dialect == "tsql":
                for temp_table, replacement_name in temp_table_replacements.items():
                    if replacement_name:
                        sql_query = sql_query.replace(temp_table, replacement_name)

            # Use the `sqlglot.transpile()` function to transpile the user's SQL query to the desired dialect.
            transpiled_sql_query = sqlglot.transpile(sql_query, origin_dialect, output_dialect, pretty=format_checkbox)

            # Display the transpiled SQL query in a text box.
            for line in transpiled_sql_query:
                col2.code(line)
