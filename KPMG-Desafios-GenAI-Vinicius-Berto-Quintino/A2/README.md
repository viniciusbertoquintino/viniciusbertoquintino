# 🤖 Sistema Multi-Agentes: Redator · Crítico · Editor

## 📋 Descrição do Desafio

Criar um sistema multi-agentes onde:

- **3 papéis**: Redator, Crítico e Editor
- **Objetivo**: Produzir um comunicado claro sobre reembolsos para reduzir contatos do suporte N1
- **Máximo 2 rodadas** (com regras de parada)
- **DoD (Definition of Done)**: Críticas devem apontar fonte; texto final consistente e factual

---

## 🎯 Como Funciona (Explicação Simples)

### Analogia: Como uma redação de jornal

Imagine que você está em uma redação de jornal:

1. **Redator** → Escreve a primeira versão da notícia
2. **Crítico** → Lê e aponta problemas ("Essa frase está confusa", "Falta informação aqui")
3. **Editor** → Pega tudo e produz a versão final para publicação

### Fluxo Visual

```
┌─────────┐       ┌─────────┐       ┌─────────┐
│ REDATOR │  -->  │ CRÍTICO │  -->  │ EDITOR  │
└─────────┘       └─────────┘       └─────────┘
    ↓                 ↓                 ↓
 Escreve          Analisa           Finaliza
 rascunho        + aponta          versão OK
                 problemas
```

---

## 🔧 Estrutura do Código (Parte por Parte)

### Parte 1️⃣: Imports

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
```

**O que faz?** Importa as ferramentas necessárias do Agno (biblioteca de agentes IA).

---

### Parte 2️⃣: Criar o Agente Redator

```python
redator = Agent(
    name="Redator",
    model=OpenAIChat("gpt-4o"),
    role="Especialista em redação...",
    instructions="Você é um redator..."
)
```

**O que faz?**

- Cria um agente chamado "Redator"
- Usa GPT-4o como "cérebro"
- Define as **instruções** (como se fosse um manual de treinamento)

**Analogia**: É como contratar um funcionário e dar o manual de instruções dele.

---

### Parte 3️⃣: Criar o Agente Crítico

```python
critico = Agent(
    name="Crítico",
    instructions="Verificar clareza, completude, ambiguidades..."
)
```

**O que faz?**

- Cria um agente que **analisa** o texto do Redator
- Sempre cita a **fonte** do problema (qual frase tem erro)
- Usa emojis para deixar visual: ❌ (problema), ✅ (aprovado)

**Regra importante**: O Crítico SEMPRE deve dizer DE ONDE veio o problema!

---

### Parte 4️⃣: Criar o Agente Editor

```python
editor = Agent(
    name="Editor",
    instructions="Produzir versão final corrigindo problemas..."
)
```

**O que faz?**

- Recebe o texto inicial + as críticas
- Corrige tudo
- Produz a **versão final** pronta para publicar

---

### Parte 5️⃣: Função Principal (Orquestração)

```python
def executar_sistema_multiagentes():
    # 1. Redator escreve
    resposta_redator = redator.run(solicitacao_inicial)
  
    # 2. Crítico analisa
    resposta_critico = critico.run(texto_do_redator)
  
    # 3. Editor finaliza
    resposta_editor = editor.run(texto_inicial + criticas)
```

**O que faz?**

- **Orquestra** (coordena) os 3 agentes em sequência
- Cada agente recebe o que precisa e produz sua saída
- `.run()` = "execute sua tarefa"

**Analogia**: É como um maestro regendo uma orquestra - cada músico (agente) toca na hora certa.

---

## 🚀 Como Executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Rodar o programa

```bash
python multiagente.py
```

---

## 📊 Exemplo de Saída

```
🚀 INICIANDO SISTEMA MULTI-AGENTES
===============================================

📝 ETAPA 1: Redator escrevendo comunicado inicial...
-----------------------------------------------
[Texto do comunicado...]

🔍 ETAPA 2: Crítico analisando o comunicado...
-----------------------------------------------
❌ Problema: Prazo não especificado claramente
📍 Fonte: "Entre em contato para reembolso"

✍️ ETAPA 3: Editor produzindo versão final...
-----------------------------------------------
📢 COMUNICADO OFICIAL - POLÍTICA DE REEMBOLSOS
[Versão final corrigida...]

✅ SISTEMA MULTI-AGENTES CONCLUÍDO COM SUCESSO!
```

---

## 🎓 Conceitos-Chave para Iniciantes

### O que é um Agente?

Um agente é como um "funcionário virtual" que:

- Tem um **papel** específico (Redator, Crítico, Editor)
- Recebe **instruções** de como trabalhar
- Usa IA para **tomar decisões** e produzir resultados

### Por que 3 agentes em vez de 1?

**Divisão de responsabilidades!**

- Redator foca em **criar** conteúdo
- Crítico foca em **encontrar** problemas
- Editor foca em **corrigir** e finalizar

É mais eficiente que 1 agente tentando fazer tudo.

### O que significa "2 rodadas máx."?

- **Rodada 1**: Redator → Crítico → Editor = 1 ciclo completo
- **Rodada 2**: Se necessário, repetir (mas limitamos para não ficar infinito)

No código atual, usamos apenas 1 rodada (suficiente para maioria dos casos).

### Como funciona a "regra de parada"?

O Crítico pode dizer:

- ✅ "Aprovado sem ressalvas" → Para aqui, está OK!
- ❌ "Tem problemas..." → Editor corrige e finaliza

---

## 🔍 Atendimento ao DoD

✅ **Críticas apontam fonte**: O Crítico sempre cita o trecho problemático
✅ **Texto final consistente**: Editor corrige todas as inconsistências
✅ **Texto final factual**: Baseado nas informações fornecidas (sem inventar dados)
✅ **Máximo 2 rodadas**: Sistema implementa em 1 rodada (pode expandir se necessário)

---

## 💡 Melhorias Futuras (Opcional)

1. **Implementar 2ª rodada**: Adicionar loop se Crítico reprovar
2. **Salvar histórico**: Guardar todas as versões em arquivo
3. **Interface web**: Criar dashboard para visualizar o processo
4. **Métricas**: Contar quantos problemas foram corrigido
5.

**Desenvolvido por Vinicius com bastante dedicação. Foram exploradas diferentes abordagens de IA para mostrar que não existe uma solução única — tudo depende do contexto específico de cada problema.**