#!/bin/bash

# Script para reiniciar o backend quando houver problemas de conexão
# Uso: ./restart-backend.sh

echo "🔄 Reiniciando backend Calmou..."
docker restart calmou_backend

echo "⏳ Aguardando inicialização..."
sleep 3

echo "✅ Testando conexão..."
curl -s http://192.168.0.109:5001/ | grep -q "Calmou API" && echo "✅ Backend está online!" || echo "❌ Backend ainda não está respondendo"

echo ""
echo "📊 Status dos containers:"
docker ps | grep calmou

echo ""
echo "💡 Se o problema persistir, execute:"
echo "   docker restart calmou_backend calmou_postgres"
