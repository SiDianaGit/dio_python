CREATE DATABASE sistema_bancario;
GO
USE sistema_bancario;
GO

CREATE TABLE clientes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    data_nascimento DATE,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    endereco VARCHAR(255) NOT NULL
);

---

CREATE TABLE contas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    numero VARCHAR(10) NOT NULL UNIQUE,
    agencia VARCHAR(10) NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    limite_saque DECIMAL(10, 2) NOT NULL,
    limite_saques_diarios INT NOT NULL,
    numero_saques INT NOT NULL DEFAULT 0,
    cliente_id INT,
    CONSTRAINT FK_Contas_Clientes FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

---

CREATE TABLE transacoes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    data DATETIME NOT NULL,
    conta_id INT,
    CONSTRAINT FK_Transacoes_Contas FOREIGN KEY (conta_id) REFERENCES contas(id)
);