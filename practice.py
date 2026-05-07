import streamlit as st
import sqlite3
import pandas as pd

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="SQLite User Manager",
    layout="wide"
)

st.title("SQLite User Manager")

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# -------------------------------
# CREATE TABLE
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    age INTEGER
)
""")

conn.commit()

# =========================================================
# USER FORM SECTION
# =========================================================
st.header("Add User")

with st.form("user_form", clear_on_submit=True):

    name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    age = st.number_input(
        "Enter Age",
        min_value=0,
        step=1
    )

    submitted = st.form_submit_button("Save User")

    if submitted:

        if name.strip() == "":
            st.warning("Please enter a name.")

        else:
            try:
                cursor.execute(
                    """
                    INSERT INTO users (name, email, age)
                    VALUES (?, ?, ?)
                    """,
                    (name.strip(), email.strip(), int(age))
                )

                conn.commit()

                st.success("User saved successfully!")

            except Exception as e:
                st.error(f"Error saving user: {e}")

# =========================================================
# SHOW DATA SECTION
# =========================================================
st.header("User Data")

if st.button("Show Data"):

    try:
        cursor.execute("SELECT * FROM users")

        data = cursor.fetchall()

        df = pd.DataFrame(
            data,
            columns=["ID", "Name", "Email", "Age"]
        )

        st.dataframe(df, width="stretch")

    except Exception as e:
        st.error(f"Error fetching data: {e}")

# =========================================================
# SQL QUERY RUNNER SECTION
# =========================================================
st.header("SQL Query Runner")

# Layout for query input and button
col1, col2 = st.columns([5, 1])

# Query input
with col1:
    query = st.text_area(
        "Enter SQL Query",
        value="SELECT * FROM users",
        height=150,
        key="query_input"
    )

# Run button
with col2:
    st.write("")
    st.write("")
    run_query = st.button("Run Query")

# Placeholder for result
result_container = st.empty()

# Execute query
if run_query:

    # Clear old result immediately
    result_container.empty()

    try:
        cursor.execute(query)

        # SELECT Queries
        if query.strip().upper().startswith("SELECT"):

            data = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(data, columns=columns)

            result_container.dataframe(
                df,
                width="stretch"
            )

        else:
            # INSERT / UPDATE / DELETE / CREATE
            conn.commit()

            result_container.success(
                "Query executed successfully."
            )

    except Exception as e:
        result_container.error(f"Error: {e}")

# -------------------------------
# CLOSE CONNECTION
# -------------------------------
conn.close()