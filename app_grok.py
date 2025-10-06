import gradio as gr
import time
from datetime import datetime
from grok_client import GrokClient
from config import GROK_API_KEY

client = GrokClient()

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto+Mono:wght@300;400;500&display=swap');

:root {
    --terminal-bg: #0a0e27;
    --terminal-border: #1e3a5f;
    --terminal-glow: #00d9ff;
    --terminal-text: #00ff88;
    --warning-color: #ff6b35;
}

body {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    font-family: 'Roboto Mono', monospace;
}

.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto;
}

/* Computer Screen Frame */
.computer-frame {
    background: linear-gradient(145deg, #1a1f3a, #0f1729);
    border: 3px solid var(--terminal-border);
    border-radius: 20px;
    padding: 20px;
    box-shadow:
        0 0 30px rgba(0, 217, 255, 0.3),
        inset 0 0 20px rgba(0, 0, 0, 0.5);
    position: relative;
    margin: 20px 0;
}

.computer-frame::before {
    content: '';
    position: absolute;
    top: -3px;
    left: -3px;
    right: -3px;
    bottom: -3px;
    background: linear-gradient(45deg, var(--terminal-glow), transparent, var(--terminal-glow));
    border-radius: 20px;
    z-index: -1;
    opacity: 0.5;
    animation: border-glow 3s ease-in-out infinite;
}

@keyframes border-glow {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 0.8; }
}

/* Status Bar */
.status-bar {
    background: rgba(0, 217, 255, 0.1);
    border: 1px solid var(--terminal-glow);
    border-radius: 10px;
    padding: 15px 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'Orbitron', sans-serif;
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
    animation: pulse 2s ease-in-out infinite;
}

.status-connected {
    background: #00ff88;
    box-shadow: 0 0 10px #00ff88;
}

.status-disconnected {
    background: #ff6b35;
    box-shadow: 0 0 10px #ff6b35;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(1.2); }
}

.status-text {
    color: var(--terminal-glow);
    font-weight: 700;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.status-time {
    color: var(--terminal-text);
    font-size: 12px;
    font-weight: 400;
}

/* Chat Interface */
#chatbot {
    background: rgba(10, 14, 39, 0.8) !important;
    border: 2px solid var(--terminal-border) !important;
    border-radius: 15px !important;
    min-height: 500px !important;
    font-family: 'Roboto Mono', monospace !important;
}

#chatbot .message {
    padding: 15px !important;
    margin: 10px 0 !important;
    border-radius: 10px !important;
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

#chatbot .message.user {
    background: linear-gradient(135deg, rgba(0, 217, 255, 0.2), rgba(0, 217, 255, 0.1)) !important;
    border-left: 3px solid var(--terminal-glow) !important;
}

#chatbot .message.bot {
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 255, 136, 0.1)) !important;
    border-left: 3px solid var(--terminal-text) !important;
}

/* Input Area */
.input-container {
    background: rgba(30, 58, 95, 0.3);
    border: 2px solid var(--terminal-border);
    border-radius: 15px;
    padding: 15px;
    margin-top: 20px;
}

#message-input {
    background: rgba(10, 14, 39, 0.6) !important;
    border: 1px solid var(--terminal-glow) !important;
    color: var(--terminal-text) !important;
    font-family: 'Roboto Mono', monospace !important;
    font-size: 14px !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

#message-input:focus {
    border-color: var(--terminal-glow) !important;
    box-shadow: 0 0 15px rgba(0, 217, 255, 0.3) !important;
}

/* Buttons */
.btn-primary {
    background: linear-gradient(135deg, var(--terminal-glow), #0088cc) !important;
    border: none !important;
    color: #0a0e27 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    padding: 12px 30px !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 20px rgba(0, 217, 255, 0.4) !important;
}

.btn-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 30px rgba(0, 217, 255, 0.6) !important;
}

.btn-secondary {
    background: linear-gradient(135deg, var(--warning-color), #cc5500) !important;
    border: none !important;
    color: white !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    padding: 12px 30px !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

.btn-secondary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 20px rgba(255, 107, 53, 0.4) !important;
}

/* Loading Animation */
.loading-text {
    color: var(--terminal-glow);
    font-family: 'Orbitron', sans-serif;
    animation: loading-pulse 1.5s ease-in-out infinite;
}

@keyframes loading-pulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

/* Title */
.title {
    font-family: 'Orbitron', sans-serif;
    font-size: 36px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, var(--terminal-glow), var(--terminal-text));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(0, 217, 255, 0.5);
    margin-bottom: 10px;
    letter-spacing: 3px;
}

.subtitle {
    font-family: 'Roboto Mono', monospace;
    text-align: center;
    color: var(--terminal-text);
    font-size: 14px;
    margin-bottom: 30px;
    opacity: 0.8;
}

/* Stats Display */
.stats-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-top: 20px;
}

.stat-box {
    background: rgba(0, 217, 255, 0.1);
    border: 1px solid var(--terminal-glow);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
}

.stat-label {
    color: var(--terminal-glow);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 5px;
}

.stat-value {
    color: var(--terminal-text);
    font-size: 20px;
    font-weight: 700;
    font-family: 'Orbitron', sans-serif;
}
"""

custom_js = """
function() {
    console.log("🚀 Grok AI Agent Initialized");

    setInterval(() => {
        const timeElement = document.querySelector('.status-time');
        if (timeElement) {
            const now = new Date();
            timeElement.textContent = now.toLocaleTimeString('pt-BR');
        }
    }, 1000);

    document.body.classList.add('dark');
}
"""


def get_status_html(is_connected: bool) -> str:
    """Gera HTML da barra de status"""
    status_class = "status-connected" if is_connected else "status-disconnected"
    status_text = "CONECTADO AO GROK ✓" if is_connected else "DESCONECTADO ✗"

    return f"""
    <div class="status-bar">
        <div class="status-indicator">
            <div class="status-dot {status_class}"></div>
            <span class="status-text">{status_text}</span>
        </div>
        <span class="status-time">{datetime.now().strftime('%H:%M:%S')}</span>
    </div>
    """


def chat_with_grok(message: str, history: list) -> tuple:
    """Processa mensagem e retorna resposta do Grok"""

    if not client.is_connected():
        error_msg = "❌ Configure sua GROK_API_KEY no arquivo config.py"
        history.append((message, error_msg))
        return history, ""

    history.append((message, "🤖 Digitando..."))
    yield history, ""

    messages = [{"role": "system", "content": "Você é Grok, um assistente de IA inteligente e prestativo. Responda de forma clara e objetiva."}]

    for user_msg, bot_msg in history[:-1]:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if bot_msg and bot_msg != "🤖 Digitando...":
            messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": message})

    start_time = time.time()
    response = client.chat(messages)
    response_time = time.time() - start_time

    bot_response = client.get_response_text(response)
    bot_response += f"\n\n⏱️ _Tempo de resposta: {response_time:.2f}s_"

    history[-1] = (message, bot_response)

    yield history, ""


def clear_chat():
    """Limpa o histórico do chat"""
    return [], ""


with gr.Blocks(theme=gr.themes.Soft(), css=custom_css, js=custom_js) as demo:

    with gr.Column(elem_classes="computer-frame"):

        gr.HTML("<div class='title'>⚡ GROK AI AGENT ⚡</div>")
        gr.HTML("<div class='subtitle'>Powered by xAI • Interface Neural Avançada</div>")

        status_display = gr.HTML(get_status_html(client.is_connected()))

        chatbot = gr.Chatbot(
            label="💬 Terminal de Comunicação",
            elem_id="chatbot",
            height=500,
            bubble_full_width=False,
            avatar_images=(
                "https://api.dicebear.com/7.x/avataaars/svg?seed=user",
                "https://api.dicebear.com/7.x/bottts/svg?seed=grok"
            )
        )

        with gr.Column(elem_classes="input-container"):
            with gr.Row():
                msg = gr.Textbox(
                    label="",
                    placeholder="Digite sua mensagem aqui... (Enter para enviar)",
                    elem_id="message-input",
                    scale=4,
                    show_label=False
                )

            with gr.Row():
                send_btn = gr.Button("🚀 ENVIAR", elem_classes="btn-primary", scale=1)
                clear_btn = gr.Button("🗑️ LIMPAR", elem_classes="btn-secondary", scale=1)

        gr.HTML("""
        <div class="stats-container">
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
        </div>
        """)

        gr.HTML("""
        <div style="text-align: center; margin-top: 30px; padding: 20px;
                    border-top: 1px solid rgba(0, 217, 255, 0.3);">
            <p style="color: #00d9ff; font-size: 12px; font-family: 'Roboto Mono', monospace;">
                🛡️ SISTEMA PROTEGIDO • CONEXÃO CRIPTOGRAFADA • INTERFACE NEURAL v2.0
            </p>
        </div>
        """)

    send_btn.click(
        fn=chat_with_grok,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

    msg.submit(
        fn=chat_with_grok,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

    clear_btn.click(
        fn=clear_chat,
        outputs=[chatbot, msg]
    )


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 INICIANDO GROK AI AGENT")
    print("=" * 60)
    print(f"✓ Interface Gradio carregada")
    print(f"✓ Cliente Grok configurado")
    print(f"✓ Status API: {'CONECTADO' if client.is_connected() else 'CONFIGURE A API KEY'}")
    print("=" * 60)
    print("🌐 Acesse: http://localhost:7860")
    print("=" * 60)

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
