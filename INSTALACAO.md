# 📦 Guia de Instalação - Grok AI Agent

## 🚀 Setup Completo

### Passo 1: Instalar Dependências

```bash
pip install -r requirements.txt
```

**Ou instale manualmente os módulos essenciais:**

```bash
pip install gradio requests
```

### Passo 2: Configurar API Key

Edite `config.py`:

```python
GROK_API_KEY = "xai-844c92bf-23fd-4053-83c8-ab4f62d1031e"
```

✅ Sua chave JÁ está configurada corretamente!

### Passo 3: Verificar Setup

```bash
python test_setup.py
```

### Passo 4: Executar o App

```bash
python app.py
```

Acesse: http://localhost:7860

---

## 📋 Status Atual

```
✓ config.py - Configurado
✓ grok_client.py - Pronto
✓ app.py - Pronto
✓ GROK_API_KEY - Configurada

⚠ gradio - Precisa instalar
⚠ requests - Precisa instalar
```

---

## 🔧 Solução de Problemas

### Erro: ModuleNotFoundError: No module named 'gradio'

```bash
pip install gradio
```

### Erro: ModuleNotFoundError: No module named 'requests'

```bash
pip install requests
```

### Instalar tudo de uma vez

```bash
pip install gradio requests Pillow
```

---

## ✅ Verificação Rápida

Execute este comando para verificar:

```bash
python3 -c "import gradio, requests; print('✓ Tudo pronto!')"
```

Se não houver erro, está tudo ok!

---

## 🎯 Próximos Passos

1. Instale as dependências: `pip install gradio requests`
2. Execute: `python app.py`
3. Abra: http://localhost:7860
4. Digite uma mensagem e teste!

---

**Após instalar as dependências, o app está 100% pronto para uso!**
