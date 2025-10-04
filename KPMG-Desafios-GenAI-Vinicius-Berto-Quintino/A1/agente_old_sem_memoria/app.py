"""
Interface Streamlit para o Agente de Reembolso

"""
import streamlit as st
import json
from datetime import datetime
from agente_reembolso import criar_agente, processar_pergunta  # type: ignore

# ========================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================

st.set_page_config(
    page_title="Assistente de Reembolso",
    page_icon="💰",
    layout="centered"
)

# ========================================
# TÍTULO E DESCRIÇÃO
# ========================================

st.title("💰 Assistente de Reembolso")
st.markdown("Olá! Sou seu assistente virtual. Pergunte sobre a política de reembolso!")

# ========================================
# BARRA LATERAL (SIDEBAR)
# ========================================

with st.sidebar:
    st.header("ℹ️ Como usar")
    st.markdown("""
    **Você pode perguntar:**
    - Qual o prazo para pedir reembolso?
    - Como funciona o reembolso por defeito?
    - Calcule reembolso de R$ 500
    - Preciso de nota fiscal?
    
    **O agente pode:**
    - ✅ Responder suas dúvidas
    - ✅ Calcular reembolsos
    - ✅ Citar a política
    """)
    
    st.divider()
    
    # Botão para limpar conversa
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.mensagens = []
        st.session_state.logs = []
        st.rerun()
    
    # Botão para baixar logs
    if st.button("📥 Baixar Logs"):
        if "logs" in st.session_state and st.session_state.logs:
            logs_json = json.dumps(st.session_state.logs, indent=2, ensure_ascii=False)
            st.download_button(
                label="⬇️ Clique para baixar",
                data=logs_json,
                file_name=f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# ========================================
# INICIALIZAR O AGENTE E MEMÓRIA
# ========================================

# Inicializa a lista de mensagens (memória da conversa)
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Inicializa a lista de logs
if "logs" not in st.session_state:
    st.session_state.logs = []

# Função para criar o agente com cache (para evitar recriação desnecessária)
@st.cache_resource
def criar_agente_cache():
    return criar_agente()

# Cria o agente (só uma vez)
if "agente" not in st.session_state:
    with st.spinner("Iniciando assistente..."):
        try:
            st.session_state.agente = criar_agente()
            st.success("✅ Assistente pronto!", icon="🤖")
        except Exception as e:
            st.error(f"❌ Erro ao criar agente: {str(e)}")
            st.stop()

# ========================================
# MOSTRAR HISTÓRICO DE MENSAGENS
# ========================================

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================================
# CAMPO DE INPUT DO USUÁRIO
# ========================================

if pergunta := st.chat_input("Digite sua pergunta aqui..."):
    
    # Adiciona a pergunta do usuário ao histórico
    st.session_state.mensagens.append({
        "role": "user",
        "content": pergunta
    })
    
    # Mostra a pergunta do usuário
    with st.chat_message("user"):
        st.markdown(pergunta)
    
    # Processa e mostra a resposta do agente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Chama o agente para processar a pergunta
                resposta = processar_pergunta(st.session_state.agente, pergunta)
                
                # Mostra a resposta
                st.markdown(resposta)
                
                # Adiciona resposta ao histórico
                st.session_state.mensagens.append({
                    "role": "assistant",
                    "content": resposta
                })
                
                # Salva log estruturado
                log = {
                    "timestamp": datetime.now().isoformat(),
                    "pergunta": pergunta,
                    "resposta": resposta
                }
                st.session_state.logs.append(log)
                
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
                
                # Log de erro
                log_erro = {
                    "timestamp": datetime.now().isoformat(),
                    "pergunta": pergunta,
                    "erro": str(e)
                }
                st.session_state.logs.append(log_erro)

# ========================================
# RODAPÉ
# ========================================

st.divider()
st.caption("🤖 Assistente desenvolvido com Agno + Streamlit")
