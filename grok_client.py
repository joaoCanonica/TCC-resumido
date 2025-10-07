import json
import requests
from typing import List, Dict, Optional
from config import GROK_API_KEY


class GrokClient:
    """Cliente para interagir com a API do Grok (x.ai)"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or GROK_API_KEY
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-beta"
        self.historico = []

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False
    ) -> Dict:
        """
        Envia mensagens para o Grok e retorna a resposta

        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "..."}]
            temperature: Controle de criatividade (0-2)
            max_tokens: Máximo de tokens na resposta
            stream: Se True, retorna stream de respostas

        Returns:
            Resposta da API do Grok
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"Erro ao conectar com Grok API: {str(e)}"
            }

    def get_response_text(self, response: Dict) -> str:
        """Extrai o texto da resposta do Grok"""
        if "error" in response:
            return f"❌ Erro: {response.get('message', 'Erro desconhecido')}"

        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            return f"❌ Erro ao processar resposta: {str(e)}"

    def is_connected(self) -> bool:
        """Verifica se a API key está configurada"""
        return self.api_key and self.api_key != "COLOQUE_SUA_CHAVE_AQUI844c92bf-23fd-4053-83c8-ab4f62d1031e"

    def limpar_historico(self):
        """Limpa o histórico de conversação"""
        self.historico = []


def gerar_resposta(prompt: str, cliente: GrokClient = None) -> str:
    """
    Função principal para gerar resposta do Grok a partir de um prompt

    Args:
        prompt: Texto enviado pelo usuário
        cliente: Instância do GrokClient (opcional, cria uma nova se não fornecido)

    Returns:
        Resposta do Grok em texto
    """
    if cliente is None:
        cliente = GrokClient()

    if not cliente.is_connected():
        return "❌ Erro: Configure a GROK_API_KEY no arquivo config.py"

    cliente.historico.append({"role": "user", "content": prompt})

    system_message = {
        "role": "system",
        "content": "Você é Grok, um assistente de IA inteligente, prestativo e amigável. Responda de forma clara, objetiva e útil em português."
    }

    messages = [system_message] + cliente.historico[-10:]

    response = cliente.chat(messages)
    resposta_texto = cliente.get_response_text(response)

    cliente.historico.append({"role": "assistant", "content": resposta_texto})

    return resposta_texto
