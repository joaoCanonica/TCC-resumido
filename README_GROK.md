# 🚀 Grok AI Agent - Interface Neural Avançada

Aplicativo web completo com interface Gradio moderna integrada à API do Grok (xAI).

## ✨ Características

- 🤖 **Integração direta com Grok API** (xAI)
- 💬 **Interface de chat interativa** com design futurista
- ⚡ **Execução 100% local** sem dependências externas pesadas
- 🎨 **Design cyberpunk** com animações e efeitos visuais
- 📊 **Monitoramento em tempo real** do status da conexão
- ⏱️ **Métricas de performance** (tempo de resposta)

## 🛠️ Instalação Rápida

### Windows
```bash
run_grok.bat
```

### Linux/Mac
```bash
chmod +x run_grok.sh
./run_grok.sh
```

### Manual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar
python app_grok.py
```

## 🔑 Configuração da API

1. Edite o arquivo `config.py`
2. Substitua `COLOQUE_SUA_CHAVE_AQUI` pela sua chave da API do Grok
3. Obtenha sua chave em: https://x.ai/api

```python
# config.py
GROK_API_KEY = "xai-sua-chave-aqui"
```

## 🌐 Acesso

Após iniciar, acesse:
- **URL Local**: http://localhost:7860
- **Interface**: Totalmente responsiva e moderna

## 🎯 Funcionalidades

### Chat Interativo
- Envio de mensagens em tempo real
- Histórico de conversação
- Indicador de "digitando..."
- Avatar personalizado para usuário e IA

### Status em Tempo Real
- ✅ Indicador de conexão (verde = conectado, vermelho = desconectado)
- ⏱️ Relógio ao vivo
- 📊 Métricas de performance
- 🤖 Status do modelo (GROK-BETA)

### Design Cyberpunk
- 🎨 Gradientes animados
- ✨ Efeitos de brilho (glow)
- 💫 Animações suaves
- 🖥️ Moldura de terminal futurista

## 📋 Estrutura de Arquivos

```
project/
├── app_grok.py          # Aplicativo principal Gradio
├── grok_client.py       # Cliente da API do Grok
├── config.py            # Configurações (API KEY)
├── requirements.txt     # Dependências Python
├── run_grok.sh         # Script de execução (Linux/Mac)
├── run_grok.bat        # Script de execução (Windows)
└── README_GROK.md      # Este arquivo
```

## 🔧 Troubleshooting

### Erro: API Key inválida
- Verifique se configurou corretamente em `config.py`
- Certifique-se de que a chave começa com `xai-`

### Erro: Módulo não encontrado
```bash
pip install -r requirements.txt --upgrade
```

### Porta já em uso
Edite `app_grok.py` e altere a porta:
```python
demo.launch(server_port=8080)  # Altere de 7860 para outra porta
```

## 📊 Requisitos

- Python 3.8+
- Conexão com internet (para API do Grok)
- 2GB RAM mínimo
- Navegador moderno (Chrome, Firefox, Edge)

## 🚀 Próximos Passos

- [ ] Adicionar suporte a streaming de respostas
- [ ] Implementar histórico persistente
- [ ] Adicionar mais modelos (GPT-4, Claude, etc.)
- [ ] Sistema de plugins
- [ ] Exportar conversas

## 📝 Licença

Este projeto é baseado nos arquivos originais do repositório e adaptado para uso local com Grok API.

## 🤝 Suporte

Para problemas ou dúvidas:
1. Verifique a documentação da API do Grok: https://docs.x.ai
2. Confira os logs no terminal
3. Revise o arquivo `config.py`

---

**Desenvolvido com ⚡ por um agente especializado em IA**
