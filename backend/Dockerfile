# ==================================================
# Dockerfile - Calmou Backend API
# ==================================================
# Imagem multi-stage para otimizar tamanho final

# --- STAGE 1: Builder ---
FROM python:3.11-slim as builder

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /build

# Copia requirements e instala dependências
COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt


# --- STAGE 2: Runtime ---
FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

# Instala apenas runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório da aplicação
WORKDIR /app

# Copia dependências Python do builder
COPY --from=builder /root/.local /root/.local

# Copia código da aplicação
COPY . .

# Cria diretório de logs
RUN mkdir -p /app/logs

# Para desenvolvimento, roda como root (em produção deve usar appuser)
# RUN useradd -m -u 1000 appuser
# USER appuser

# Expõe porta da aplicação
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5001/health')" || exit 1

# Comando para iniciar a aplicação
# Para desenvolvimento, use o servidor Flask
CMD ["python", "app.py"]

# Para produção, descomente a linha abaixo:
# CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
