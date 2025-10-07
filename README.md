# 🤖 Grok AI Agent

Aplicativo funcional de chat com interface Gradio integrada à API do Grok (xAI).

## 🚀 Instalação e Execução

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar API Key
Edite o arquivo `config.py` e adicione sua chave da API do Grok:
```python
GROK_API_KEY = "xai-sua-chave-aqui"
```

Obtenha sua chave em: https://x.ai/api

### 3. Executar o Aplicativo
```bash
python app.py
```

Acesse: **http://localhost:7860**

## 📁 Estrutura do Projeto

```
project/
├── app.py              # Aplicativo principal (Gradio)
├── grok_client.py      # Cliente da API do Grok
├── config.py           # Configurações (API KEY)
├── requirements.txt    # Dependências
├── e2bqwen.py         # Módulo de agente E2B
├── model_replay.py    # Replay de modelos
├── eval.py            # Avaliação
└── show_eval.py       # Visualização de avaliações
```

## ✨ Funcionalidades

- ✅ Chat interativo com Grok API
- ✅ Interface Gradio moderna e responsiva
- ✅ Histórico de conversação
- ✅ Indicador de tempo de resposta
- ✅ Exemplos de perguntas
- ✅ Status de conexão em tempo real
- ✅ Botão para limpar chat

## 🎯 Como Usar

1. Digite sua mensagem no campo de texto
2. Pressione **Enter** ou clique em **🚀 Enviar**
3. Aguarde a resposta do Grok
4. Continue a conversação naturalmente

## 🔧 API

### Função Principal

```python
from grok_client import gerar_resposta

resposta = gerar_resposta("Olá, como você está?")
print(resposta)
```

### Cliente Avançado

```python
from grok_client import GrokClient

cliente = GrokClient()
messages = [
    {"role": "user", "content": "Explique Python"}
]
response = cliente.chat(messages)
texto = cliente.get_response_text(response)
```

## 📊 Especificações

- **Modelo**: grok-beta
- **Endpoint**: https://api.x.ai/v1/chat/completions
- **Porta**: 7860
- **Framework**: Gradio
- **Linguagem**: Python 3.8+

## 🛠️ Dependências Principais

- `gradio` - Interface web
- `requests` - Chamadas HTTP
- `e2b_desktop` - Sandbox E2B
- `smolagents` - Framework de agentes
- `openai` - Cliente OpenAI compatível

## 📝 Licença

Projeto desenvolvido para integração com Grok API (xAI).

---

**Desenvolvido com Python + Gradio**
