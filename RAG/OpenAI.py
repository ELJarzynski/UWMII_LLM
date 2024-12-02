import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI


import os
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment")


def load_documents():
    document_loader = PyPDFDirectoryLoader("data")
    return document_loader.load()


def split_documents(documents: list[Document]):
    text_splitter = CharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def embedding_fun():
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)  # Przekazanie klucza API do OpenAI
    return embeddings


def prepare_db(embedding_function):
    db = Chroma(
        persist_directory="database",
        embedding_function=embedding_function
    )
    return db


def search_db(db, query_text):
    docs = db.similarity_search(query_text)
    return docs


def generate_response(results, query_text):
    chat_model = ChatOpenAI(model="gpt-4", temperature=0.5, api_key=openai_api_key)

    conversation_chain = load_qa_chain(chat_model, chain_type="stuff")
    response = conversation_chain.run(input_documents=results, question=query_text)
    return response


def query_rag(query_text: str):
    embedding_function = embedding_fun()
    db = prepare_db(embedding_function)

    results = search_db(db, query_text)
    response_text = generate_response(results, query_text)

    formatted_response = f"Response: {response_text}"
    return formatted_response


if __name__ == "__main__":
    print(query_rag("Number of ects points for databases"))
