#!/usr/bin/env python3
"""
Grok AI Agent - Interface Web Simples
Aplicativo minimalista que funciona sem dependências externas pesadas
"""

import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import os

# Importar chave da API
try:
    from config import GROK_API_KEY
except:
    GROK_API_KEY = "xai-844c92bf-23fd-4053-83c8-ab4f62d1031e"

# Histórico global de mensagens
chat_history = []


def call_grok_api(messages):
    """Chama a API do Grok e retorna a resposta"""

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

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"]

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return f"❌ Erro HTTP {e.code}: {error_body}"
    except Exception as e:
        return f"❌ Erro: {str(e)}"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ Grok AI Agent</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto+Mono:wght@300;400&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

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
            top: -3px;
            left: -3px;
            right: -3px;
            bottom: -3px;
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
            text-shadow: 0 0 30px rgba(0, 217, 255, 0.5);
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
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
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

        .message.user .message-header {
            color: #00d9ff;
        }

        .message.bot .message-header {
            color: #00ff88;
        }

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

        button:active {
            transform: translateY(0);
        }

        .clear-btn {
            background: linear-gradient(135deg, #ff6b35, #cc5500);
        }

        .clear-btn:hover {
            box-shadow: 0 0 30px rgba(255, 107, 53, 0.6);
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

        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(10, 14, 39, 0.5);
        }

        ::-webkit-scrollbar-thumb {
            background: #00d9ff;
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #00ff88;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">⚡ GROK AI AGENT ⚡</div>
        <div class="subtitle">Powered by xAI • Interface Neural Avançada</div>

        <div class="status-bar">
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span class="status-text">CONECTADO AO GROK ✓</span>
            </div>
            <span id="clock" style="color: #00ff88; font-size: 14px;"></span>
        </div>

        <div class="chat-container" id="chatContainer">
            <div class="message bot">
                <div class="message-header">🤖 GROK</div>
                <div class="message-content">Olá! Sou o Grok, seu assistente de IA. Como posso ajudá-lo hoje?</div>
            </div>
        </div>

        <div class="loading" id="loading">🤖 Processando resposta...</div>

        <div class="input-container">
            <input
                type="text"
                id="messageInput"
                placeholder="Digite sua mensagem... (Enter para enviar)"
                autocomplete="off"
            />
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
                <div class="stat-value">ONLINE</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">API</div>
                <div class="stat-value">X.AI</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Mensagens</div>
                <div class="stat-value" id="messageCount">0</div>
            </div>
        </div>
    </div>

    <script>
        // Atualizar relógio
        function updateClock() {
            const now = new Date();
            document.getElementById('clock').textContent = now.toLocaleTimeString('pt-BR');
        }
        setInterval(updateClock, 1000);
        updateClock();

        let messageCount = 0;

        // Enviar mensagem
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();

            if (!message) return;

            // Adicionar mensagem do usuário
            addMessage('user', message);
            input.value = '';
            messageCount++;
            updateMessageCount();

            // Mostrar loading
            document.getElementById('loading').style.display = 'block';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();

                // Adicionar resposta do bot
                addMessage('bot', data.response);
                messageCount++;
                updateMessageCount();

            } catch (error) {
                addMessage('bot', '❌ Erro ao conectar com o servidor: ' + error.message);
            }

            // Esconder loading
            document.getElementById('loading').style.display = 'none';
        }

        // Adicionar mensagem ao chat
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

        // Limpar chat
        function clearChat() {
            const container = document.getElementById('chatContainer');
            container.innerHTML = `
                <div class="message bot">
                    <div class="message-header">🤖 GROK</div>
                    <div class="message-content">Chat limpo! Como posso ajudá-lo?</div>
                </div>
            `;
            messageCount = 0;
            updateMessageCount();

            // Limpar histórico no servidor
            fetch('/api/clear', { method: 'POST' });
        }

        // Atualizar contador
        function updateMessageCount() {
            document.getElementById('messageCount').textContent = messageCount;
        }

        // Enter para enviar
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""


class GrokRequestHandler(BaseHTTPRequestHandler):
    """Handler para requisições HTTP"""

    def log_message(self, format, *args):
        """Suprimir logs padrão"""
        pass

    def do_GET(self):
        """Servir página HTML"""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Processar requisições POST"""

        if self.path == '/api/chat':
            # Ler corpo da requisição
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            user_message = data.get('message', '')

            # Adicionar ao histórico
            chat_history.append({"role": "user", "content": user_message})

            # Preparar mensagens para API
            messages = [
                {"role": "system", "content": "Você é Grok, um assistente de IA inteligente e prestativo. Responda de forma clara e objetiva em português."}
            ] + chat_history[-10:]  # Últimas 10 mensagens

            # Chamar API
            bot_response = call_grok_api(messages)

            # Adicionar resposta ao histórico
            chat_history.append({"role": "assistant", "content": bot_response})

            # Enviar resposta
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()

            response = json.dumps({
                'response': bot_response,
                'timestamp': datetime.now().isoformat()
            }, ensure_ascii=False)

            self.wfile.write(response.encode('utf-8'))

        elif self.path == '/api/clear':
            # Limpar histórico
            chat_history.clear()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()


def run_server(port=7860):
    """Iniciar servidor HTTP"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, GrokRequestHandler)

    print("=" * 70)
    print("�� GROK AI AGENT - SERVIDOR INICIADO")
    print("=" * 70)
    print(f"✓ Servidor rodando em: http://localhost:{port}")
    print(f"✓ API Key configurada: {'Sim ✓' if GROK_API_KEY else 'Não ✗'}")
    print(f"✓ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print("📝 Pressione Ctrl+C para parar o servidor")
    print("=" * 70)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor encerrado pelo usuário")
        httpd.shutdown()


if __name__ == "__main__":
    run_server()
