import openai
import streamlit as st
import time

# Set the Streamlit page configuration
st.set_page_config(page_title="🐻💬 BearGPT Chat", layout="wide")

# Streamlit title
st.title("🐻💬 Welcome to BearGPT Chat")

# Input for OpenAI API Key
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
if openai_api_key:
    openai.api_key = openai_api_key
else:
    st.error("Please enter your OpenAI API key to proceed.")
    st.stop()

# Welcome message
st.write("Welcome Bears to BearGPT Chat! This is a demo of an AI chatbot built to serve your needs as a student. Feel free to ask any questions about school or anything else you would like to know about.")

# Function to create an OpenAI Assistant
def create_assistant():
    return openai.Assistant.create(
        model="gpt-4-1106-preview",
        name="BSU Information Assistant",
        instructions="You are an assistant that provides information about Bridgewater State University. Answer questions to the best of your knowledge and provide helpful responses.",
    )

# Function to run the assistant and get the response
def get_assistant_response(assistant_id, user_message):
    thread = openai.Thread.create()
    message = openai.Message.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )
    run = openai.Run.create(
        assistant_id=assistant_id,
        thread_id=thread.id
    )
    
    # Polling for the assistant's response
    while True:
        run_status = openai.Run.retrieve(run.id)
        if run_status['status'] == 'succeeded':
            break
        time.sleep(1)  # Poll every second

    messages = openai.Message.list(thread_id=thread.id)
    return [msg['content'] for msg in messages.data if msg['role'] == 'assistant']

# Initialize assistant
assistant = create_assistant() if openai_api_key else None

# User input
user_input = st.text_input("Ask a question:")

# If there's user input, get and display the response from the assistant
if user_input and assistant:
    responses = get_assistant_response(assistant.id, user_input)
    for response in responses:
        st.write(response)
