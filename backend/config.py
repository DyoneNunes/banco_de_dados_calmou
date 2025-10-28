"""
Configurações centralizadas da aplicação Calmou
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class Config:
    """Configurações base da aplicação"""

    # --- Flask ---
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'development')

    # --- Database ---
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'meu_banco')

    # --- JWT ---
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'

    # --- CORS ---
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:*,http://127.0.0.1:*').split(',')

    # --- Rate Limiting ---
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per minute')
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')

    # --- Logging ---
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))

    # --- Security ---
    BCRYPT_LOG_ROUNDS = int(os.getenv('BCRYPT_LOG_ROUNDS', 12))
    PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', 8))

    # --- Application ---
    APP_NAME = 'Calmou API'
    APP_VERSION = '1.0.0'

    @staticmethod
    def validate():
        """Valida configurações obrigatórias"""
        required = ['POSTGRES_PASSWORD']
        missing = [key for key in required if not os.getenv(key)]

        if missing:
            raise ValueError(
                f"❌ Configurações obrigatórias ausentes no .env: {', '.join(missing)}"
            )


class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    ENV = 'production'

    # Força HTTPS em produção
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # CORS mais restritivo
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')

    @staticmethod
    def validate():
        """Validação adicional para produção"""
        Config.validate()

        # Em produção, SECRET_KEY não pode ser o padrão
        if Config.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError(
                "❌ SECRET_KEY deve ser definido em produção!"
            )

        # JWT_SECRET_KEY também não pode ser padrão
        if Config.JWT_SECRET_KEY == Config.SECRET_KEY:
            raise ValueError(
                "❌ JWT_SECRET_KEY deve ser diferente de SECRET_KEY em produção!"
            )


class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    DEBUG = True
    POSTGRES_DB = 'meu_banco_test'
    RATELIMIT_ENABLED = False


# Mapeamento de ambientes
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Retorna a configuração apropriada baseada no ambiente"""
    env = os.getenv('FLASK_ENV', 'development')
    config = config_by_name.get(env, DevelopmentConfig)

    # Valida configurações
    config.validate()

    return config
