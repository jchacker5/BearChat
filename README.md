# Welcome to BearChat: Bridgewater State University's AI Assistant

BearChat is a Streamlit-based AI assistant that uses OpenAI's GPT-4 and Langchain to provide students with timely, accurate, and engaging information about Bridgewater State University. This project was built as a senior design directed-study project by Joseph Defendre. 

## Installation

Ensure you have Python 3.7 or higher and pip installed on your system.

### Steps

1. **Clone the Repository**
   Download the code to your local machine using the following command:

   ```bash
   git clone https://github.com/your-username/BearChat.git
   ```

2. **Set Up a Virtual Environment (Optional)**
   Create and activate a virtual environment to manage dependencies:

   ```bash
   python -m venv bearchat-env
   source bearchat-env/bin/activate  # On Windows, use `bearchat-env\Scripts\activate`
   ```

3. **Install Dependencies**
   Navigate to the cloned repository and install the necessary packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Environmental Variables**
   Set your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

   Replace `'your-api-key'` with your actual OpenAI API key.

## Usage

Run the Streamlit app with the following command from within the repository directory:

```bash
streamlit run bearchat.py
```

Navigate to the URL provided in your terminal to start using BearChat.

## How It Works

1. Enter your query in the Streamlit interface.
2. BearChat's Langchain-initialized agent processes your query.
3. OpenAI's GPT-4 generates a response based on the context provided.

## Features

- Intuitive Streamlit interface for easy user interactions.
- Advanced and contextually aware responses powered by OpenAI's GPT-4.
- Customizable and scalable architecture via Langchain.
- incorporates data directly form the school's Website in its knowledge. 

## Tech Stack

- **Streamlit**: For the web interface.
- **Langchain**: To initialize and manage the chatbot agent.
- **OpenAI's GPT-4**: As the AI model for generating responses.

## License

This project is open-source and distributed under the [MIT License](LICENSE).
