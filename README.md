# Welcome to the Bridgewater State University FAQ Bot!
#BearChat

This project is a specialized Streamlit application that uses Langchain and Playwright to answer student questions about `bridgew.edu`. The application also features a SQLite database to store previously answered questions, reducing the need for repeated site scraping.

## Installation

First, clone the repository to your local machine.

### Prerequisites

Install the necessary Python packages:

```bash
pip install playwright streamlit sqlite
```

Then, install a Playwright browser:

```bash
playwright install
```

## Usage

To start the Streamlit app, run:

```bash
streamlit run bearchat.py
```

Open the URL displayed in your terminal to access the Streamlit interface.

### How to Use

1. The Streamlit app will prompt you to enter a question about `bridgew.edu`.
2. Click the 'Submit' button to get the answer.
3. The application will first check the SQLite database for a previously stored answer. If found, it will display the answer from the database.
4. If the question is new, the Langchain agent will use Playwright tools to scrape or interact with the `bridgew.edu` site to find the answer.
5. The new question and its answer will be stored in the SQLite database for future queries.

## Features

- Streamlit interface for ease of use
- Langchain agent with Playwright tools for web interactions
- SQLite database to store and retrieve previous queries

## Status
- [x] Streamlit interface
- [x] Langchain agent
- [x] Playwright tools
- [x] SQLite database
- [ ] Docker container


## Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

## License

This project is open-source and available under the [MIT License](LICENSE).

