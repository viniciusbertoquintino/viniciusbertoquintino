
import streamlit as st
from agente_reembolso import criar_agente, processar_pergunta

# Função para tratar a resposta antes de mostrar
def tratar_resposta(resposta):
    
    # Converte para string se necessário
    texto = str(resposta)
    
    # Exemplo 1: Adiciona emoji no início se não tiver
    if not texto.startswith(('💰', '🤖', '✅', '❌', '⚠️')):
        texto = "🤖 " + texto
    
    # Exemplo 2: Destaca valores em reais
    import re
    texto = re.sub(r'R\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', r'**R$ \1**', texto)
    
    # Exemplo 3: Formata listas (sem quebrar linhas desnecessariamente)
    # texto = texto.replace('- ', '\n- ')  # Comentado para evitar quebras desnecessárias
    
    # Exemplo 4: Personaliza mensagens de erro
    if "erro" in texto.lower() or "error" in texto.lower():
        texto = f"❌ **Ops!** {texto}"
    
    return texto


# Configurações iniciais da página


st.set_page_config(
    page_title="Assistente de Reembolso",
    page_icon="💰",
    layout="centered"
)


# Titulo e descrição

st.title("💰 Assistente de Reembolso")
st.markdown("Olá! Sou seu assistente virtual. Pergunte sobre a política de reembolso!")


# Barra lateral


with st.sidebar:
    st.header("ℹ️ Como usar")
    st.markdown("""
    **Você pode perguntar:**
    - Qual o prazo para pedir reembolso?
    - Como funciona o reembolso por defeito?
    - Calcule reembolso de R$ 500
    - Preciso de nota fiscal?
    
    **O agente tem:**
    - ✅ Memória automática (lembra da conversa)
    - ✅ RAG com base de conhecimento
    - ✅ Calculadora de reembolso
    """)
    
    st.divider()
    
    # Botão para limpar conversa
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.mensagens = []
        st.rerun()

# INICIALIZAR O AGENTE

# Inicializa a lista de mensagens
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Cria o agente (só uma vez)
if "agente" not in st.session_state:
    with st.spinner("Iniciando assistente..."):
        try:
            st.session_state.agente = criar_agente()
            st.success("✅ Assistente pronto!", icon="🤖")
        except Exception as e:
            st.error(f"❌ Erro ao criar agente: {str(e)}")
            st.stop()


# Mostra o histórico de mensagens

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Campo de input do usuário

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
                # Chama o agente (ele já tem memória integrada)
                resposta = processar_pergunta(
                    st.session_state.agente, 
                    pergunta,
                    user_id="usuario_streamlit"
                )
                
                # Trata a resposta antes de mostrar
                resposta_tratada = tratar_resposta(resposta)
                # Mostra a resposta tratada
                st.markdown(resposta_tratada)
                
                # Adiciona resposta tratada ao histórico visual
                st.session_state.mensagens.append({
                    "role": "assistant",
                    "content": resposta_tratada
                })
                
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")


# RODAPÉ

st.divider()
st.caption("🤖 Assistente de Reembolso")
