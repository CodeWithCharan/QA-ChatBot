from dotenv import load_dotenv
load_dotenv()  # loading all the env variables
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# config your Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# function to get responses
def get_response(text, img):
    if text != "":
        response = model.generate_content([text, img])
        return response.text
    response = model.generate_content(img)
    return response.text

# initialize streamlit app
st.set_page_config(page_title="Q&A Image DEMO", page_icon="🤖")

st.header("Gemini LLM Application")

input = st.text_input("User: ", key="input")

upload_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
img = None
if upload_file is not None:
    img = Image.open(upload_file)  # Open the image file
    st.image(img, caption="File uploaded!", use_column_width=True)

submit = st.button("Ask about the image")

# if user clicked submit
if submit:
    result = get_response(input, img)
    st.subheader("AI: ")
    st.write(result)