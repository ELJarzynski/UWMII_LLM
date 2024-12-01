# Chatbot for the Faculty of Mathematics and Computer Science

This is a small web application featuring a chatbot that provides answers to questions about the Faculty of Mathematics and Computer Science at the University of Warmia and Mazury. It is a Retrieval-Augmented Generation (RAG) system that processes PDFs and provides relevant answers to user questions based on the extracted content.
## Technologies Used
* **Backend:** Django 
* **Frontend:** Vue.js 
* **Language Model & API:** Powered by LangChain Open API and Ollama

### Dataset and Scope
The dataset used for the RAG system consists of PDFs that describe course syllabi from the University of Warmia and Mazury. Since this is a small project developed for coursework, it specifically includes data only for first semester.
## Installation

### Prerequisites
Make sure you have Docker installed on your machine.

### Setting Up the Backend

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   cd LLM
2. **Build and run the Docker containers:**
   ```bash
   docker-compose up --build

### Ensuring Open API conectivity
To make sure the app is running as it should be. Go to [OpenAi](https://platform.openai.com/api-keys) Log in and create api key for free then paste it in your Django settings file (`settings.py`) or  (`.env`)