# Chatbot for the Faculty of Mathematics and Computer Science

### This is a small web application featuring a chatbot that provides answers to questions about the Faculty of Mathematics and Computer Science at the University of Warmia and Mazury.
## Technologies Used
* **Backend:** Django 
* **Frontend:** Vue.js 
* **Language Model & API:** Powered by LangChain with Groq integration

### Dataset and Scope
The dataset used to train the LLM was created by scraping content from [http://wmii.uwm.edu.pl/](http://wmii.uwm.edu.pl/). Since this is a small project developed for coursework, it includes data specifically from the [Students' page](http://wmii.uwm.edu.pl/studenci)

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

### Ensuring Groq API conectivity
To make sure the app is running as it should be. Go to [Groq Page](https://console.groq.com/keys) Log in and create api key for free then paste it in your Django settings file (`settings.py`) 