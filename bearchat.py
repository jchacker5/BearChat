import openai
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pdfkit
import time
import os
from dotenv import load_dotenv

# Load environment variables and set Streamlit configuration
load_dotenv()
st.set_page_config(page_title="🐻💬 BearChat", layout="wide")
st.title("🐻💬 Welcome to BearChat")

# Initialize OpenAI client with API key
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai

# Assistant configuration
assistant_id = 'asst_or5rq7uFw9b6Yfcm1MXqOzSE'

# Scrape website and convert text to PDF
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def text_to_pdf(text, filename):
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_string(text, filename, configuration=config)
    return filename

def upload_to_openai(filepath):
    with open(filepath, "rb") as file:
        response = openai.File.create(file=file, purpose="answers")
    return response.id

# Create an OpenAI Assistant
@st.cache(allow_output_mutation=True)
def create_assistant():
    try:
        return client.beta.assistants.create(
            model="gpt-4-1106-preview",
            name="BearChat Assistant",
            instructions="Assist students with queries related to Bridgewater State University.",
            tools=[{"type": "code_interpreter"}, {"type": "web_scraping"}, {"type": "web_search"}]
        )
    except Exception as e:
        st.error(f"Failed to create assistant: {e}")
        st.stop()

assistant = create_assistant()

# Get and display assistant response
def get_assistant_response(assistant_id, user_message):
    try:
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_message)
        run = client.beta.threads.runs.create(assistant_id=assistant_id, thread_id=thread.id)
        timeout = 30  # Timeout after 30 seconds
        start_time = time.time()
        while True:
            run_status = client.beta.threads.retrieve(run.id)
            if run_status['status'] == 'succeeded': break
            elif run_status['status'] == 'failed' or time.time() - start_time > timeout:
                st.error("Error in processing request.")
                return []
            time.sleep(1)
        return [msg['content'] for msg in client.beta.threads.messages.list(thread_id=thread.id).data if msg['role'] == 'assistant']
    except Exception as e:
        st.error(f"Error: {e}")
        return []

user_input = st.text_input("Tell me about Bridgewater State University...")
if user_input and assistant:
    responses = get_assistant_response(assistant.id, user_input)
    for response in responses:
        st.write(response)
