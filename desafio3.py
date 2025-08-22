import datetime

# Constantes globais
AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_TRANSACOES = 10

def depositar(cpf, num_conta, saldo, valor, extrato, /):
    """
    Função que realiza um depósito na conta de um usuário.
    Recebe os argumentos por posição: cpf, num_conta, saldo, valor e extrato.
    Retorna o saldo atualizado e o extrato da conta.
    """
    if valor > 0:
        saldo += valor
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{data_hora} - Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, cpf, num_conta, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Função que realiza um saque na conta de um usuário.
    Recebe os argumentos por nome: cpf, num_conta, saldo, valor, extrato, limite, numero_saques e limite_saques.
    Retorna o saldo atualizado e o extrato da conta.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques diários excedido.")
    elif valor > 0:
        saldo -= valor
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{data_hora} - Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(cpf, num_conta, saldo, /, *, extrato):
    """
    Função que exibe o extrato da conta de um usuário.
    Recebe os argumentos por posição: cpf, num_conta, saldo.
    Recebe o argumento por nome: extrato.
    """
    print("\n=============== EXTRATO ===============")
    print(f"Conta: {num_conta}")
    print(f"CPF: {cpf}")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=======================================")

def cadastrar_usuario(usuarios):
    """
    Função que cadastra um novo usuário.
    Verifica se o CPF já está cadastrado.
    Armazena os usuários em uma lista de dicionários.
    """
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = filtrar_usuario(usuarios, cpf)

    if usuario_existente:
        print("\n@@@ Já existe um usuário com este CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("Usuário cadastrado com sucesso!")

def criar_conta_corrente(agencia, numero_conta, usuarios):
    """
    Função que cria uma nova conta corrente.
    Vincula a conta a um usuário existente através do CPF.
    Retorna a lista de contas atualizada.
    """
    cpf = input("Informe o CPF do usuário (somente números): ")
    usuario = filtrar_usuario(usuarios, cpf)

    if not usuario:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return None

    print("\nConta criada com sucesso!")
    return {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "cpf": cpf,
        "saldo": 0,
        "limite": 500,
        "extrato": "",
        "numero_saques": 0,
        "numero_transacoes": 0
    }

def filtrar_usuario(usuarios, cpf):
    """
    Função auxiliar para buscar um usuário por CPF.
    Retorna o usuário se encontrado, caso contrário, retorna None.
    """
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def filtrar_conta(contas, cpf, num_conta):
    """
    Função auxiliar para buscar uma conta por CPF e número da conta.
    Retorna a conta se encontrada, caso contrário, retorna None.
    """
    contas_filtradas = [conta for conta in contas if conta["cpf"] == cpf and conta["numero_conta"] == num_conta]
    return contas_filtradas[0] if contas_filtradas else None

def listar_contas(contas):
    """
    Função que lista todas as contas existentes.
    """
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            CPF:\t\t{conta['cpf']}
        """
        print("=" * 100)
        print(linha)

def listar_usuarios(usuarios):
    """
    Função que lista todos os usuários cadastrados.
    """
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado! @@@")
        return

    for usuario in usuarios:
        print("=" * 100)
        for chave, valor in usuario.items():
            print(f"{chave.capitalize()}:\t{valor}")

def main():
    """
    Função principal que gerencia o fluxo do programa.
    """
    usuarios = []
    contas = []
    numero_conta = 1

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

    while True:
        opcao = input(menu)

        if opcao == "d":
            # Solicita CPF e número da conta para realizar o depósito
            cpf = input("Informe o CPF do usuário: ")
            num_conta = int(input("Informe o número da conta: "))
            conta = filtrar_conta(contas, cpf, num_conta)

            if not conta:
                print("Conta não encontrada ou dados incorretos.")
                continue

            # Verifica o limite de transações diárias antes de prosseguir
            if conta["numero_transacoes"] >= LIMITE_TRANSACOES:
                print("Operação falhou! Você excedeu o número máximo de transações diárias.")
                continue

            valor = float(input("Informe o valor do depósito: "))
            conta["saldo"], conta["extrato"] = depositar(cpf, num_conta, conta["saldo"], valor, conta["extrato"])
            conta["numero_transacoes"] += 1

        elif opcao == "s":
            # Solicita CPF e número da conta para realizar o saque
            cpf = input("Informe o CPF do usuário: ")
            num_conta = int(input("Informe o número da conta: "))
            conta = filtrar_conta(contas, cpf, num_conta)

            if not conta:
                print("Conta não encontrada ou dados incorretos.")
                continue

            # Verifica o limite de transações diárias antes de prosseguir
            if conta["numero_transacoes"] >= LIMITE_TRANSACOES:
                print("Operação falhou! Você excedeu o número máximo de transações diárias.")
                continue

            valor = float(input("Informe o valor do saque: "))
            conta["saldo"], conta["extrato"], conta["numero_saques"] = sacar(
                cpf=cpf,
                num_conta=num_conta,
                saldo=conta["saldo"],
                valor=valor,
                extrato=conta["extrato"],
                limite=conta["limite"],
                numero_saques=conta["numero_saques"],
                limite_saques=LIMITE_SAQUES
            )
            conta["numero_transacoes"] += 1

        elif opcao == "e":
            # Solicita CPF e número da conta para exibir o extrato
            cpf = input("Informe o CPF do usuário: ")
            num_conta = int(input("Informe o número da conta: "))
            conta = filtrar_conta(contas, cpf, num_conta)

            if not conta:
                print("Conta não encontrada ou dados incorretos.")
                continue

            exibir_extrato(cpf, num_conta, conta["saldo"], extrato=conta["extrato"])

        elif opcao == "nu":
            # Chama a função para cadastrar um novo usuário
            cadastrar_usuario(usuarios)

        elif opcao == "nc":
            # Chama a função para criar uma nova conta
            nova_conta = criar_conta_corrente(AGENCIA, numero_conta, usuarios)
            if nova_conta:
                contas.append(nova_conta)
                numero_conta += 1

        elif opcao == "lc":
            # Lista todas as contas cadastradas
            listar_contas(contas)

        elif opcao == "lu":
            # Lista todos os usuários cadastrados
            listar_usuarios(usuarios)

        elif opcao == "q":
            # Sai do programa
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()