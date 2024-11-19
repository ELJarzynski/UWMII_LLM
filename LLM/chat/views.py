from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatHistory
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings


chat_history = []

def get_chat_history(request):
    if request.method == 'GET':
        return JsonResponse({'history': chat_history})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

# Inicjalizacja modelu
MODEL = 'llama-3.1-70b-versatile'
api_key = settings.GROQ_API_KEY
llm = ChatGroq(model=MODEL, api_key=api_key, temperature=0)

# Szablon zapytania
default_prompt = ChatPromptTemplate.from_messages([
    ("system", "Jesteś pomocnym asystentem. Odpowiadaj wyłącznie w języku polskim."),
    ("human", "{message}")
])

chat_chain = default_prompt | llm | StrOutputParser()

# Zmienna do przechowywania wiadomości
current_user_message = None

@csrf_exempt
@api_view(['POST'])
def send_message(request):
    """
    Endpoint do wysyłania wiadomości od użytkownika.
    """
    global current_user_message

    if request.method == 'POST':
        user_message = request.data.get('message', '')  # Pobierz wiadomość z frontendu
        if user_message:
            # Zapisz wiadomość
            current_user_message = user_message
            return JsonResponse({"message": "Message received. Use '/get-response/' to get the response."})
        return JsonResponse({"error": "No message provided"}, status=400)

@csrf_exempt
@api_view(['GET'])
def get_response(request):
    """
    Endpoint do pobierania odpowiedzi na zapytanie od bota.
    """
    global current_user_message

    if current_user_message:
        try:
            response = chat_chain.invoke({"message": current_user_message})  # Odpowiedź modelu

            # Zapisz odpowiedź i wiadomość w historii
            chat_history = ChatHistory(user_message=current_user_message, model_response=response)
            chat_history.save()

            # Wyczyszczenie wiadomości po uzyskaniu odpowiedzi
            current_user_message = None

            return JsonResponse({"response": response})  # Zwróć odpowiedź modelu
        except Exception as e:
            return JsonResponse({"error": f"Error: {str(e)}"}, status=500)

    return JsonResponse({"error": "No message to respond to."}, status=400)
