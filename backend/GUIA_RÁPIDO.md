# ⚡ Guia Rápido - API Calmou

**Start em 5 minutos!** 🚀

---

## 🎯 Opção 1: Início Rápido (Desenvolvimento)

```bash
# 1. Instale dependências
pip install -r requirements.txt

# 2. Configure .env
cp .env.example .env
nano .env  # Adicione sua senha do PostgreSQL

# 3. Execute migração do banco
psql -U postgres -d meu_banco -f migration_fix_usuarios.sql

# 4. Inicie o servidor
python app.py
```

✅ API rodando em: `http://localhost:5001`

---

## 🐳 Opção 2: Docker (Recomendado)

```bash
# 1. Configure .env
cp .env.example .env

# 2. Suba tudo
docker-compose up -d

# 3. Veja logs
docker-compose logs -f backend
```

✅ API rodando em: `http://localhost:5001`
✅ pgAdmin em: `http://localhost:5050` (se usar `--profile tools`)

---

## 🧪 Teste a API

```bash
# Health check
curl http://localhost:5001/health

# Criar usuário
curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste",
    "email": "teste@email.com",
    "password": "senha12345"
  }'

# Login
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@email.com",
    "password": "senha12345"
  }'
```

---

## 📋 Checklist Mínimo

- [ ] PostgreSQL instalado e rodando
- [ ] Banco `meu_banco` criado
- [ ] Arquivo `.env` configurado com `POSTGRES_PASSWORD`
- [ ] Migração executada (`migration_fix_usuarios.sql`)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)

---

## ⚠️ Problemas Comuns

### Erro: "Falha ao conectar ao PostgreSQL"
```bash
# Verifique se o PostgreSQL está rodando
sudo service postgresql status  # Linux
brew services list              # Mac

# Teste conexão manual
psql -U postgres -d meu_banco
```

### Erro: "POSTGRES_PASSWORD é obrigatório"
```bash
# Adicione no .env:
echo "POSTGRES_PASSWORD=sua_senha_aqui" >> .env
```

### Erro: "Módulo não encontrado"
```bash
# Instale dependências novamente
pip install -r requirements.txt
```

### Porta 5001 já está em uso
```bash
# Mude a porta no app.py (última linha)
app.run(host='0.0.0.0', port=5002, debug=config.DEBUG)
```

---

## 📚 Documentação Completa

Veja `README.md` para:
- Todos os endpoints da API
- Exemplos de uso com JWT
- Configurações avançadas
- Deploy em produção
- Testes automatizados

---

## 🆘 Ajuda Rápida

**Logs:**
```bash
tail -f logs/app.log
```

**Reset do banco:**
```bash
dropdb meu_banco
createdb meu_banco
psql -U postgres -d meu_banco -f calmousql.sql
psql -U postgres -d meu_banco -f migration_fix_usuarios.sql
```

**Parar Docker:**
```bash
docker-compose down
```

---

**💡 Dica**: Leia `CORREÇÕES_APLICADAS.md` para entender todas as mudanças!
