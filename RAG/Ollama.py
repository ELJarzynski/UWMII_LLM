import os
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM, OllamaEmbeddings

CHROMA_PATH = "ollama_database"

PROMPT_TEMPLATE = """
You are a helpful assistant answering questions based strictly on the provided context. 
Provide a detailed and well-explained response, including examples if possible. 
If the answer to the question cannot be found in the context, do not reply or make anything up.

Context:
{context}

---

Question:
{question}

Detailed Answer:
"""


# Funkcja do tworzenia embeddingów za pomocą Ollama
def embedding_fun():
    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")  # Embedding model
    return embeddings

# Funkcja przygotowująca bazę danych (Chroma)
def prepare_db(embedding_function):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    return db

# Funkcja wykonująca zapytanie na bazie danych i zwracająca wyniki
def search_db(db, query_text, k=5):
    results = db.similarity_search_with_score(query_text, k)
    return results

# Funkcja generująca odpowiedź za pomocą modelu Ollama
def generate_response(results, query_text):
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Użycie modelu z Ollama
    model = OllamaLLM(model="llama3.2:latest", use_gpu=True)   # Generative model
    response_text = model.invoke(prompt)

    return response_text

# Główna funkcja zapytania RAG
def query_rag(query_text: str):
    # Przygotowanie bazy danych
    embedding_function = embedding_fun()
    db = prepare_db(embedding_function)

    # Wyszukiwanie w bazie danych
    results = search_db(db, query_text)

    # Generowanie odpowiedzi
    response_text = generate_response(results, query_text)

    # Formatowanie i wyświetlanie odpowiedzi
    formatted_response = f"Response: {response_text}"
    return formatted_response


if __name__ == "__main__":
    print(query_rag("Number of ects points for databases"))
