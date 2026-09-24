# Newsletter Financeira com Agno

Agente automatizado que pesquisa notícias financeiras, gera resumo com LLM e envia por email usando o framework Agno.

> Status: scripts funcionais — evolução incremental pelo [`ROADMAP.md`](./ROADMAP.md).

## O que este projeto prova

- integração Agno com OpenAI e Tavily para conteúdo financeiro;
- pipeline de pesquisa + geração + envio de email;
- automação de newsletter financeira;
- base para evolução com testes e agendamento.

## O que **não** é

- Consultoria financeira regulada
- Plataforma de investimentos ou trading
- Serviço de assessoria financeira

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Newsletter Financeira com Agno |
| ID prefixo | NF |
| Status | Scripts funcionais (em evolução) |
| Última etapa concluída | NF.01 — scripts Agno |
| Próxima etapa | NF.02 — `pyproject.toml` e `uv` |
| Superfície | Scripts Python |

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md): Base, Pipeline, Qualidade, Produção.

## Estrutura

```
newsletter-financeira-agno/
├── 01.agente.py           # Agente Agno
├── 02.email_tool.py       # Ferramenta de envio de email
├── 03.news_financeira.py  # Pipeline de newsletter
├── prompt.py              # Prompts do agente
└── requirements.txt
```

## Pré-requisitos

- Python 3.8+
- Chaves: OpenAI API, Tavily API, credenciais SMTP

## Instalação

```bash
git clone https://github.com/viniciusbertoquintino/newsletter-financeira-agno.git
cd newsletter-financeira-agno
pip install -r requirements.txt
```

Copie `.env.example` e configure as variáveis.

## Execução

```bash
python 01.agente.py           # Testar agente
python 03.news_financeira.py  # Pipeline completo
```

## Stack

- Python, Agno, OpenAI, Tavily, python-dotenv
