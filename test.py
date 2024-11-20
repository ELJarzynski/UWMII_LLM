from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os


# Wczytanie modelu i tokenizera dla LLaMA
model_url = "meta-llama/Llama-3.2-3B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_url, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(model_url, use_auth_token=True)

# Załaduj dane z pliku JSONL
dataset = load_dataset("json", data_files="datatest.jsonl")

# Funkcja do preprocessingu danych
def preprocess(example):
    inputs = tokenizer(
        example["instruction"],
        truncation=True,
        padding="max_length",
        max_length=512
    )
    outputs = tokenizer(
        example["response"],
        truncation=True,
        padding="max_length",
        max_length=512
    )
    inputs["labels"] = outputs["input_ids"]
    return inputs

# Tokenizacja danych
tokenized_dataset = dataset.map(preprocess, batched=True)

# Argumenty treningowe
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    save_steps=10,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=10,
)

# Trener
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
)

# Rozpoczęcie treningu
trainer.train()

# Zapisanie wytrenowanego modelu
trainer.save_model("./results")
tokenizer.save_pretrained("./results")

# Załaduj wytrenowany model
model = LlamaForCausalLM.from_pretrained("./results")
tokenizer = LlamaTokenizer.from_pretrained("./results")

# Testowanie modelu
def ask_question(question, model, tokenizer):
    inputs = tokenizer(question, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=200)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Przykład pytania
question = input("Please ask me a question: ")
response = ask_question(question, model, tokenizer)
print(f"Response: {response}")
