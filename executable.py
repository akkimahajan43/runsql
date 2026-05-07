import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Analytics Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Users", "1200")
col2.metric("Revenue", "$15K")
col3.metric("Growth", "12%")

st.image("https://via.placeholder.com/800x300", caption="Overview")