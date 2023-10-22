from pathlib import Path
import streamlit as st
import sqlite3
import asyncio
from langchain import OpenAI, LLMMathChain, SQLDatabase, SQLDatabaseChain, Tool, initialize_agent, AgentType
from langchain.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models.openai import ChatOpenAI
from datetime import datetime
# Streamlit Configuration

st.set_page_config(page_title="Welcome to BearChat", page_icon='🐻💬', layout="centered", initial_sidebar_state="collapsed")
st.title("Welcome to BearChat🐻💬, powered by ChatGPT")
# SQLite Database Initialization
DB_PATH = Path("queries.db").absolute()
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS questions (question TEXT, answer TEXT)''')
conn.commit()

# User OpenAI API Key Input
user_openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
enable_custom = bool(user_openai_api_key)
openai_api_key = user_openai_api_key if enable_custom else "not_supplied"

# Initialize LLM and Tools
llm = ChatOpenAI(
        temperature=0,
        openai_api_key=openai_api_key,
        model_name="gpt-4",
        max_tokens=2048,
        streaming=True,
    )

# Define web_qa 
def web_qa(url_list, query, output_name):
    loader_list = []
    for i in url_list:
        print('loading url: %s' % i)
        loader_list.append(WebBaseLoader(i))

    index = VectorstoreIndexCreator().from_loaders(loader_list)
    ans = index.query(question=query,
                      llm=llm)
    print("")
    print(ans)

    outfile_name = output_name + datetime.now().strftime("%m-%d-%y-%H%M%S") + ".out"
    with open(outfile_name, 'w') as f:
        f.write(ans)


# Define web_qa as a tool
def web_qa_tool(query):
    url_list = [
        "https://example1.com",
        "https://example2.com"
    ]
    web_qa(url_list, query, "output_name")

tools = [
    Tool(name="web_qa_tool", func=web_qa_tool),
    Tool(name="Queries DB", func=db_chain.run),
]

# Initialize Langchain Agent
agent_chain = initialize_agent(
    tools=tools,
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

    cursor.execute("SELECT answer FROM questions WHERE question=?", (prompt,))
    db_answer = cursor.fetchone()

    if db_answer:
        answer = db_answer[0]
    else:
        langchain_response = agent_chain.run(prompt)
        answer = langchain_response['answer']
        cursor.execute("INSERT INTO questions (question, answer) VALUES (?, ?)", (prompt, answer))
        conn.commit()

    with st.chat_message("assistant"):
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# Close database
conn.close()
