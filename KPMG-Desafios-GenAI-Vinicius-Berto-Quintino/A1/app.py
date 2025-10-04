"""
Interface Streamlit para o Agente de Reembolso
Com Sistema de Memória (Curto Prazo + Sessão)
"""
import streamlit as st
import json
from datetime import datetime
from agente_reembolso import criar_agente, processar_pergunta  # type: ignore
from memoria import MemoriaAgente  # type: ignore

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
    
    **O agente tem:**
    - ✅ Memória de curto prazo (últimas 10 msgs)
    - ✅ Histórico completo da sessão
    - ✅ RAG com base de conhecimento
    """)
    
    st.divider()
    
    # Mostra estatísticas da memória
    if "memoria" in st.session_state:
        st.subheader("📊 Estatísticas")
        memoria = st.session_state.memoria
        st.metric("Buffer", f"{len(memoria.memoria_curto_prazo)}")
        st.metric("Sessão", len(memoria.memoria_sessao))
    
    st.divider()
    
    # Botão para limpar conversa
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.mensagens = []
        if "memoria" in st.session_state:
            st.session_state.memoria.limpar_tudo()
        st.rerun()
    
    # Botão para baixar sessão
    if st.button("📥 Baixar Sessão"):
        if "memoria" in st.session_state:
            historico = st.session_state.memoria.obter_historico_completo()
            sessao_json = json.dumps(historico, indent=2, ensure_ascii=False)
            st.download_button(
                label="⬇️ Clique para baixar",
                data=sessao_json,
                file_name=f"sessao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# ========================================
# INICIALIZAR O AGENTE E MEMÓRIA
# ========================================

# Inicializa a lista de mensagens (memória da conversa)
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Inicializa a memória do agente
if "memoria" not in st.session_state:
    st.session_state.memoria = MemoriaAgente(limite_curto_prazo=10)

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
                # Chama o agente COM MEMÓRIA para processar a pergunta
                resposta = processar_pergunta(
                    st.session_state.agente, 
                    pergunta,
                    memoria=st.session_state.memoria  # Passa a memória!
                )
                
                # Mostra a resposta
                st.markdown(resposta)
                
                # Adiciona resposta ao histórico visual
                st.session_state.mensagens.append({
                    "role": "assistant",
                    "content": resposta
                })
                
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")

# ========================================
# RODAPÉ
# ========================================

st.divider()
st.caption("🤖 Assistente com Memória | Agno + Streamlit | RAG + Knowledge Base")
