#!/bin/bash

echo "=========================================="
echo "🚀 INICIANDO GROK AI AGENT"
echo "=========================================="

if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

echo "📥 Instalando dependências..."
pip install -r requirements.txt

echo "=========================================="
echo "✅ Setup completo!"
echo "🌐 Iniciando servidor em http://localhost:7860"
echo "=========================================="

python app_grok.py
