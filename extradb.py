import datetime
from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# --- Configuração do Banco de Dados com SQLAlchemy ---
DB_URL = "mssql+pyodbc://localhost\\SQLEXPRESS/sistema_bancario?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# --- Definição das Classes (Mapeamento de Objetos para Tabelas) ---

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    data_nascimento = Column(DateTime)
    cpf = Column(String(14), nullable=False, unique=True)
    endereco = Column(String(255), nullable=False)
    contas = relationship("ContaCorrente", back_populates="cliente")

class ContaCorrente(Base):
    __tablename__ = "contas"
    id = Column(Integer, primary_key=True)
    numero = Column(String(10), nullable=False, unique=True)
    agencia = Column(String(10), nullable=False)
    saldo = Column(Float, nullable=False, default=0.0)
    limite_saque = Column(Float, nullable=False)
    limite_saques_diarios = Column(Integer, nullable=False)
    numero_saques = Column(Integer, nullable=False, default=0)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Cliente", back_populates="contas")
    transacoes = relationship("Transacao", back_populates="conta")
    
    @property
    def historico(self):
        if not hasattr(self, '_historico'):
            self._historico = Historico(self)
        return self._historico

class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True)
    tipo = Column(String(50), nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(DateTime, nullable=False)
    conta_id = Column(Integer, ForeignKey("contas.id"))

    conta = relationship("ContaCorrente", back_populates="transacoes")

# --- Classes de Negócio (Adaptadas para usar o ORM) ---

class Historico:
    def __init__(self, conta):
        self._conta = conta

    def adicionar_transacao(self, tipo, valor, session):
        try:
            nova_transacao = Transacao(
                tipo=tipo,
                valor=valor,
                data=datetime.datetime.now(),
                conta=self._conta
            )
            session.add(nova_transacao)
        except Exception as e:
            print(f"Erro ao adicionar transação: {e}")
            session.rollback()

class TransacaoBase(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta, session):
        pass

class Deposito(TransacaoBase):
    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta, session):
        try:
            conta.saldo += self.valor
            session.add(conta)
            conta.historico.adicionar_transacao("Deposito", self.valor, session)
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        except Exception as e:
            print(f"Erro ao registrar depósito: {e}")
            session.rollback()
            return False

class Saque(TransacaoBase):
    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta, session):
        try:
            excedeu_saldo = self.valor > conta.saldo
            excedeu_limite = self.valor > conta.limite_saque
            excedeu_saques = conta.numero_saques >= conta.limite_saques_diarios

            if excedeu_saldo:
                print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            elif excedeu_limite:
                print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            elif excedeu_saques:
                print("\n@@@ Operação falhou! Número máximo de saques diários excedido. @@@")
            else:
                conta.saldo -= self.valor
                conta.numero_saques += 1
                session.add(conta)
                conta.historico.adicionar_transacao("Saque", self.valor, session)
                print("\n=== Saque realizado com sucesso! ===")
                return True
            return False
        except Exception as e:
            print(f"Erro ao registrar saque: {e}")
            session.rollback()
            return False

# --- Funções de Fluxo (Atualizadas para usar o ORM) ---

def filtrar_cliente(cpf, session):
    return session.query(Cliente).filter_by(cpf=cpf).first()

def filtrar_conta(cliente, numero_conta, session):
    return session.query(ContaCorrente).filter_by(numero=numero_conta, cliente=cliente).first()

def depositar_flow():
    session = Session()
    try:
        cpf = input("Informe o CPF do cliente (somente números): ")
        cliente = filtrar_cliente(cpf, session)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        num_conta = input("Informe o número da conta: ")
        conta = filtrar_conta(cliente, num_conta, session)

        if not conta:
            print("\n@@@ Conta não encontrada para este cliente! @@@")
            return

        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)
        sucesso = transacao.registrar(conta, session)
        
        if sucesso:
            session.commit()
        else:
            session.rollback()

    except ValueError as e:
        print(f"\n@@@ Erro: {e} @@@")
    finally:
        session.close()

def sacar_flow():
    session = Session()
    try:
        cpf = input("Informe o CPF do cliente (somente números): ")
        cliente = filtrar_cliente(cpf, session)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        num_conta = input("Informe o número da conta: ")
        conta = filtrar_conta(cliente, num_conta, session)

        if not conta:
            print("\n@@@ Conta não encontrada para este cliente! @@@")
            return

        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)
        sucesso = transacao.registrar(conta, session)

        if sucesso:
            session.commit()
        else:
            session.rollback()

    except ValueError as e:
        print(f"\n@@@ Erro: {e} @@@")
    finally:
        session.close()

def exibir_extrato_flow():
    session = Session()
    try:
        cpf = input("Informe o CPF do cliente (somente números): ")
        cliente = filtrar_cliente(cpf, session)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        num_conta = input("Informe o número da conta: ")
        conta = filtrar_conta(cliente, num_conta, session)

        if not conta:
            print("\n@@@ Conta não encontrada para este cliente! @@@")
            return

        print("\n=============== EXTRATO ===============")
        print(f"Agência:\t{conta.agencia}")
        print(f"Conta:\t\t{conta.numero}")
        print(f"Cliente:\t{cliente.nome}")
        
        extrato = ""
        # Agora, a transação está ligada à conta, e o SQLAlchemy irá carregá-la
        for transacao in conta.transacoes:
            extrato += f"{transacao.data.strftime('%d/%m/%Y %H:%M:%S')} - {transacao.tipo}: R$ {transacao.valor:.2f}\n"

        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo atual:\t R$ {conta.saldo:.2f}")
        print("=======================================")
    finally:
        session.close()

def cadastrar_usuario_flow():
    session = Session()
    try:
        cpf = input("Informe o CPF (somente números): ")
        cliente_existente = filtrar_cliente(cpf, session)

        if cliente_existente:
            print("\n@@@ Já existe um cliente com este CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (AAAA-MM-DD): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        
        novo_cliente = Cliente(
            nome=nome,
            data_nascimento=datetime.datetime.strptime(data_nascimento, "%Y-%m-%d"),
            cpf=cpf,
            endereco=endereco
        )
        session.add(novo_cliente)
        session.commit()
        print("\n=== Cliente cadastrado com sucesso! ===")
    except Exception as e:
        print(f"Erro ao cadastrar cliente: {e}")
        session.rollback()
    finally:
        session.close()

def criar_conta_flow():
    session = Session()
    try:
        cpf = input("Informe o CPF do cliente (somente números): ")
        cliente = filtrar_cliente(cpf, session)

        if not cliente:
            print("\n@@@ Cliente não encontrado! Fluxo de criação de conta encerrado. @@@")
            return

        ultima_conta = session.query(ContaCorrente).order_by(ContaCorrente.id.desc()).first()
        if ultima_conta:
            proximo_numero = str(int(ultima_conta.numero) + 1).zfill(4)
        else:
            proximo_numero = "0001"
        
        nova_conta = ContaCorrente(
            numero=proximo_numero,
            agencia="0001",
            limite_saque=500.00,
            limite_saques_diarios=3,
            cliente=cliente
        )
        session.add(nova_conta)
        session.commit()
        print(f"\n=== Conta {proximo_numero} criada com sucesso para {cliente.nome}! ===")
    except Exception as e:
        print(f"Erro ao criar conta: {e}")
        session.rollback()
    finally:
        session.close()

def listar_contas_flow():
    session = Session()
    try:
        contas = session.query(ContaCorrente).join(Cliente).order_by(ContaCorrente.numero).all()
        if not contas:
            print("\n@@@ Nenhuma conta cadastrada! @@@")
        else:
            print("\n=============== CONTAS CADASTRADAS ===============")
            for conta in contas:
                print(f"""
Agência:\t{conta.agencia}
C/C:\t\t{conta.numero}
Cliente:\t{conta.cliente.nome}
CPF:\t\t{conta.cliente.cpf}
""")
            print("==================================================")
    except Exception as e:
        print(f"Erro ao listar contas: {e}")
    finally:
        session.close()

def listar_usuarios_flow():
    session = Session()
    try:
        clientes = session.query(Cliente).order_by(Cliente.nome).all()
        if not clientes:
            print("\n@@@ Nenhum cliente cadastrado! @@@")
        else:
            print("\n=============== CLIENTES CADASTRADOS ===============")
            for cliente in clientes:
                print(f"""
Nome:\t\t{cliente.nome}
CPF:\t\t{cliente.cpf}
Endereço:\t{cliente.endereco}
""")
            print("======================================================")
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
    finally:
        session.close()

def main():
    menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo usuário
    [nc] Nova conta
    [lc] Listar contas
    [lu] Listar usuários
    [q] Sair
    => """

    opcoes_menu = {
        "d": depositar_flow,
        "s": sacar_flow,
        "e": exibir_extrato_flow,
        "nu": cadastrar_usuario_flow,
        "nc": criar_conta_flow,
        "lc": listar_contas_flow,
        "lu": listar_usuarios_flow,
        "q": "Sair"
    }

    while True:
        opcao = input(menu).lower()
        acao = opcoes_menu.get(opcao)

        if acao:
            if acao == "Sair":
                break
            acao()
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    # Cria as tabelas no banco de dados se elas não existirem
    print("Criando tabelas no banco de dados (se necessário)...")
    Base.metadata.create_all(engine)
    print("Tabelas prontas.")

    main()