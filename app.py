#!/usr/bin/env python3
"""
Seu Agente Virtual - Interface Moderna
Design de tela de computador com integração Grok API
"""

import gradio as gr
import time
from datetime import datetime
from grok_client import GrokClient, gerar_resposta

cliente = GrokClient()

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@300;400;500&display=swap');

/* Fundo da página - Mesa de trabalho */
body {
    font-family: 'Inter', sans-serif;
    background: radial-gradient(circle at top, #1b1b1b, #0e0e0e);
    margin: 0;
    padding: 20px;
    overflow-x: hidden;
}

/* Container principal - Moldura do computador */
.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    background: linear-gradient(145deg, #2a2a2a, #1a1a1a) !important;
    border-radius: 20px !important;
    box-shadow:
        0 0 60px rgba(0, 0, 0, 0.9),
        inset 0 1px 1px rgba(255, 255, 255, 0.1),
        0 10px 40px rgba(0, 0, 0, 0.5) !important;
    border: 1px solid #333 !important;
    padding: 15px !important;
    position: relative !important;
}

/* Botões de controle MacBook-style no topo */
.gradio-container::before {
    content: '';
    position: absolute;
    top: 15px;
    left: 20px;
    width: 12px;
    height: 12px;
    background: #ff5f57;
    border-radius: 50%;
    box-shadow:
        20px 0 0 #ffbd2e,
        40px 0 0 #28ca42;
    z-index: 1000;
}

/* Título principal */
.title {
    color: #00b3ff;
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    margin: 30px 0 10px 0;
    text-shadow: 0 0 20px rgba(0, 179, 255, 0.5);
    letter-spacing: 1px;
}

.subtitle {
    color: #888;
    font-size: 14px;
    text-align: center;
    margin-bottom: 25px;
    font-weight: 400;
}

/* Barra de status */
.status-bar {
    background: linear-gradient(135deg, #1a1a1a, #0f0f0f);
    border: 1px solid #333;
    border-radius: 12px;
    padding: 12px 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 10px;
}

.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #00ff88;
    animation: pulse 2s ease-in-out infinite;
    box-shadow: 0 0 15px #00ff88;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.3); }
}

.status-text {
    color: #00b3ff;
    font-weight: 600;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Área do chat - Tela do computador */
#chatbot {
    background: #0f0f0f !important;
    border: 2px solid #2a2a2a !important;
    border-radius: 12px !important;
    min-height: 500px !important;
    box-shadow:
        inset 0 0 30px rgba(0, 0, 0, 0.8),
        0 4px 20px rgba(0, 0, 0, 0.6) !important;
    padding: 15px !important;
}

#chatbot .message {
    padding: 12px 16px !important;
    border-radius: 10px !important;
    margin: 8px 0 !important;
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
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
    background: linear-gradient(135deg, rgba(0, 179, 255, 0.15), rgba(0, 179, 255, 0.05)) !important;
    border-left: 3px solid #00b3ff !important;
}

#chatbot .message.bot {
    background: linear-gradient(135deg, rgba(123, 97, 255, 0.15), rgba(123, 97, 255, 0.05)) !important;
    border-left: 3px solid #7b61ff !important;
}

/* Campo de input */
#message-input {
    background: #1a1a1a !important;
    border: 2px solid #2a2a2a !important;
    border-radius: 10px !important;
    padding: 14px !important;
    font-size: 14px !important;
    color: #fff !important;
    font-family: 'Roboto Mono', monospace !important;
    transition: all 0.3s ease !important;
}

#message-input:focus {
    border-color: #00b3ff !important;
    box-shadow: 0 0 20px rgba(0, 179, 255, 0.3) !important;
    background: #0f0f0f !important;
}

#message-input::placeholder {
    color: #555 !important;
}

/* Botões */
button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    transition: all 0.3s ease !important;
    border: none !important;
    cursor: pointer !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    font-size: 13px !important;
}

button.primary {
    background: linear-gradient(145deg, #00b3ff, #0077cc) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(0, 179, 255, 0.3) !important;
}

button.primary:hover {
    background: linear-gradient(145deg, #0077cc, #00b3ff) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(0, 179, 255, 0.5) !important;
}

button.secondary {
    background: linear-gradient(145deg, #7b61ff, #5541cc) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(123, 97, 255, 0.3) !important;
}

button.secondary:hover {
    background: linear-gradient(145deg, #5541cc, #7b61ff) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(123, 97, 255, 0.5) !important;
}

/* Footer */
.footer-info {
    text-align: center;
    margin-top: 25px;
    padding: 15px;
    background: linear-gradient(135deg, rgba(0, 179, 255, 0.05), rgba(123, 97, 255, 0.05));
    border-radius: 10px;
    border: 1px solid #2a2a2a;
    color: #00b3ff;
    font-size: 12px;
    font-weight: 500;
}

/* Exemplos */
.examples {
    margin-top: 20px;
}

.example-label {
    color: #00b3ff;
    font-weight: 600;
    margin-bottom: 10px;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Scrollbar customizada */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #1a1a1a;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #00b3ff, #7b61ff);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #0077cc, #5541cc);
}

/* Ajustes de responsividade */
@media (max-width: 768px) {
    .gradio-container {
        padding: 10px !important;
        border-radius: 15px !important;
    }

    .title {
        font-size: 24px;
    }

    #chatbot {
        min-height: 400px !important;
    }
}
"""


def processar_mensagem(mensagem: str, historico: list) -> tuple:
    """Processa mensagem do usuário e retorna resposta do Grok"""
    if not mensagem.strip():
        return historico, ""

    if not cliente.is_connected():
        error_msg = "❌ Configure sua GROK_API_KEY no arquivo config.py"
        historico.append((mensagem, error_msg))
        return historico, ""

    historico.append((mensagem, "🤖 Processando..."))
    yield historico, ""

    start_time = time.time()
    resposta = gerar_resposta(mensagem, cliente)
    response_time = time.time() - start_time

    resposta_completa = f"{resposta}\n\n⏱️ _Tempo: {response_time:.2f}s_"
    historico[-1] = (mensagem, resposta_completa)

    yield historico, ""


def limpar_chat() -> tuple:
    """Limpa o histórico do chat"""
    cliente.limpar_historico()
    return [], ""


def obter_status_html() -> str:
    """Gera HTML com status de conexão"""
    is_connected = cliente.is_connected()
    status_text = "Sistema Conectado" if is_connected else "Sistema Offline"

    return f"""
    <div class="status-bar">
        <div class="status-indicator">
            <div class="status-dot"></div>
            <span class="status-text">{status_text}</span>
        </div>
        <span class="status-text">{datetime.now().strftime('%H:%M:%S')}</span>
    </div>
    """


# Interface Gradio
with gr.Blocks(theme=gr.themes.Soft(), css=custom_css, title="💻 Seu Agente Virtual") as app:

    gr.HTML("""
        <div class="title">💻 Seu Agente Virtual</div>
        <div class="subtitle">Interface inteligente com Grok AI • Powered by xAI</div>
    """)

    status_html = gr.HTML(obter_status_html())

    chatbot = gr.Chatbot(
        label="",
        elem_id="chatbot",
        height=500,
        bubble_full_width=False,
        avatar_images=(
            "https://api.dicebear.com/7.x/avataaars/svg?seed=user&backgroundColor=00b3ff",
            "https://api.dicebear.com/7.x/bottts/svg?seed=grok&backgroundColor=7b61ff"
        ),
        show_label=False
    )

    with gr.Row():
        msg = gr.Textbox(
            label="",
            placeholder="Digite sua mensagem... (Enter para enviar)",
            elem_id="message-input",
            scale=4,
            show_label=False,
            lines=2
        )

    with gr.Row():
        enviar_btn = gr.Button("📤 Enviar", elem_classes="primary", scale=2)
        limpar_btn = gr.Button("🗑️ Limpar", elem_classes="secondary", scale=1)

    gr.HTML("""
        <div class="footer-info">
            <strong>⚡ Sistema Operacional</strong><br>
            Modelo: <strong>Grok-Beta</strong> •
            Endpoint: <strong>api.x.ai</strong> •
            Status: <strong>Online</strong>
        </div>
    """)

    gr.Examples(
        examples=[
            "Olá! Como você pode me ajudar?",
            "Explique o conceito de inteligência artificial",
            "Quais são as melhores práticas em Python?",
            "Crie um exemplo de código para ordenar listas",
            "Diferença entre Machine Learning e Deep Learning"
        ],
        inputs=msg,
        label="💡 Sugestões de Perguntas"
    )

    # Event handlers
    enviar_btn.click(
        fn=processar_mensagem,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

    msg.submit(
        fn=processar_mensagem,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

    limpar_btn.click(
        fn=limpar_chat,
        outputs=[chatbot, msg]
    )


if __name__ == "__main__":
    print("=" * 70)
    print("💻 INICIANDO SEU AGENTE VIRTUAL")
    print("=" * 70)
    print(f"✓ Sistema configurado")
    print(f"✓ Grok API: {'Conectado ✓' if cliente.is_connected() else 'Configure config.py'}")
    print(f"✓ Modelo: grok-beta")
    print(f"✓ Interface: Tema Computador Moderno")
    print("=" * 70)
    print("🌐 Acesse: http://localhost:7860")
    print("=" * 70)

    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
