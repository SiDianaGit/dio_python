import datetime
from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# --- Configuração do Banco de Dados com SQLAlchemy ---

# Define a URL de conexão com o banco de dados MSSQL.
# O SQLAlchemy usa esta string para se conectar e interagir com o banco de dados.
# O `pyodbc` é o driver necessário para a conexão com o SQL Server.
DB_URL = "mssql+pyodbc://localhost\\SQLEXPRESS/sistema_bancario?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"

# Cria a "engine", que é o ponto de partida para qualquer aplicação SQLAlchemy.
# A engine é responsável por gerenciar a pool de conexões com o banco de dados.
engine = create_engine(DB_URL)

# Cria a classe `Session`, que será usada para criar sessões de banco de dados.
# Uma `session` é um objeto de trabalho que gerencia todas as operações de banco de dados.
# A `sessionmaker` é uma "fábrica" que cria essas sessões.
Session = sessionmaker(bind=engine)

# Cria uma "base declarativa" para as classes de modelo.
# O `declarative_base` é uma classe que, quando herdada, permite que você mapeie
# classes Python para tabelas de banco de dados de forma declarativa e simples.
Base = declarative_base()

# --- Definição das Classes (Mapeamento de Objetos para Tabelas) ---

# Mapeia a classe `Cliente` para a tabela "clientes" no banco de dados.
class Cliente(Base):
    # O `__tablename__` define o nome da tabela no banco de dados.
    __tablename__ = "clientes"

    # Define as colunas da tabela "clientes" e seus respectivos tipos de dados.
    # `Column` é usado para definir a coluna.
    # `Integer` para a chave primária `id`.
    id = Column(Integer, primary_key=True)
    # `String(255)` para o nome, `nullable=False` para garantir que não seja nulo.
    nome = Column(String(255), nullable=False)
    # `DateTime` para a data de nascimento.
    data_nascimento = Column(DateTime)
    # `String(14)` para o CPF, com `unique=True` para garantir unicidade.
    cpf = Column(String(14), nullable=False, unique=True)
    # `String(255)` para o endereço.
    endereco = Column(String(255), nullable=False)
    # Cria um relacionamento entre `Cliente` e `ContaCorrente`.
    # `relationship` define a relação de um para muitos (um cliente pode ter várias contas).
    # `back_populates` cria um link de volta para o cliente na classe `ContaCorrente`.
    contas = relationship("ContaCorrente", back_populates="cliente")

# Mapeia a classe `ContaCorrente` para a tabela "contas".
class ContaCorrente(Base):
    # Define o nome da tabela.
    __tablename__ = "contas"

    # Define as colunas da tabela "contas".
    id = Column(Integer, primary_key=True)
    # `String(10)` para o número da conta, com `unique=True`.
    numero = Column(String(10), nullable=False, unique=True)
    # `String(10)` para a agência.
    agencia = Column(String(10), nullable=False)
    # `Float` para o saldo, com valor padrão de 0.0.
    saldo = Column(Float, nullable=False, default=0.0)
    # `Float` para o limite de saque.
    limite_saque = Column(Float, nullable=False)
    # `Integer` para o limite de saques diários.
    limite_saques_diarios = Column(Integer, nullable=False)
    # `Integer` para a contagem de saques.
    numero_saques = Column(Integer, nullable=False, default=0)
    # `ForeignKey` cria uma chave estrangeira, vinculando a conta a um cliente.
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    # Define o relacionamento de volta para a classe `Cliente`.
    cliente = relationship("Cliente", back_populates="contas")
    # Define o relacionamento para a classe `Transacao`.
    transacoes = relationship("Transacao", back_populates="conta")

    # Define a propriedade `historico` que cria uma instância de `Historico`.
    # É um `property` para permitir o acesso como um atributo (`conta.historico`),
    # encapsulando a criação do objeto `Historico`.
    @property
    def historico(self):
        # Verifica se o atributo `_historico` já existe na instância.
        if not hasattr(self, '_historico'):
            # Se não existir, cria uma nova instância de `Historico` e a armazena.
            self._historico = Historico(self)
        # Retorna a instância de `Historico`.
        return self._historico

# Mapeia a classe `Transacao` para a tabela "transacoes".
class Transacao(Base):
    # Define o nome da tabela.
    __tablename__ = "transacoes"
    
    # Define as colunas da tabela "transacoes".
    id = Column(Integer, primary_key=True)
    # `String(50)` para o tipo de transação (ex: "Deposito", "Saque").
    tipo = Column(String(50), nullable=False)
    # `Float` para o valor da transação.
    valor = Column(Float, nullable=False)
    # `DateTime` para a data e hora da transação.
    data = Column(DateTime, nullable=False)
    # `ForeignKey` vincula a transação a uma conta.
    conta_id = Column(Integer, ForeignKey("contas.id"))

    # Define o relacionamento de volta para a classe `ContaCorrente`.
    conta = relationship("ContaCorrente", back_populates="transacoes")

# --- Classes de Negócio (Adaptadas para usar o ORM) ---

# Classe para gerenciar o histórico de transações de uma conta.
class Historico:
    # O construtor recebe uma instância de `conta`.
    def __init__(self, conta):
        self._conta = conta

    # Adiciona uma nova transação à sessão do SQLAlchemy.
    def adicionar_transacao(self, tipo, valor, session):
        try:
            # Cria uma nova instância de `Transacao` com os dados fornecidos.
            nova_transacao = Transacao(
                tipo=tipo,
                valor=valor,
                # Usa `datetime.datetime.now()` para pegar a data e hora atuais.
                data=datetime.datetime.now(),
                # Associa a transação à conta usando o objeto `conta` do SQLAlchemy.
                conta=self._conta
            )
            # Adiciona o novo objeto `Transacao` à sessão.
            # Este comando apenas prepara o objeto para ser inserido; o commit ainda não ocorreu.
            session.add(nova_transacao)
        except Exception as e:
            print(f"Erro ao adicionar transação: {e}")
            # Em caso de erro, reverte todas as operações pendentes na sessão.
            session.rollback()

# Classe base abstrata para transações, garantindo que as subclasses implementem métodos `valor` e `registrar`.
class TransacaoBase(ABC):
    # `@property` permite acessar `valor` como um atributo.
    # `@abstractmethod` força a implementação em subclasses.
    @property
    @abstractmethod
    def valor(self):
        pass

    # `@abstractmethod` força a implementação em subclasses.
    # O método `registrar` deve registrar a transação no banco de dados.
    @abstractmethod
    def registrar(self, conta, session):
        pass

# Classe `Deposito` que herda de `TransacaoBase`.
class Deposito(TransacaoBase):
    # O construtor inicializa a transação com um valor.
    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self._valor = valor

    # Implementação do método `valor` da classe base.
    @property
    def valor(self):
        return self._valor

    # Implementação do método `registrar`.
    def registrar(self, conta, session):
        try:
            # Atualiza o saldo da conta no objeto Python.
            conta.saldo += self.valor
            # Adiciona a conta à sessão para que a alteração no saldo seja rastreada.
            # Este comando apenas prepara a alteração; o commit ainda não ocorreu.
            session.add(conta)
            # Chama o método para adicionar a transação ao histórico.
            # Este comando também apenas prepara a transação para ser adicionada.
            conta.historico.adicionar_transacao("Deposito", self.valor, session)
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        except Exception as e:
            print(f"Erro ao registrar depósito: {e}")
            # Em caso de erro, reverte todas as operações pendentes na sessão.
            session.rollback()
            return False

# Classe `Saque` que herda de `TransacaoBase`.
class Saque(TransacaoBase):
    # O construtor inicializa a transação com um valor.
    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        self._valor = valor

    # Implementação do método `valor` da classe base.
    @property
    def valor(self):
        return self._valor

    # Implementação do método `registrar`.
    def registrar(self, conta, session):
        try:
            # Realiza as verificações de negócio antes de efetuar o saque.
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
                # Atualiza o saldo e o contador de saques no objeto Python.
                conta.saldo -= self.valor
                conta.numero_saques += 1
                # Adiciona a conta à sessão para que as alterações sejam rastreadas.
                # Este comando apenas prepara a alteração.
                session.add(conta)
                # Chama o método para adicionar a transação ao histórico.
                # Este comando também apenas prepara a transação para ser adicionada.
                conta.historico.adicionar_transacao("Saque", self.valor, session)
                print("\n=== Saque realizado com sucesso! ===")
                return True
            return False
        except Exception as e:
            print(f"Erro ao registrar saque: {e}")
            # Em caso de erro, reverte todas as operações pendentes na sessão.
            session.rollback()
            return False

# --- Funções de Fluxo (Atualizadas para usar o ORM) ---

# Função para buscar um cliente no banco de dados pelo CPF.
def filtrar_cliente(cpf, session):
    # Usa `session.query(Cliente)` para iniciar uma consulta na tabela `clientes`.
    # `filter_by(cpf=cpf)` filtra a consulta para encontrar um cliente com o CPF especificado.
    # `first()` retorna o primeiro resultado da consulta ou `None` se não houver.
    return session.query(Cliente).filter_by(cpf=cpf).first()

# Função para buscar uma conta no banco de dados pelo número e cliente.
def filtrar_conta(cliente, numero_conta, session):
    # Inicia uma consulta na tabela `contas`.
    # `filter_by` filtra por `numero` e `cliente`.
    # O SQLAlchemy permite a passagem do objeto `cliente` para fazer a comparação.
    return session.query(ContaCorrente).filter_by(numero=numero_conta, cliente=cliente).first()

# Fluxo principal para a operação de depósito.
def depositar_flow():
    # Cria uma nova sessão para a operação.
    session = Session()
    try:
        cpf = input("Informe o CPF do cliente (somente números): ")
        # Chama a função para buscar o cliente.
        cliente = filtrar_cliente(cpf, session)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        num_conta = input("Informe o número da conta: ")
        # Chama a função para buscar a conta.
        conta = filtrar_conta(cliente, num_conta, session)

        if not conta:
            print("\n@@@ Conta não encontrada para este cliente! @@@")
            return

        valor = float(input("Informe o valor do depósito: "))
        # Cria uma instância da classe `Deposito`.
        transacao = Deposito(valor)
        # Chama o método `registrar` para preparar a transação.
        sucesso = transacao.registrar(conta, session)
        
        # Se o registro foi bem-sucedido...
        if sucesso:
            # Realiza o commit para salvar todas as alterações pendentes no banco de dados.
            # ESTE É O PASSO DE COMMIT NO BANCO DE DADOS.
            session.commit()
        else:
            # Se o registro falhou, reverte as alterações.
            session.rollback()

    except ValueError as e:
        print(f"\n@@@ Erro: {e} @@@")
    finally:
        # Garante que a sessão seja fechada, liberando a conexão com o banco.
        session.close()

# Fluxo principal para a operação de saque.
def sacar_flow():
    # Cria uma nova sessão para a operação.
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
        # Cria uma instância da classe `Saque`.
        transacao = Saque(valor)
        # Chama o método `registrar` para preparar a transação.
        sucesso = transacao.registrar(conta, session)

        # Se o registro foi bem-sucedido...
        if sucesso:
            # Realiza o commit para salvar todas as alterações pendentes no banco de dados.
            # ESTE É O PASSO DE COMMIT NO BANCO DE DADOS.
            session.commit()
        else:
            # Se o registro falhou, reverte as alterações.
            session.rollback()

    except ValueError as e:
        print(f"\n@@@ Erro: {e} @@@")
    finally:
        # Garante que a sessão seja fechada.
        session.close()

# Fluxo para exibir o extrato de uma conta.
def exibir_extrato_flow():
    # Cria uma nova sessão para a operação.
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
        # Itera sobre a lista de transações da conta.
        # Devido ao `relationship` do SQLAlchemy, as transações são carregadas
        # automaticamente quando `conta.transacoes` é acessado.
        for transacao in conta.transacoes:
            # Formata a string de extrato para exibição.
            extrato += f"{transacao.data.strftime('%d/%m/%Y %H:%M:%S')} - {transacao.tipo}: R$ {transacao.valor:.2f}\n"

        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo atual:\t R$ {conta.saldo:.2f}")
        print("=======================================")
    finally:
        # Garante que a sessão seja fechada.
        session.close()

# Fluxo para cadastrar um novo usuário (cliente).
def cadastrar_usuario_flow():
    # Cria uma nova sessão.
    session = Session()
    try:
        cpf = input("Informe o CPF (somente números): ")
        # Verifica se o cliente já existe para evitar duplicidade.
        cliente_existente = filtrar_cliente(cpf, session)

        if cliente_existente:
            print("\n@@@ Já existe um cliente com este CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (AAAA-MM-DD): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        
        # Cria uma nova instância de `Cliente` com os dados do usuário.
        novo_cliente = Cliente(
            nome=nome,
            # Converte a string de data para um objeto `datetime`.
            data_nascimento=datetime.datetime.strptime(data_nascimento, "%Y-%m-%d"),
            cpf=cpf,
            endereco=endereco
        )
        # Adiciona o novo objeto `Cliente` à sessão.
        session.add(novo_cliente)
        # Realiza o commit para salvar o novo cliente no banco de dados.
        # ESTE É O PASSO DE COMMIT NO BANCO DE DADOS.
        session.commit()
        print("\n=== Cliente cadastrado com sucesso! ===")
    except Exception as e:
        print(f"Erro ao cadastrar cliente: {e}")
        # Em caso de erro, reverte as alterações.
        session.rollback()
    finally:
        # Garante que a sessão seja fechada.
        session.close()

# Fluxo para criar uma nova conta para um cliente existente.
def criar_conta_flow():
    # Cria uma nova sessão.
    session = Session()
    try:
        cpf = input("Informe o CPF do cliente (somente números): ")
        cliente = filtrar_cliente(cpf, session)

        if not cliente:
            print("\n@@@ Cliente não encontrado! Fluxo de criação de conta encerrado. @@@")
            return

        # Busca a última conta cadastrada para determinar o próximo número.
        # `order_by(ContaCorrente.id.desc())` ordena as contas por `id` em ordem decrescente.
        # `first()` pega a última.
        ultima_conta = session.query(ContaCorrente).order_by(ContaCorrente.id.desc()).first()
        
        if ultima_conta:
            # Incrementa o número da última conta e formata com zeros à esquerda.
            proximo_numero = str(int(ultima_conta.numero) + 1).zfill(4)
        else:
            proximo_numero = "0001"
        
        # Cria uma nova instância de `ContaCorrente`.
        nova_conta = ContaCorrente(
            numero=proximo_numero,
            agencia="0001",
            limite_saque=500.00,
            limite_saques_diarios=3,
            # Associa a conta ao objeto `cliente` do SQLAlchemy.
            cliente=cliente
        )
        # Adiciona o novo objeto `ContaCorrente` à sessão.
        session.add(nova_conta)
        # Realiza o commit para salvar a nova conta no banco de dados.
        # ESTE É O PASSO DE COMMIT NO BANCO DE DADOS.
        session.commit()
        print(f"\n=== Conta {proximo_numero} criada com sucesso para {cliente.nome}! ===")
    except Exception as e:
        print(f"Erro ao criar conta: {e}")
        # Em caso de erro, reverte as alterações.
        session.rollback()
    finally:
        # Garante que a sessão seja fechada.
        session.close()

# Fluxo para listar todas as contas cadastradas.
def listar_contas_flow():
    # Cria uma nova sessão.
    session = Session()
    try:
        # Consulta todas as contas, unindo-as com a tabela `clientes`.
        # O `join(Cliente)` permite que os dados do cliente sejam acessados diretamente.
        # `order_by(ContaCorrente.numero)` ordena a lista por número da conta.
        # `all()` retorna todos os resultados da consulta em uma lista.
        contas = session.query(ContaCorrente).join(Cliente).order_by(ContaCorrente.numero).all()
        if not contas:
            print("\n@@@ Nenhuma conta cadastrada! @@@")
        else:
            print("\n=============== CONTAS CADASTRADAS ===============")
            # Itera sobre a lista de contas para imprimir os detalhes.
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
        # Garante que a sessão seja fechada.
        session.close()

# Fluxo para listar todos os usuários (clientes) cadastrados.
def listar_usuarios_flow():
    # Cria uma nova sessão.
    session = Session()
    try:
        # Consulta todos os clientes e os ordena por nome.
        clientes = session.query(Cliente).order_by(Cliente.nome).all()
        if not clientes:
            print("\n@@@ Nenhum cliente cadastrado! @@@")
        else:
            print("\n=============== CLIENTES CADASTRADOS ===============")
            # Itera sobre a lista de clientes para imprimir os detalhes.
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
        # Garante que a sessão seja fechada.
        session.close()

# Função principal que executa o loop do menu.
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

    # Dicionário que mapeia as opções do menu para as funções correspondentes.
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

    # Loop infinito para exibir o menu até que o usuário escolha sair.
    while True:
        opcao = input(menu).lower()
        # Usa `opcoes_menu.get(opcao)` para obter a função associada à opção.
        # `get` retorna `None` se a chave não existir, evitando erros.
        acao = opcoes_menu.get(opcao)

        if acao:
            if acao == "Sair":
                break
            # Chama a função correspondente.
            acao()
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# O `if __name__ == "__main__":` garante que o código abaixo só seja executado
# quando o script é rodado diretamente (não quando é importado como módulo).
if __name__ == "__main__":
    print("Criando tabelas no banco de dados (se necessário)...")
    # `Base.metadata.create_all(engine)` cria todas as tabelas definidas pelas
    # classes que herdam de `Base`, caso elas ainda não existam no banco de dados.
    Base.metadata.create_all(engine)
    print("Tabelas prontas.")

    # Chama a função principal para iniciar a aplicação.
    main()