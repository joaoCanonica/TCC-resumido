#!/usr/bin/env python3
"""
Grok AI Agent - Demo Interface
Versão de demonstração com simulação quando API não está disponível
"""

import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import random

try:
    from config import GROK_API_KEY
except:
    GROK_API_KEY = "xai-844c92bf-23fd-4053-83c8-ab4f62d1031e"

chat_history = []


def call_grok_api(messages):
    """Chama a API do Grok com fallback para modo demo"""

    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROK_API_KEY}"
    }
    payload = {
        "model": "grok-beta",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"], True

    except Exception as e:
        # Modo demo - simular respostas
        print(f"⚠️  API indisponível ({str(e)}), usando modo DEMO")
        return simulate_grok_response(messages), False


def simulate_grok_response(messages):
    """Simula resposta do Grok para demonstração"""

    user_message = messages[-1]["content"].lower()

    responses = {
        "olá": "Olá! 👋 Sou o Grok em modo demonstração. Como posso ajudá-lo hoje?",
        "oi": "Oi! Tudo bem? Estou aqui para ajudar!",
        "como você está": "Estou ótimo! Funcionando perfeitamente em localhost. E você?",
        "python": "Python é uma linguagem incrível! 🐍 É versátil, poderosa e tem uma sintaxe clara. Perfeita para IA!",
        "ia": "Inteligência Artificial está revolucionando o mundo! Posso ajudar com desenvolvimento, análise de dados e muito mais.",
        "ajuda": "Claro! Posso ajudar com:\n• Programação (Python, JavaScript, etc)\n• Dúvidas técnicas\n• Explicações conceituais\n• Criação de código\n• E muito mais!",
    }

    for keyword, response in responses.items():
        if keyword in user_message:
            return response

    return f"Entendi sua mensagem: '{messages[-1]['content']}'\n\n💡 Estou rodando em **modo DEMO** pois a API do Grok está temporariamente indisponível. Mas posso te mostrar todas as funcionalidades da interface!\n\n✨ Recursos ativos:\n• Chat em tempo real\n• Design futurista\n• Histórico de mensagens\n• Interface responsiva"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ Grok AI Agent</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto+Mono:wght@300;400&display=swap');

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Roboto Mono', monospace;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #00ff88;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 1200px;
            background: linear-gradient(145deg, #1a1f3a, #0f1729);
            border: 3px solid #1e3a5f;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 0 50px rgba(0, 217, 255, 0.3);
            position: relative;
        }

        .container::before {
            content: '';
            position: absolute;
            top: -3px; left: -3px; right: -3px; bottom: -3px;
            background: linear-gradient(45deg, #00d9ff, transparent, #00ff88);
            border-radius: 20px;
            z-index: -1;
            opacity: 0.5;
            animation: border-glow 3s ease-in-out infinite;
        }

        @keyframes border-glow {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 0.8; }
        }

        .title {
            font-family: 'Orbitron', sans-serif;
            font-size: 42px;
            font-weight: 900;
            text-align: center;
            background: linear-gradient(135deg, #00d9ff, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            letter-spacing: 3px;
        }

        .subtitle {
            text-align: center;
            color: #00d9ff;
            font-size: 14px;
            margin-bottom: 30px;
            opacity: 0.8;
        }

        .status-bar {
            background: rgba(0, 217, 255, 0.1);
            border: 1px solid #00d9ff;
            border-radius: 10px;
            padding: 15px 20px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00ff88;
            box-shadow: 0 0 10px #00ff88;
            animation: pulse 2s ease-in-out infinite;
        }

        .status-dot.demo {
            background: #ffaa00;
            box-shadow: 0 0 10px #ffaa00;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(1.2); }
        }

        .status-text {
            color: #00d9ff;
            font-weight: 700;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .chat-container {
            background: rgba(10, 14, 39, 0.8);
            border: 2px solid #1e3a5f;
            border-radius: 15px;
            padding: 20px;
            height: 500px;
            overflow-y: auto;
            margin-bottom: 20px;
        }

        .message {
            margin: 15px 0;
            padding: 15px;
            border-radius: 10px;
            animation: message-appear 0.3s ease-out;
        }

        @keyframes message-appear {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
            background: linear-gradient(135deg, rgba(0, 217, 255, 0.2), rgba(0, 217, 255, 0.1));
            border-left: 3px solid #00d9ff;
            margin-left: 50px;
        }

        .message.bot {
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 255, 136, 0.1));
            border-left: 3px solid #00ff88;
            margin-right: 50px;
        }

        .message-header {
            font-weight: 700;
            margin-bottom: 8px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .message.user .message-header { color: #00d9ff; }
        .message.bot .message-header { color: #00ff88; }

        .message-content {
            color: #ffffff;
            line-height: 1.6;
            white-space: pre-wrap;
        }

        .input-container {
            display: flex;
            gap: 10px;
        }

        #messageInput {
            flex: 1;
            background: rgba(10, 14, 39, 0.6);
            border: 2px solid #00d9ff;
            color: #00ff88;
            font-family: 'Roboto Mono', monospace;
            font-size: 14px;
            border-radius: 10px;
            padding: 15px;
            outline: none;
            transition: all 0.3s ease;
        }

        #messageInput:focus {
            border-color: #00ff88;
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
        }

        button {
            background: linear-gradient(135deg, #00d9ff, #0088cc);
            border: none;
            color: #0a0e27;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.4);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 30px rgba(0, 217, 255, 0.6);
        }

        .clear-btn {
            background: linear-gradient(135deg, #ff6b35, #cc5500);
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .stat-box {
            background: rgba(0, 217, 255, 0.1);
            border: 1px solid #00d9ff;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }

        .stat-label {
            color: #00d9ff;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }

        .stat-value {
            color: #00ff88;
            font-size: 20px;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
        }

        .loading {
            display: none;
            text-align: center;
            color: #00d9ff;
            margin: 10px 0;
            animation: loading-pulse 1.5s ease-in-out infinite;
        }

        @keyframes loading-pulse {
            0%, 100% { opacity: 0.4; }
            50% { opacity: 1; }
        }

        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: rgba(10, 14, 39, 0.5); }
        ::-webkit-scrollbar-thumb { background: #00d9ff; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">⚡ GROK AI AGENT ⚡</div>
        <div class="subtitle">Powered by xAI • Interface Neural Avançada</div>

        <div class="status-bar">
            <div class="status-indicator">
                <div class="status-dot" id="statusDot"></div>
                <span class="status-text" id="statusText">CONECTADO ✓</span>
            </div>
            <span id="clock" style="color: #00ff88; font-size: 14px;"></span>
        </div>

        <div class="chat-container" id="chatContainer">
            <div class="message bot">
                <div class="message-header">🤖 GROK</div>
                <div class="message-content">Olá! Sou o Grok, seu assistente de IA.\n\n✨ Sistema totalmente funcional!\n💬 Digite qualquer mensagem para começar.</div>
            </div>
        </div>

        <div class="loading" id="loading">🤖 Processando resposta...</div>

        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Digite sua mensagem... (Enter para enviar)" autocomplete="off"/>
            <button onclick="sendMessage()">🚀 ENVIAR</button>
            <button class="clear-btn" onclick="clearChat()">🗑️ LIMPAR</button>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-label">Modelo</div>
                <div class="stat-value">GROK-BETA</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Status</div>
                <div class="stat-value" id="statStatus">ONLINE</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Modo</div>
                <div class="stat-value" id="statMode">DEMO</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Mensagens</div>
                <div class="stat-value" id="messageCount">0</div>
            </div>
        </div>
    </div>

    <script>
        function updateClock() {
            const now = new Date();
            document.getElementById('clock').textContent = now.toLocaleTimeString('pt-BR');
        }
        setInterval(updateClock, 1000);
        updateClock();

        let messageCount = 0;

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;

            addMessage('user', message);
            input.value = '';
            messageCount++;
            updateMessageCount();

            document.getElementById('loading').style.display = 'block';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                addMessage('bot', data.response);

                if (data.is_demo) {
                    document.getElementById('statusDot').classList.add('demo');
                    document.getElementById('statusText').textContent = 'MODO DEMO ⚠️';
                    document.getElementById('statMode').textContent = 'DEMO';
                } else {
                    document.getElementById('statMode').textContent = 'API REAL';
                }

                messageCount++;
                updateMessageCount();

            } catch (error) {
                addMessage('bot', '❌ Erro: ' + error.message);
            }

            document.getElementById('loading').style.display = 'none';
        }

        function addMessage(type, content) {
            const container = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            const header = type === 'user' ? '👤 VOCÊ' : '🤖 GROK';
            messageDiv.innerHTML = `
                <div class="message-header">${header}</div>
                <div class="message-content">${content}</div>
            `;
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }

        function clearChat() {
            document.getElementById('chatContainer').innerHTML = `
                <div class="message bot">
                    <div class="message-header">🤖 GROK</div>
                    <div class="message-content">Chat limpo! Como posso ajudá-lo?</div>
                </div>
            `;
            messageCount = 0;
            updateMessageCount();
            fetch('/api/clear', { method: 'POST' });
        }

        function updateMessageCount() {
            document.getElementById('messageCount').textContent = messageCount;
        }

        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""


class GrokRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            user_message = data.get('message', '')

            chat_history.append({"role": "user", "content": user_message})

            messages = [
                {"role": "system", "content": "Você é Grok, um assistente de IA inteligente e prestativo."}
            ] + chat_history[-10:]

            bot_response, is_real_api = call_grok_api(messages)
            chat_history.append({"role": "assistant", "content": bot_response})

            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()

            response = json.dumps({
                'response': bot_response,
                'timestamp': datetime.now().isoformat(),
                'is_demo': not is_real_api
            }, ensure_ascii=False)

            self.wfile.write(response.encode('utf-8'))

        elif self.path == '/api/clear':
            chat_history.clear()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def run_server(port=7860):
    server_address = ('', port)
    httpd = HTTPServer(server_address, GrokRequestHandler)

    print("=" * 70)
    print("🚀 GROK AI AGENT - SERVIDOR ATIVO")
    print("=" * 70)
    print(f"✓ URL: http://localhost:{port}")
    print(f"✓ API Key: {'Configurada ✓' if GROK_API_KEY else 'Não configurada'}")
    print(f"✓ Modo: API Real com fallback para Demo")
    print("=" * 70)
    print("📝 Pressione Ctrl+C para parar")
    print("=" * 70)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor encerrado")
        httpd.shutdown()


if __name__ == "__main__":
    run_server()
