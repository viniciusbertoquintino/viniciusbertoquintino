# Agents Design — Arquitetura dos Agentes

## Padrão de implementação

Todos os agentes seguem o padrão **ReAct simplificado**:
1. Recebem input do usuário
2. Opcionalmente consultam o RAG para contexto
3. Executam raciocínio estruturado via LLM
4. Retornam output em JSON com steps

## Agent 1 — Document Analyst

**Responsabilidades:**
- Resumir documentos longos
- Extrair pontos-chave e action items
- Identificar riscos e cláusulas problemáticas
- Gerar FAQ automático

**Input:** Texto do documento ou nome do documento indexado
**Output:** `{ summary, key_points[], risks[], faq[], action_items[] }`

## Agent 2 — Ticket Assistant

**Responsabilidades:**
- Analisar texto do chamado
- Consultar políticas via RAG
- Classificar prioridade (Alta/Média/Normal/Baixa)
- Identificar área responsável
- Sugerir resposta ao cliente

**Input:** Texto do chamado de suporte
**Output:** `{ priority, area, category, steps[], suggested_response, sla_hours }`

## Agent 3 — Workflow Planner

**Responsabilidades:**
- Decompor solicitação em etapas sequenciais
- Acionar ferramentas simuladas (calculate, classify, search)
- Gerar plano de ação com próximos passos

**Input:** Descrição de solicitação complexa
**Output:** `{ objective, steps[], tools_called[], recommended_action, estimated_completion }`

## Extensão para LangGraph (V2)

Para adicionar loops e memória de curto prazo:

```python
from langgraph.graph import StateGraph, END

def build_ticket_agent():
    graph = StateGraph(TicketState)
    graph.add_node("search_policy", search_policy_node)
    graph.add_node("calculate", calculate_node)
    graph.add_node("classify", classify_node)
    graph.add_node("respond", respond_node)
    
    graph.add_edge("search_policy", "calculate")
    graph.add_edge("calculate", "classify")
    graph.add_edge("classify", "respond")
    graph.add_edge("respond", END)
    
    return graph.compile()
```
