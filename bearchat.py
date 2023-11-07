# Import necessary modules
import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun

# Set the app title and page config
st.set_page_config(page_title="🐻💬 BearGPT Chat")
st.title("🐻💬 Welcome to BearGPT Chat")

# Sidebar for API key input
with st.sidebar:
    openai_api_key = st.text_input("Please Enter OpenAI API Key", key="langchain_search_api_key_openai", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# Welcome message
"""
Welcome Bears to BearGPT Chat! This is a demo of a python built AI chatbot built to serve your needs as a student feel free to ask any questions about school or anything else you would like to know about.
"""

# Initialize chat messages if not present
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

# Display previous chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle new user input
if prompt := st.chat_input(placeholder="Tell me about Bridgwater State University"):
    # Append the new user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the new user message
    st.chat_message("user").write(prompt)

    # Check for OpenAI API key
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Initialize the language model and search tool
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    
    # Create the search agent
    search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)

    # Generate and display the assistant's response
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
