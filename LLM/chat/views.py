import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import ChatHistory
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from django.conf import settings
from dotenv import load_dotenv
import os


load_dotenv()
CHROMA_PATH = settings.CHROMA_PATH
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

def generate_response_from_rag(query_text: str):
    """
    Funkcja generująca odpowiedź na podstawie zapytania, używając LangChain i OpenAI.
    """
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = PromptTemplate.from_template(""" 
    You are a helpful assistant answering questions based strictly on the provided context. 
    Provide a straight response. 
    If the answer to the question cannot be found in the context, do not reply or make anything up.

    Context:
    {context}

    ---

    Question:
    {question}

    """)

    prompt = prompt_template.format(context=context_text, question=query_text)

    # Generowanie odpowiedzi
    chat_model = ChatOpenAI(model="gpt-4o", temperature=0)
    response = chat_model.invoke(prompt)

    return response.content.strip()


@csrf_exempt
@api_view(['GET', 'POST'])
def generate_response_view(request):
    """
    Widok do generowania odpowiedzi na podstawie pytania użytkownika.
    """
    if request.method == 'GET':
        user_message = request.GET.get('message', '')
    elif request.method == 'POST':
        user_message = request.data.get('message', '')
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
    user_message = request.data.get('message', '')
    if user_message:
        response = generate_response_from_rag(user_message)

        # Zapisanie odpowiedź w historii
        chat_history = ChatHistory(user_message=user_message, model_response=response)
        chat_history.save()

        return JsonResponse({"response": response})

    return JsonResponse({"error": "No message provided"}, status=400)


@csrf_exempt
@api_view(['GET'])
def get_chat_history(request):
    """
    Endpoint do pobierania historii czatu.
    """
    session_key = request.session.session_key
    if session_key:
        chat_history = ChatHistory.objects.filter(session_id=session_key)
        history = [{"user_message": entry.user_message, "model_response": entry.model_response, "timestamp": entry.timestamp} for entry in chat_history]
        return JsonResponse({'history': history})

    return JsonResponse({'history': []})
