"""
Sistema de Memória para o Agente de Reembolso
==============================================

Este módulo implementa duas tipos de memória:
1. Memória de Curto Prazo (buffer): guarda as últimas N mensagens
2. Memória de Sessão: guarda todo o histórico da conversa

"""

from datetime import datetime
from typing import List, Dict
import json


class MemoriaAgente:
    """
    Classe que gerencia a memória do agente.
    
    Atributos:
        - memoria_curto_prazo: lista com as últimas mensagens (buffer)
        - memoria_sessao: lista com TODAS as mensagens da sessão
        - limite_curto_prazo: quantas mensagens guardar no buffer
    """
    
    def __init__(self, limite_curto_prazo: int = 10):
        """
        Inicializa o sistema de memória.
        
        Args:
            limite_curto_prazo: número máximo de mensagens na memória de curto prazo
        """
        # Memória de curto prazo: só as últimas N mensagens
        self.memoria_curto_prazo: List[Dict] = []
        
        # Memória de sessão: TODAS as mensagens (histórico completo)
        self.memoria_sessao: List[Dict] = []
        
        # Limite do buffer de curto prazo
        self.limite_curto_prazo = limite_curto_prazo
        
        print(f"✅ Memória iniciada (buffer de {limite_curto_prazo} mensagens)")
    
    
    def adicionar_mensagem(self, papel: str, conteudo: str):
        """
        Adiciona uma nova mensagem nas duas memórias.
        
        Args:
            papel: 'usuario' ou 'assistente'
            conteudo: o texto da mensagem
        """
        # Cria um dicionário com a mensagem
        mensagem = {
            "papel": papel,
            "conteudo": conteudo,
            "timestamp": datetime.now().isoformat()
        }
        
        # 1) Adiciona na memória de SESSÃO (histórico completo)
        self.memoria_sessao.append(mensagem)
        
        # 2) Adiciona na memória de CURTO PRAZO (buffer limitado)
        self.memoria_curto_prazo.append(mensagem)
        
        # Se o buffer ficou maior que o limite, remove a mais antiga
        if len(self.memoria_curto_prazo) > self.limite_curto_prazo:
            mensagem_removida = self.memoria_curto_prazo.pop(0)  # Remove a primeira (mais antiga)
            print(f"🗑️ Buffer cheio! Removida mensagem antiga: '{mensagem_removida['conteudo'][:30]}...'")
    
    
    def obter_contexto_curto_prazo(self) -> str:
        """
        Retorna as últimas mensagens formatadas como texto.
        Isso será enviado ao agente para dar contexto da conversa recente.
        
        Returns:
            String com as mensagens do buffer
        """
        if not self.memoria_curto_prazo:
            return "Nenhuma conversa recente."
        
        # Formata as mensagens de forma legível
        contexto = "📝 **Histórico recente da conversa:**\n\n"
        for msg in self.memoria_curto_prazo:
            papel = "👤 Usuário" if msg["papel"] == "usuario" else "🤖 Assistente"
            contexto += f"{papel}: {msg['conteudo']}\n\n"
        
        return contexto
    
    
    def obter_historico_completo(self) -> List[Dict]:
        """
        Retorna todo o histórico da sessão.
        
        Returns:
            Lista com todas as mensagens
        """
        return self.memoria_sessao.copy()
    
    
    def limpar_buffer(self):
        """
        Limpa apenas a memória de curto prazo (buffer).
        Mantém o histórico completo da sessão.
        """
        self.memoria_curto_prazo.clear()
        print("🗑️ Buffer de curto prazo limpo!")
    
    
    def limpar_tudo(self):
        """
        Limpa TODAS as memórias (reset completo).
        """
        self.memoria_curto_prazo.clear()
        self.memoria_sessao.clear()
        print("🗑️ Todas as memórias foram limpas!")
    
    
    def salvar_sessao(self, nome_arquivo: str = "sessao.json"):
        """
        Salva o histórico completo em um arquivo JSON.
        
        Args:
            nome_arquivo: nome do arquivo para salvar
        """
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(self.memoria_sessao, f, indent=2, ensure_ascii=False)
            print(f"💾 Sessão salva em '{nome_arquivo}'!")
        except Exception as e:
            print(f"❌ Erro ao salvar sessão: {e}")
    
    
    def carregar_sessao(self, nome_arquivo: str = "sessao.json"):
        """
        Carrega um histórico de uma sessão anterior.
        
        Args:
            nome_arquivo: nome do arquivo para carregar
        """
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                self.memoria_sessao = json.load(f)
            
            # Atualiza o buffer com as últimas N mensagens
            self.memoria_curto_prazo = self.memoria_sessao[-self.limite_curto_prazo:]
            
            print(f"📂 Sessão carregada de '{nome_arquivo}'!")
            print(f"   Total de mensagens: {len(self.memoria_sessao)}")
        except FileNotFoundError:
            print(f"⚠️ Arquivo '{nome_arquivo}' não encontrado.")
        except Exception as e:
            print(f"❌ Erro ao carregar sessão: {e}")
    
    
    def mostrar_estatisticas(self):
        """
        Mostra estatísticas sobre a memória.
        """
        print("\n📊 **Estatísticas da Memória:**")
        print(f"   • Mensagens no buffer (curto prazo): {len(self.memoria_curto_prazo)}/{self.limite_curto_prazo}")
        print(f"   • Mensagens na sessão (total): {len(self.memoria_sessao)}")
        
        if self.memoria_sessao:
            usuario_msgs = sum(1 for m in self.memoria_sessao if m["papel"] == "usuario")
            assistente_msgs = sum(1 for m in self.memoria_sessao if m["papel"] == "assistente")
            print(f"   • Mensagens do usuário: {usuario_msgs}")
            print(f"   • Mensagens do assistente: {assistente_msgs}")