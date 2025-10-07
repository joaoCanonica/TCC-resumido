#!/usr/bin/env python3
"""
Script de verificação do setup do projeto
"""

import sys

def verificar_modulos():
    """Verifica se todos os módulos necessários estão instalados"""

    modulos = {
        'gradio': 'Interface web',
        'requests': 'Chamadas HTTP',
        'config': 'Configurações locais'
    }

    modulos_opcionais = {
        'e2b_desktop': 'Sandbox E2B (opcional)',
        'smolagents': 'Framework de agentes (opcional)',
        'openai': 'Cliente OpenAI (opcional)',
        'huggingface_hub': 'HuggingFace Hub (opcional)'
    }

    print("=" * 70)
    print("🔍 VERIFICANDO DEPENDÊNCIAS DO PROJETO")
    print("=" * 70)

    erros = []
    avisos = []

    # Verificar módulos obrigatórios
    print("\n📦 Módulos Obrigatórios:")
    for modulo, descricao in modulos.items():
        try:
            __import__(modulo)
            print(f"  ✓ {modulo:20s} - {descricao}")
        except ImportError:
            print(f"  ✗ {modulo:20s} - {descricao} (FALTANDO)")
            erros.append(modulo)

    # Verificar módulos opcionais
    print("\n📦 Módulos Opcionais:")
    for modulo, descricao in modulos_opcionais.items():
        try:
            __import__(modulo)
            print(f"  ✓ {modulo:20s} - {descricao}")
        except ImportError:
            print(f"  ⚠ {modulo:20s} - {descricao} (não instalado)")
            avisos.append(modulo)

    # Verificar configuração
    print("\n⚙️  Configuração:")
    try:
        from config import GROK_API_KEY
        if GROK_API_KEY and GROK_API_KEY != "COLOQUE_SUA_CHAVE_AQUI844c92bf-23fd-4053-83c8-ab4f62d1031e":
            if GROK_API_KEY.startswith("xai-"):
                print(f"  ✓ GROK_API_KEY configurada corretamente")
            else:
                print(f"  ⚠ GROK_API_KEY não começa com 'xai-'")
                avisos.append("API Key format")
        else:
            print(f"  ✗ GROK_API_KEY não configurada")
            erros.append("GROK_API_KEY")
    except Exception as e:
        print(f"  ✗ Erro ao carregar config.py: {e}")
        erros.append("config.py")

    # Relatório final
    print("\n" + "=" * 70)
    if not erros:
        print("✅ TODOS OS REQUISITOS OBRIGATÓRIOS SATISFEITOS!")
        if avisos:
            print(f"⚠️  {len(avisos)} avisos (módulos opcionais)")
        print("\n🚀 Execute: python app.py")
    else:
        print("❌ FALTAM DEPENDÊNCIAS OBRIGATÓRIAS!")
        print(f"\nInstale com: pip install {' '.join(erros)}")
        print("\nOu instale tudo: pip install -r requirements.txt")
        return False
    print("=" * 70)

    return True


if __name__ == "__main__":
    sucesso = verificar_modulos()
    sys.exit(0 if sucesso else 1)
