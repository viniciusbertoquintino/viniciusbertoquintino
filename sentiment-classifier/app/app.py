import streamlit as st
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch

# Carregar o modelo e o tokenizer
model_path = "sentiment_model"
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)

# Título do app
st.title("Classificador de Sentimentos com IA 🤖")
st.write("Digite um texto abaixo e veja se o sentimento é positivo ou negativo.")

# Entrada de texto
user_input = st.text_area("Texto para análise", "")

# Botão de predição
if st.button("Analisar Sentimento"):
    if user_input.strip() == "":
        st.warning("Por favor, digite um texto para análise.")
    else:
        # Tokenizar entrada
        inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)

        # Fazer predição
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=1).item()

        # Interpretar resultado
        sentiment = "Positivo 😊" if predicted_class == 1 else "Negativo 😞"
        st.success(f"Sentimento previsto: {sentiment}")
