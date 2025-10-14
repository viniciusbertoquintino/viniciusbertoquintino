from datasets import load_dataset
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
import torch

# Carregar o dataset IMDb
dataset = load_dataset("imdb")

# Carregar o tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

# Tokenizar os dados
def tokenize_function(example):
    return tokenizer(example["text"], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Preparar para PyTorch
tokenized_datasets.set_format("torch", columns=["input_ids", "attention_mask", "label"])

# Carregar o modelo
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# Definir argumentos de treinamento
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    load_best_model_at_end=True,
    logging_steps=100,
)

# Criar o Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# Treinar o modelo
trainer.train()

# Salvar o modelo
model.save_pretrained("sentiment_model")
tokenizer.save_pretrained("sentiment_model")

print("Modelo treinado e salvo em 'sentiment_model'.")
