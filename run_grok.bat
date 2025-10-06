@echo off
echo ==========================================
echo 🚀 INICIANDO GROK AI AGENT
echo ==========================================

if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo 📥 Instalando dependências...
pip install -r requirements.txt

echo ==========================================
echo ✅ Setup completo!
echo 🌐 Iniciando servidor em http://localhost:7860
echo ==========================================

python app_grok.py
pause
