import datetime
from abc import ABC, abstractmethod

# Constantes globais
AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500

class Historico:
    """
    Classe para armazenar o histórico de transações de uma conta.
    """
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

class Transacao(ABC):
    """
    Classe abstrata para definir a interface de uma transação.
    """
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    """
    Classe para representar uma transação de depósito.
    """
    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    """
    Classe para representar uma transação de saque.
    """
    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Conta:
    """
    Classe base para representar uma conta bancária.
    """
    def __init__(self, cliente, numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = AGENCIA
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    """
    Classe para representar uma conta corrente, que herda de Conta.
    Adiciona limites de saque.
    """
    def __init__(self, cliente, numero, limite=LIMITE_VALOR_SAQUE, limite_saques=LIMITE_SAQUES):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        numero_saques = self._numero_saques
        limite_saques = self.limite_saques

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques diários excedido. @@@")
        else:
            return super().sacar(valor)
        return False

class Cliente:
    """
    Classe para representar um cliente, que pode ter múltiplas contas.
    """
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    """
    Classe para representar um cliente pessoa física, que herda de Cliente.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

def filtrar_cliente(clientes, cpf):
    """
    Função auxiliar para buscar um cliente por CPF.
    Retorna o cliente se encontrado, caso contrário, retorna None.
    """
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def filtrar_conta(cliente, numero_conta):
    """
    Função auxiliar para buscar uma conta de um cliente por número.
    Retorna a conta se encontrada, caso contrário, retorna None.
    """
    for conta in cliente.contas:
        if conta.numero == numero_conta:
            return conta
    return None

class NumeroContaManager:
    """
    Gerencia a geração de números de conta sequenciais.
    """
    def __init__(self, numero_inicial=1):
        self._proximo_numero = numero_inicial

    def obter_proximo_numero(self):
        numero = self._proximo_numero
        self._proximo_numero += 1
        return numero

def depositar_flow(clientes):
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    num_conta = int(input("Informe o número da conta: "))
    conta = filtrar_conta(cliente, num_conta)

    if not conta:
        print("\n@@@ Conta não encontrada para este cliente! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    try:
        transacao = Deposito(valor)
        cliente.realizar_transacao(conta, transacao)
    except ValueError as e:
        print(f"\n@@@ Erro: {e} @@@")


def sacar_flow(clientes):
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    num_conta = int(input("Informe o número da conta: "))
    conta = filtrar_conta(cliente, num_conta)

    if not conta:
        print("\n@@@ Conta não encontrada para este cliente! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    try:
        transacao = Saque(valor)
        cliente.realizar_transacao(conta, transacao)
    except ValueError as e:
        print(f"\n@@@ Erro: {e} @@@")

def exibir_extrato_flow(clientes):
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    num_conta = int(input("Informe o número da conta: "))
    conta = filtrar_conta(cliente, num_conta)

    if not conta:
        print("\n@@@ Conta não encontrada para este cliente! @@@")
        return

    print("\n=============== EXTRATO ===============")
    print(f"Agência:\t{conta.agencia}")
    print(f"Conta:\t\t{conta.numero}")
    print(f"Cliente:\t{cliente.nome}")
    extrato = ""
    for transacao in conta.historico.transacoes:
        extrato += f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}\n"

    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo atual:\t R$ {conta.saldo:.2f}")
    print("=======================================")

def cadastrar_usuario_flow(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente_existente = filtrar_cliente(clientes, cpf)

    if cliente_existente:
        print("\n@@@ Já existe um cliente com este CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    novo_cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(novo_cliente)
    print("\n=== Cliente cadastrado com sucesso! ===")

def criar_conta_flow(clientes, contas, numero_conta_manager):
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado! Fluxo de criação de conta encerrado. @@@")
        return

    numero_conta = numero_conta_manager.obter_proximo_numero()
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")

def listar_contas_flow(contas):
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

def listar_usuarios_flow(clientes):
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


def main():
    """
    Função principal que gerencia o fluxo do programa.
    """
    clientes = []
    contas = []
    gerenciador_contas = NumeroContaManager()

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
        "d": lambda: depositar_flow(clientes),
        "s": lambda: sacar_flow(clientes),
        "e": lambda: exibir_extrato_flow(clientes),
        "nu": lambda: cadastrar_usuario_flow(clientes),
        "nc": lambda: criar_conta_flow(clientes, contas, gerenciador_contas),
        "lc": lambda: listar_contas_flow(contas),
        "lu": lambda: listar_usuarios_flow(clientes),
        "q": lambda: "Sair"
    }

    while True:
        opcao = input(menu)
        acao = opcoes_menu.get(opcao)

        if acao:
            resultado = acao()
            if resultado == "Sair":
                break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()
