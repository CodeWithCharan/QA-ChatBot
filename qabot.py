# imports
from dotenv import load_dotenv
load_dotenv() # loading all the env variables
import streamlit as st
import os
import google.generativeai as genai

# config your gemini api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load Gemini model
model = genai.GenerativeModel("gemini-pro")

# function to get responses
def get_response(question):
    response = model.generate_content(question)
    return response.text

# initialize streamlit app

st.set_page_config(page_title="Q&A DEMO", page_icon="🤖")

st.header("Gemini LLM Application")

input = st.text_input("User: ", key="input")
submit = st.button("Ask the question")

# if user clicked submit
if submit:
    result = get_response(input)
    st.subheader("AI: ")
    st.write(result)