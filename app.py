#!/usr/bin/env python3
"""
Grok AI Agent - Aplicativo Principal
Interface Gradio para interagir com o Grok via API
"""

import gradio as gr
import time
from datetime import datetime
from grok_client import GrokClient, gerar_resposta

cliente = GrokClient()

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
    font-family: 'Inter', sans-serif;
}

.gradio-container {
    max-width: 1400px !important;
}

#chatbot {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-radius: 15px !important;
    min-height: 600px !important;
}

#chatbot .message {
    padding: 12px !important;
    border-radius: 8px !important;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 15px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
    margin-bottom: 15px;
}

.status-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #10b981;
    animation: pulse 2s ease-in-out infinite;
    box-shadow: 0 0 10px #10b981;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(1.2); }
}

.status-text {
    color: white;
    font-weight: 600;
    font-size: 14px;
}

#message-input {
    border: 2px solid #667eea !important;
    border-radius: 10px !important;
    padding: 12px !important;
    font-size: 14px !important;
}

button.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

button.primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
}

button.secondary {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
}

.footer-info {
    text-align: center;
    margin-top: 20px;
    padding: 15px;
    background: rgba(102, 126, 234, 0.1);
    border-radius: 10px;
    color: #667eea;
    font-size: 13px;
}
"""


def processar_mensagem(mensagem: str, historico: list) -> tuple:
    """
    Processa a mensagem do usuário e retorna a resposta do Grok

    Args:
        mensagem: Texto enviado pelo usuário
        historico: Histórico de conversação do Gradio

    Returns:
        Tupla com (histórico atualizado, campo de input limpo)
    """
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
    resposta_completa = f"{resposta}\n\n⏱️ _Tempo de resposta: {response_time:.2f}s_"

    historico[-1] = (mensagem, resposta_completa)

    yield historico, ""


def limpar_chat() -> tuple:
    """
    Limpa o histórico do chat

    Returns:
        Tupla com (histórico vazio, campo de input limpo)
    """
    cliente.limpar_historico()
    return [], ""


def obter_status_html() -> str:
    """
    Gera HTML com status de conexão

    Returns:
        HTML formatado com status
    """
    is_connected = cliente.is_connected()
    status_class = "status-dot" if is_connected else "status-dot offline"
    status_text = "✓ Conectado ao Grok" if is_connected else "✗ Desconectado"

    return f"""
    <div class="status-indicator">
        <div class="{status_class}"></div>
        <span class="status-text">{status_text}</span>
        <span class="status-text" style="margin-left: auto;">{datetime.now().strftime('%H:%M:%S')}</span>
    </div>
    """


with gr.Blocks(theme=gr.themes.Soft(), css=custom_css, title="Grok AI Agent") as app:

    gr.HTML("""
        <div style="text-align: center; padding: 30px 0 20px 0;">
            <h1 style="font-size: 48px; font-weight: 700; margin: 0;
                       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;">
                🤖 Grok AI Agent
            </h1>
            <p style="font-size: 16px; color: #64748b; margin-top: 10px;">
                Interface inteligente para conversar com o Grok via xAI API
            </p>
        </div>
    """)

    status_html = gr.HTML(obter_status_html())

    with gr.Row():
        with gr.Column(scale=1):
            chatbot = gr.Chatbot(
                label="💬 Conversação",
                elem_id="chatbot",
                height=600,
                bubble_full_width=False,
                avatar_images=(
                    "https://api.dicebear.com/7.x/avataaars/svg?seed=user",
                    "https://api.dicebear.com/7.x/bottts/svg?seed=grok"
                )
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="",
                    placeholder="Digite sua mensagem aqui... (Enter para enviar)",
                    elem_id="message-input",
                    scale=4,
                    show_label=False,
                    lines=2
                )

            with gr.Row():
                enviar_btn = gr.Button("🚀 Enviar", elem_classes="primary", scale=2)
                limpar_btn = gr.Button("🗑️ Limpar", elem_classes="secondary", scale=1)

    gr.HTML("""
        <div class="footer-info">
            <strong>📊 Informações do Sistema</strong><br>
            Modelo: <strong>grok-beta</strong> •
            Endpoint: <strong>api.x.ai</strong> •
            Status: <strong>Online</strong>
        </div>
    """)

    gr.Examples(
        examples=[
            "Olá! Como você funciona?",
            "Explique o que é inteligência artificial",
            "Quais são os principais conceitos de Python?",
            "Me ajude a criar um código Python para ordenar uma lista",
            "Qual a diferença entre machine learning e deep learning?"
        ],
        inputs=msg,
        label="💡 Exemplos de Perguntas"
    )

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
    print("🚀 INICIANDO GROK AI AGENT")
    print("=" * 70)
    print(f"✓ Cliente Grok configurado")
    print(f"✓ API Key: {'Configurada ✓' if cliente.is_connected() else 'Configure no config.py'}")
    print(f"✓ Modelo: grok-beta")
    print("=" * 70)
    print("🌐 Acesse: http://localhost:7860")
    print("=" * 70)

    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
