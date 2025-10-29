#!/bin/bash

# Script rápido para reiniciar o backend quando der erro 500
# Uso: ./fix-backend.sh

echo "🔄 Reiniciando backend..."
docker restart calmou_backend > /dev/null 2>&1

echo "✅ Pronto! Recarregue o app."
echo ""
echo "💡 Dica: Pressione 'r' no Metro bundler ou sacuda o dispositivo"
