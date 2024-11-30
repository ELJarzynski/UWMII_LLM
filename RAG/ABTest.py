import time
from OpenAI import query_rag as openai_query
from Ollama import query_rag as ollama_query

# The query we want to test with both models
query_text = "Number of hours per semester for databases"

# Measure time and get response from Ollama
start_time_ollama = time.time()
response_ollama = ollama_query(query_text)
end_time_ollama = time.time()
ollama_time = end_time_ollama - start_time_ollama

# # Measure time and get response from OpenAI
# start_time_openai = time.time()
# response_openai = openai_query(query_text)
# end_time_openai = time.time()
# openai_time = end_time_openai - start_time_openai

print(f"Ollama Response: {response_ollama}")
print(f"Ollama Response Time: {ollama_time:.4f} seconds")

# # Print the results
# print(f"OpenAI Response: {response_openai}")
# print(f"OpenAI Response Time: {openai_time:.4f} seconds\n")