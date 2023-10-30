# Welcome to BearChat: Bridgewater State University's FAQ Bot

BearChat is a Streamlit-based FAQ bot designed to assist students with inquiries about Bridgewater State University. Utilizing Langchain and OpenAI's GPT-3, the bot provides real-time, context-aware answers.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Steps

1. Clone this repository to your local machine.
   
```bash
git clone <repository_url>
```

2. Install the required Python packages:

```bash
pip install streamlit
```

## Usage

Run the Streamlit app with the following command:

```bash
streamlit run bearchat.py
```

A URL will appear in your terminal. Open this URL in a web browser to interact with the bot.

## How It Works

1. The Streamlit interface prompts you to enter your query.
2. Your query is processed by an agent initialized via Langchain.
3. The agent utilizes OpenAI's GPT-3 for generating a context-aware response.

## Features

- User-friendly Streamlit interface
- Context-aware responses via OpenAI's GPT-3
- Modular design powered by Langchain

## Tech Stack

- **Streamlit**: Web interface
- **Langchain**: Agent initialization and management
- **OpenAI's GPT-3**: Chat model for generating responses

## License

This project is open-source and available under the [MIT License](LICENSE).