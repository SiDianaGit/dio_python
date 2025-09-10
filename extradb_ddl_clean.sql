USE sistema_bancario;
GO

-- 1. Remove a tabela 'transacoes' (a mais dependente)
IF OBJECT_ID('dbo.transacoes', 'U') IS NOT NULL
BEGIN
    DROP TABLE transacoes;
    PRINT 'Tabela "transacoes" removida com sucesso.';
END
ELSE
BEGIN
    PRINT 'Tabela "transacoes" n�o encontrada. Nenhuma a��o necess�ria.';
END
GO

-- 2. Remove a tabela 'contas'
IF OBJECT_ID('dbo.contas', 'U') IS NOT NULL
BEGIN
    DROP TABLE contas;
    PRINT 'Tabela "contas" removida com sucesso.';
END
ELSE
BEGIN
    PRINT 'Tabela "contas" n�o encontrada. Nenhuma a��o necess�ria.';
END
GO

-- 3. Remove a tabela 'clientes' (a mais independente)
IF OBJECT_ID('dbo.clientes', 'U') IS NOT NULL
BEGIN
    DROP TABLE clientes;
    PRINT 'Tabela "clientes" removida com sucesso.';
END
ELSE
BEGIN
    PRINT 'Tabela "clientes" n�o encontrada. Nenhuma a��o necess�ria.';
END
GO