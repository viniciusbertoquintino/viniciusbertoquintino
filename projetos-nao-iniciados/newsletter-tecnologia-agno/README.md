# Newsletter de Tecnologia com Agno

Agente automatizado que pesquisa notícias de tecnologia, gera resumo com LLM e envia por email usando o framework Agno.

> Status: scripts funcionais — evolução incremental pelo [`ROADMAP.md`](./ROADMAP.md).

## O que este projeto prova

- integração Agno com OpenAI e Tavily;
- pipeline de pesquisa + geração + envio de email;
- automação de newsletter de tecnologia;
- base para evolução com testes e agendamento.

## O que **não** é

- Plataforma de email marketing enterprise
- CMS de conteúdo ou blog
- Serviço SaaS de newsletters

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Newsletter de Tecnologia com Agno |
| ID prefixo | NT |
| Status | Scripts funcionais (em evolução) |
| Última etapa concluída | NT.01 — scripts Agno |
| Próxima etapa | NT.02 — `pyproject.toml` e `uv` |
| Superfície | Scripts Python |

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md): Base, Pipeline, Qualidade, Produção.

## Estrutura

```
newsletter-tecnologia-agno/
├── 01.agente.py        # Agente Agno com Tavily
├── 02.email_tool.py    # Ferramenta de envio de email
├── 03.news_tech.py     # Pipeline de newsletter
├── prompt.py           # Prompts do agente
└── requirements.txt
```

## Pré-requisitos

- Python 3.8+
- Chaves: OpenAI API, Tavily API, credenciais SMTP

## Instalação

```bash
git clone https://github.com/viniciusbertoquintino/newsletter-tecnologia-agno.git
cd newsletter-tecnologia-agno
pip install -r requirements.txt
```

Copie `.env.example` (quando disponível) e configure as variáveis.

## Execução

```bash
python 01.agente.py      # Testar agente
python 03.news_tech.py   # Pipeline completo
```

## Stack

- Python, Agno, OpenAI, Tavily, python-dotenv
