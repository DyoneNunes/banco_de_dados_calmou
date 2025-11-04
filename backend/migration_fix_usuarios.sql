-- ==========================================
-- MIGRATION: Correção da tabela usuarios
-- Data: 2025-10-23
-- Descrição: Corrige inconsistências na coluna de senha
-- ==========================================

-- IMPORTANTE: Faça backup do banco antes de executar!
-- pg_dump meu_banco > backup_antes_migration.sql

\connect meu_banco

BEGIN;

-- Passo 1: Verificar se a coluna password_hash existe e está vazia
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'usuarios'
        AND column_name = 'password_hash'
    ) THEN
        -- Passo 2: Copiar dados de nomedatabelasenha para password_hash
        UPDATE usuarios
        SET password_hash = nomedatabelasenha
        WHERE password_hash IS NULL;

        RAISE NOTICE 'Dados copiados de nomedatabelasenha para password_hash';
    END IF;
END $$;

-- Passo 3: Remover a coluna nomedatabelasenha
ALTER TABLE usuarios
DROP COLUMN IF EXISTS nomedatabelasenha;

-- Passo 4: Garantir que password_hash seja NOT NULL
ALTER TABLE usuarios
ALTER COLUMN password_hash SET NOT NULL;

-- Passo 5: Verificar a estrutura final
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'usuarios'
ORDER BY ordinal_position;

COMMIT;

-- ==========================================
-- FIM DA MIGRATION
-- ==========================================
-- Após executar, verifique se os usuários ainda conseguem fazer login
-- Teste: SELECT id, nome, email, password_hash FROM usuarios LIMIT 5;
