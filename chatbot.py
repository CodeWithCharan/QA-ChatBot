from dotenv import load_dotenv
load_dotenv()  # loading all the env variables
import streamlit as st
import os
import google.generativeai as genai
from streamlit import components

# config your Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load Gemini model
model = genai.GenerativeModel("gemini-pro")

# chat var
chat = model.start_chat(history=[])

# function to get responses
def get_response(question):
    response = chat.send_message(question, stream=True)
    return response

# initialize streamlit app
st.set_page_config(page_title="ChatBot", page_icon="🤖")

# Dark mode styling
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: white;
    }
    .chat-bubble {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #1f7a8c;
        color: white;
        align-self: flex-end;
    }
    .bot-bubble {
        background-color: #2e2e2e;
        color: white;
        align-self: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
        background-color: #2c2c2c;
        border-radius: 10px;
        margin-top: 20px;
    }
    .input-container {
        margin-top: 20px;
    }
    input[type="text"] {
        background-color: #1c1c1c;
        color: white;
        border: 1px solid #555;
        border-radius: 5px;
    }
    button {
        background-color: #1f7a8c;
        color: white;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.header("Gemini LLM ChatBot")

# chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("User: ", key="input", placeholder="Type your message here...")
submit = st.button("Submit")

if user_input and submit:
    response = get_response(user_input)
    # add query to the chat history
    st.session_state['chat_history'].append(('You', user_input))
    
    full_response = ""
    # Collect all chunks of the bot's response
    for chunk in response:
        full_response += chunk.text
    # Add the full response to the chat history
    st.session_state['chat_history'].append(('Bot', full_response))

# Chat history
st.subheader("Chat")
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, text in st.session_state['chat_history']:
    if role == 'You':
        st.markdown(f'<div class="chat-bubble user-bubble"><strong>{role}:</strong> {text}</div>', unsafe_allow_html=True)
    else:
        # Check if the bot response contains markdown content
        if '|' in text and '-' in text:  # Rough check for markdown table
            st.markdown(f'<div class="chat-bubble bot-bubble"><strong>{role}:</strong></div>', unsafe_allow_html=True)
            st.markdown(text, unsafe_allow_html=True)  # Render markdown content
        else:
            st.markdown(f'<div class="chat-bubble bot-bubble"><strong>{role}:</strong> {text}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Add some padding to the input area for better UI
st.markdown('<div class="input-container">', unsafe_allow_html=True)
