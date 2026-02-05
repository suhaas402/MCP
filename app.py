import streamlit as st
import asyncio
from client import run_query

st.set_page_config(page_title="MCP Demo", layout="centered")

st.title("MCP Tool Demo")
st.write("Math and Weather using MCP")

query = st.text_input(
    "Enter a query",
    placeholder="Example: What is 15 + 27? or Weather in Tokyo"
)

if st.button("Run"):
    if query.strip() == "":
        st.warning("Please enter a query.")
    else:
        with st.spinner("Running MCP tools..."):
            result = asyncio.run(run_query(query))
        st.success("Result")
        st.write(result)
