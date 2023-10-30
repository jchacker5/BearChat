import os 
import streamlit as st
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
import json
# Streamlit Configuration
st.set_page_config(page_title="Welcome to BearChat", page_icon='🐻💬', layout="centered", initial_sidebar_state="collapsed")
st.title("Welcome to BearChat🐻💬")

# User OpenAI API Key Input
user_openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
enable_custom = bool(user_openai_api_key)
openai_api_key = user_openai_api_key if enable_custom else "not_supplied"

# Initialize LLM
llm = ChatOpenAI(
    temperature=0,
    openai_api_key=openai_api_key,
    model_name="gpt-3.5-turbo-0613",
    max_tokens=2048,
    streaming=True
)

# Modify web_qa to return the answer
def web_qa(url_list, query):
    loader_list = []
    for i in url_list:
        loader_list.append(WebBaseLoader(i))
    index = VectorstoreIndexCreator().from_loaders(loader_list)
    ans = index.query(question=query, llm=llm)
    return ans

# Define web_qa as a tool
def web_qa_tool(query):
    url_list = ["https://www.bridgew.edu"]
    return web_qa(url_list, query)

# Initialize Langchain Agent with only web_qa_tool
agent_chain = initialize_agent(
    tools=[Tool(name="web_qa_tool", func=web_qa_tool, description="This tool performs web-based QA")],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Ask me a question about Bridgew.edu!"}]

# Chat UI and Logic
if st.session_state.get("messages"):
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    langchain_response = agent_chain.run(prompt)
    
    print("Debug info: ", langchain_response)  # Debug: Print the response
    
    if isinstance(langchain_response, str):  # Check if it's a string
        answer = langchain_response  # Directly use the string as the answer
    elif isinstance(langchain_response, dict):  # Check if it's a dictionary
        answer = langchain_response.get('answer', 'No answer found.')  # Safely access key
    else:
        answer = "No answer found."
    
    with st.chat_message("assistant"):
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})