# Chatbot for the Faculty of Mathematics and Computer Science

This is a small web application featuring a chatbot that provides answers to questions about the Faculty of Mathematics and Computer Science at the University of Warmia and Mazury. It is a Retrieval-Augmented Generation (RAG) system that processes PDFs and provides relevant answers to user questions based on the extracted content.
## Technologies Used
* **Backend:** Django 
* **Frontend:** Vue.js 
* **Language Model & API:** Powered by LangChain Open API and Ollama

### Dataset and Scope
The dataset used for the RAG system consists of PDFs that describe course syllabi from the University of Warmia and Mazury. Since this is a small project developed for coursework, it specifically includes data only for courses from first semester.
## Installation

### Prerequisites
Make sure you have Docker installed on your machine.

### Setting Up

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   cd LLM
2. **Build and run the Docker containers:**
   ```bash
   docker-compose up --build

## Ensuring Connectivity

To ensure the app runs correctly, follow these steps based on your usage type:

1. **Choose your usage option:**
   - **For slow but free usage**, switch to the `ollama` branch.
   - **For paid usage**, stay on the `master` branch.

2. **Create your `.env` file** in the Django project.

3. **Upload PDF's and change directory `database` folder to `chat` folder**.

   - **For free usage:** Load PDF files using `PDF_ollama_loader.py`.
   - **For paid usage:** Load PDF files using `PDF_openai_loader.py`.
4. **Load PDF files**
5. **For free usage:**
   - Install [Ollama](https://ollama.com) on your device and install the `mistral:latest` model.

6. **For paid usage:**
   - Go to [OpenAI](https://platform.openai.com/api-keys), log in, create an API key, and paste it into your Django `.env` file.
![alt table](https://github.com/ELJarzynski/UWMII_LLM/blob/master/images/Intro.png)