import streamlit as st

st.title("Main Title")
st.header("Header")
st.subheader("Subheader")
st.text("Plain Text")
st.markdown("**Bold Text**")

name = st.text_input("Enter Name")

st.write(name)
age = st.number_input("Enter Age")

if st.button("Click Me"):
    st.write("Button Clicked")

city = st.selectbox(
    "Select City",
    ["Mumbai", "Pune", "Delhi"]
)

agree = st.checkbox("I Agree")

value = st.slider("Select Value", 0, 100)

col1, col2 = st.columns(2)

with col1:
    st.write("Left")

with col2:
    st.write("Right")


col1, col2 = st.columns(2)

with col1:
    st.write("Left")

with col2:
    st.write("Right")

st.sidebar.title("Menu")

option = st.sidebar.selectbox(
    "Choose",
    ["Home", "About"]
)

import pandas as pd

df = pd.DataFrame({
    "Name": ["A", "B"],
    "Salary": [1000, 2000]
})

st.dataframe(df)

st.line_chart(df["Salary"])

import pandas as pd
import streamlit as st2
uploaded_file = st2.file_uploader(
    "Upload CSV2",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st2.dataframe(df)


import streamlit as st
import os

# Folder name
UPLOAD_FOLDER = "uploads"

# Check if folder exists
if not os.path.exists(UPLOAD_FOLDER):

    # Create folder if not exists
    os.mkdir(UPLOAD_FOLDER)

    st.info(f"Folder '{UPLOAD_FOLDER}' created successfully")

else:
    st.info(f"Folder '{UPLOAD_FOLDER}' already exists")


# Upload file
uploaded_file2 = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

# Save file
if uploaded_file2 is not None:

    file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file2.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file2.getbuffer())

    st.success(f"File saved successfully at: {file_path}")
    df = pd.read_csv(uploaded_file2)
    st.dataframe(df)
if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increment"):
    st.session_state.count += 1

st.write(st.session_state.count)


with st.form("my_form"):
    name = st.text_input("Name")

    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(name)

tab1, tab2 = st.tabs(["Home", "Dashboard"])

with tab1:
    st.write("Home Page")

with tab2:
    st.write("Dashboard")

with st.expander("See Details"):
    st.write("Hidden Content")

import time

progress = st.progress(0)

for i in range(100):
    time.sleep(0.01)
    progress.progress(i + 1)

import streamlit as st

st.title("AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask something")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


from pyspark.sql import SparkSession
import streamlit as st

spark = SparkSession.builder.getOrCreate()

df = spark.read.csv("C:\\Users\\akshay.mahajan.ASCENDION\\PycharmProjects\\pythonProject4\\logs\\chatbot_logs_2026-04-28.csv", header=True)

st.dataframe(df.toPandas())