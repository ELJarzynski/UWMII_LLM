import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import ChatHistory
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.prompts import ChatPromptTemplate
from django.conf import settings


CHROMA_PATH = settings.CHROMA_PATH

# Funkcja generująca odpowiedź z modelu Ollama
def generate_response_from_rag(query_text: str):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OllamaEmbeddings(model="nomic-embed-text"))
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template("""
    You are a helpful assistant answering questions based strictly on the provided context. 
    Provide a detailed and well-explained response, including examples if possible. 
    If the answer to the question cannot be found in the context, do not reply or make anything up.

    Context:
    {context}

    ---

    Question:
    {question}

    Detailed Answer:
    """)

    prompt = prompt_template.format(context=context_text, question=query_text)

    model = OllamaLLM(model="mistral:latest", use_gpu=True)
    response_text = model.invoke(prompt)

    return response_text


@csrf_exempt
@api_view(['GET', 'POST'])
def generate_response_view(request):
    """
    Widok do generowania odpowiedzi na podstawie pytania użytkownika.
    """
    if request.method == 'GET':
        user_message = request.GET.get('message', '')  # Pobierz z URL dla GET
    elif request.method == 'POST':
        user_message = request.data.get('message', '')  # Pobierz z treści dla POST
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)

    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)

    try:
        response = generate_response_from_rag(user_message)
        return JsonResponse({"response": response})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@api_view(['POST'])
def send_message(request):
    """
    Endpoint do wysyłania wiadomości od użytkownika.
    """
    user_message = request.data.get('message', '')  # Pobierz wiadomość z frontendu
    if user_message:
        # Generowanie odpowiedzi na podstawie zapytania
        response = generate_response_from_rag(user_message)

        # Zapisz odpowiedź w historii
        chat_history = ChatHistory(user_message=user_message, model_response=response)
        chat_history.save()

        return JsonResponse({"response": response})

    return JsonResponse({"error": "No message provided"}, status=400)


@csrf_exempt
@api_view(['GET'])
def get_chat_history(request):
    """
    Endpoint do pobierania historii rozmów.
    """
    chat_history = ChatHistory.objects.all()
    history = [{"user_message": entry.user_message, "model_response": entry.model_response, "timestamp": entry.timestamp} for entry in chat_history]
    return JsonResponse({'history': history})


# Funkcja do obliczania identyfikatorów chunków
def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks

"""-----------------------------Database and pdf loader--------------------------------------------------"""
# Function to load PDFs into Chroma database
def load_documents_and_add_to_chroma():
    document_loader = PyPDFDirectoryLoader("../../RAG/data")
    documents = document_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OllamaEmbeddings(model="nomic-embed-text"))
    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if new_chunks:
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()


@csrf_exempt  # Disable CSRF for testing purposes; consider adding proper CSRF handling
def load_pdf(request):
    if request.method == 'POST':
        # Handle the PDF upload logic here
        return JsonResponse({'message': 'PDF uploaded successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
