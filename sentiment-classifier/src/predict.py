from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch
import sys

# Verifica se o texto foi passado como argumento
if len(sys.argv) < 2:
    print("Uso: python predict.py \"Texto para análise de sentimento\"")
    sys.exit(1)

# Texto de entrada
input_text = sys.argv[1]

# Carrega o modelo e o tokenizer treinados
model_path = "sentiment_model"
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)

# Tokeniza o texto
inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)

# Faz a predição
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()

# Mapeia o resultado para sentimento
sentiment = "Positivo" if predicted_class == 1 else "Negativo"

# Exibe o resultado
print(f"Texto: {input_text}")
print(f"Sentimento previsto: {sentiment}")
