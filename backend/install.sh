#!/bin/bash
# ==================================================
# Script de Instalação - Calmou Backend API
# ==================================================

set -e  # Para em caso de erro

echo "🚀 Instalando dependências do Calmou Backend..."
echo ""

# Verifica se está no ambiente virtual
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Ambiente virtual não detectado."
    echo "   Ativando ambiente virtual..."

    # Cria venv se não existir
    if [ ! -d ".venv" ]; then
        echo "   Criando ambiente virtual..."
        python3 -m venv .venv
    fi

    source .venv/bin/activate
    echo "   ✅ Ambiente virtual ativado!"
else
    echo "✅ Ambiente virtual já está ativo"
fi

echo ""
echo "📦 Instalando pacotes Python..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo ""
echo "✅ Instalação concluída com sucesso!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Configure as variáveis de ambiente (copie .env.example para .env)"
echo "   2. Execute: python app.py"
echo "   3. Ou com Docker: docker-compose up -d"
echo ""
