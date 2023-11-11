import openai
import streamlit as st
import time

# Set the Streamlit page configuration
st.set_page_config(page_title="🐻💬 BearGPT Chat", layout="wide")

# Streamlit title
st.title("🐻💬 Welcome to BearGPT Chat")

# Input for OpenAI API Key
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.error("Please enter your OpenAI API key to proceed.")
    st.stop()

# Setting the API key
openai.api_key = openai_api_key

# Welcome message
st.write("Welcome Bears to BearGPT Chat! ...")

# Function to create an OpenAI Assistant
@st.cache(allow_output_mutation=True)
def create_assistant():
    try:
        return openai.Assistant.create(
            model="gpt-4-1106-preview",
            name="BSU Information Assistant",
            instructions="You are an assistant that provides information ...",
            tools=[{"type": "code_interpreter"}],
        )
    except Exception as e:
        st.error(f"Failed to create assistant: {e}")
        st.stop()

# Function to run the assistant and get the response
def get_assistant_response(assistant_id, user_message):
    try:
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
        timeout = 30  # timeout after 30 seconds
        start_time = time.time()
        while True:
            run_status = openai.Run.retrieve(run.id)
            if run_status['status'] == 'succeeded':
                break
            elif run_status['status'] == 'failed':
                st.error("Assistant run failed.")
                return []
            elif time.time() - start_time > timeout:
                st.error("Timeout occurred while waiting for the assistant's response.")
                return []
            time.sleep(1)

        messages = openai.Message.list(thread_id=thread.id)
        return [msg['content'] for msg in messages.data if msg['role'] == 'assistant']
    except Exception as e:
        st.error(f"Error while getting assistant response: {e}")
        return []

# Initialize assistant
assistant = create_assistant()

# User input
user_input = st.text_input("Ask a question:")

# If there's user input, get and display the response from the assistant
if user_input and assistant:
    responses = get_assistant_response(assistant.id, user_input)
    for response in responses:
        st.write(response)
