# Sentiment Classifier com Hugging Face 🤖

Este projeto utiliza modelos pré-treinados da Hugging Face para classificar sentimentos em textos (positivo, negativo ou neutro). O modelo é baseado no DistilBERT e foi treinado no dataset IMDb para análise de sentimentos.

## 📦 Tecnologias

- **Python 3.8+**
- **Hugging Face Transformers** - Para modelos de linguagem
- **PyTorch** - Framework de deep learning
- **Dataset IMDb** - Dados de treinamento via Hugging Face Datasets
- **Scikit-learn** - Para métricas e avaliação
- **Streamlit** - Interface web interativa

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/viniciusbertoquintino/viniciusbertoquintino.git
cd AI-Projects/sentiment-classifier
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Treine o modelo

```bash
python src/train_model.py
```

Este comando irá:
- Baixar o dataset IMDb
- Treinar o modelo DistilBERT
- Salvar o modelo treinado na pasta `sentiment_model`

### 4. Faça previsões via linha de comando

```bash
python src/predict.py "Esse filme foi incrível!"
```

### 5. Interface web interativa

```bash
streamlit run app/app.py
```

Acesse `http://localhost:8501` no seu navegador para usar a interface web.

## 📁 Estrutura do projeto

```
sentiment-classifier/
├── app/
│   └── app.py              # Interface Streamlit
├── src/
│   ├── train_model.py      # Script de treinamento
│   └── predict.py          # Script de predição
├── requirements.txt        # Dependências
└── README.md              # Este arquivo
```

## 🎯 Como usar

1. **Treinamento**: Execute `train_model.py` para treinar o modelo
2. **Predição via CLI**: Use `predict.py` com um texto como argumento
3. **Interface Web**: Execute `streamlit run app/app.py` para uma interface amigável

## 📊 Exemplos de uso

```python
# Exemplo de texto positivo
python src/predict.py "Este filme é fantástico! Recomendo muito!"

# Exemplo de texto negativo  
python src/predict.py "Que filme terrível, perdi meu tempo."
```

## 🔧 Requisitos

- Python 3.8 ou superior
- 4GB+ de RAM recomendado
- Conexão com internet (para download do modelo e dataset)

## 📝 Notas

- O modelo é salvo na pasta `sentiment_model` após o treinamento
- A primeira execução pode demorar devido ao download dos dados
- O modelo suporta textos em inglês (baseado no dataset IMDb)