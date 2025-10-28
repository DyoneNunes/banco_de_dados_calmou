#!/bin/bash

# ========================================
# Script de Teste da API Calmou
# ========================================

API_URL="http://localhost:5001"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🚀 Iniciando testes da API Calmou..."
echo ""

# Teste 1: Health Check
echo "📊 Teste 1: Health Check"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/health)
if [ $RESPONSE -eq 200 ]; then
    echo -e "${GREEN}✅ Health Check: PASSOU${NC}"
else
    echo -e "${RED}❌ Health Check: FALHOU (HTTP $RESPONSE)${NC}"
fi
echo ""

# Teste 2: Info da API
echo "📊 Teste 2: Informações da API"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/)
if [ $RESPONSE -eq 200 ]; then
    echo -e "${GREEN}✅ Info da API: PASSOU${NC}"
else
    echo -e "${RED}❌ Info da API: FALHOU (HTTP $RESPONSE)${NC}"
fi
echo ""

# Teste 3: Registrar usuário
echo "📊 Teste 3: Registro de Usuário"
TIMESTAMP=$(date +%s)
EMAIL="teste$TIMESTAMP@calmou.app"

REGISTER_RESPONSE=$(curl -s -X POST $API_URL/register \
  -H "Content-Type: application/json" \
  -d "{
    \"nome\": \"Teste Usuario $TIMESTAMP\",
    \"email\": \"$EMAIL\",
    \"password\": \"senha12345\"
  }")

ACCESS_TOKEN=$(echo $REGISTER_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ ! -z "$ACCESS_TOKEN" ]; then
    echo -e "${GREEN}✅ Registro: PASSOU${NC}"
    echo "   Token: ${ACCESS_TOKEN:0:30}..."
else
    echo -e "${RED}❌ Registro: FALHOU${NC}"
    echo "   Resposta: $REGISTER_RESPONSE"
    exit 1
fi
echo ""

# Teste 4: Login
echo "📊 Teste 4: Login"
LOGIN_RESPONSE=$(curl -s -X POST $API_URL/login \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"senha12345\"
  }")

LOGIN_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ ! -z "$LOGIN_TOKEN" ]; then
    echo -e "${GREEN}✅ Login: PASSOU${NC}"
else
    echo -e "${RED}❌ Login: FALHOU${NC}"
    echo "   Resposta: $LOGIN_RESPONSE"
fi
echo ""

# Teste 5: Listar usuários (com autenticação)
echo "📊 Teste 5: Listar Usuários (Protegido)"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/usuarios \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if [ $RESPONSE -eq 200 ]; then
    echo -e "${GREEN}✅ Listar Usuários: PASSOU${NC}"
else
    echo -e "${RED}❌ Listar Usuários: FALHOU (HTTP $RESPONSE)${NC}"
fi
echo ""

# Teste 6: Tentar acessar sem token (deve falhar)
echo "📊 Teste 6: Acesso sem Token (deve falhar)"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/usuarios)

if [ $RESPONSE -eq 401 ]; then
    echo -e "${GREEN}✅ Proteção JWT: PASSOU (bloqueou corretamente)${NC}"
else
    echo -e "${RED}❌ Proteção JWT: FALHOU (deveria bloquear)${NC}"
fi
echo ""

# Teste 7: Registrar Humor
echo "📊 Teste 7: Registrar Humor"
USER_ID=$(echo $REGISTER_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

HUMOR_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $API_URL/humor \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "{
    \"usuario_id\": $USER_ID,
    \"nivel_humor\": 8,
    \"sentimento_principal\": \"Feliz\",
    \"notas\": \"Teste automatizado\"
  }")

if [ $HUMOR_RESPONSE -eq 201 ]; then
    echo -e "${GREEN}✅ Registrar Humor: PASSOU${NC}"
else
    echo -e "${RED}❌ Registrar Humor: FALHOU (HTTP $HUMOR_RESPONSE)${NC}"
fi
echo ""

# Teste 8: Relatório Semanal
echo "📊 Teste 8: Relatório Semanal de Humor"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/humor/relatorio-semanal \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if [ $RESPONSE -eq 200 ]; then
    echo -e "${GREEN}✅ Relatório Semanal: PASSOU${NC}"
else
    echo -e "${RED}❌ Relatório Semanal: FALHOU (HTTP $RESPONSE)${NC}"
fi
echo ""

# Teste 9: Listar Meditações (público)
echo "📊 Teste 9: Listar Meditações (Público)"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/meditacoes)

if [ $RESPONSE -eq 200 ]; then
    echo -e "${GREEN}✅ Listar Meditações: PASSOU${NC}"
else
    echo -e "${RED}❌ Listar Meditações: FALHOU (HTTP $RESPONSE)${NC}"
fi
echo ""

# Teste 10: Estatísticas (público)
echo "📊 Teste 10: Estatísticas do Sistema"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/stats)

if [ $RESPONSE -eq 200 ]; then
    echo -e "${GREEN}✅ Estatísticas: PASSOU${NC}"
else
    echo -e "${RED}❌ Estatísticas: FALHOU (HTTP $RESPONSE)${NC}"
fi
echo ""

# Resumo
echo "=========================================="
echo "🎯 RESUMO DOS TESTES"
echo "=========================================="
echo "✅ Todos os testes principais foram executados!"
echo ""
echo "📝 Dados do usuário criado:"
echo "   Email: $EMAIL"
echo "   Senha: senha12345"
echo "   ID: $USER_ID"
echo "   Token: ${ACCESS_TOKEN:0:50}..."
echo ""
echo "🔗 Acesse: $API_URL"
echo "=========================================="
