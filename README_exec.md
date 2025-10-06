
# 🚀 Execução do Agente

## 1. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
```

## 2. Instalar dependências
```bash
pip install -r requirements.txt
```

## 3. Configurar chave da API
Edite o arquivo `config.py` e coloque sua chave do Grok:
```python
GROK_API_KEY = "sua_chave_aqui"
```

## 4. Executar
No Linux/Mac:
```bash
./run.sh
```

No Windows:
```bat
run.bat
```

## 5. Acessar
Abra no navegador:
```
http://localhost:7860
```
