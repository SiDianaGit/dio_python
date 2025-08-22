# dio_python

Este README.md foi gerado para um projeto de backend em Python, que simula um sistema bancário simples com operações de depósito, saque e extrato. 

-----

### **README.md**

# DESAFIO 1 -> Sistema Bancário Simples

Este projeto é um backend simples desenvolvido em Python 3 que simula operações bancárias básicas para um único cliente. Ele foi criado como um exercício prático para solidificar conceitos de lógica de programação, controle de fluxo e manipulação de variáveis.

## 🚀 Funcionalidades

O sistema oferece as seguintes operações:

  * **Depósito**: Permite depositar valores positivos na conta. O valor é adicionado ao saldo e registrado para o extrato.
  * **Saque**: Limita o saque a 3 operações diárias, com um valor máximo de R$ 500,00 por saque. Verifica se há saldo suficiente para a transação.
  * **Extrato**: Lista todas as movimentações (depósitos e saques) realizadas na conta e exibe o saldo atual no final.
                 Mostrar no extrato a data e hora de todas as transações realizadas pela conta.
  * **Limite de Saques**: Estabelecer um limite de 10 transações diárias para uma conta
                          Se um cliente tentar fazer uma transação após atingir o limite, deve ser informado que ele excedeu o número de transações permitidas para aquele dia.


## 🛠️ Tecnologias Utilizadas

  * **Python 3**: Linguagem de programação principal.

## 💻 Como Executar

1.  Clone este repositório para a sua máquina local:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    ```
2.  Navegue até o diretório do projeto:
    ```bash
    cd seu-repositorio
    ```
3.  Execute o script Python:
    ```bash
    python app.py
    ```
    (Obs: Substitua `app.py` pelo nome do arquivo do seu código, se for diferente).

O programa será iniciado e exibirá um menu de opções no terminal para que você possa interagir com ele.

## 🧠 Lógica e Estrutura do Código

O código utiliza um loop `while` para manter o menu interativo, permitindo que o usuário realize múltiplas operações até decidir sair. As variáveis principais são:

  * `saldo`: Armazena o saldo atual da conta.
  * `extrato`: Uma string que acumula o histórico de transações, formatando os valores.
  * `numero_saques`: Contador de saques diários.
  * `limite_saques`: Constante que define o número máximo de saques por dia.

As operações de **depósito** e **saque** verificam as condições necessárias (valor positivo, saldo suficiente, limite de saque) antes de alterar o saldo e o histórico. A operação de **extrato** simplesmente exibe o conteúdo da variável `extrato` e o saldo atual, formatando a saída para o formato "R$ 999.99".

## 📚 Melhorias Futuras (Possíveis)

  * **Multiplos Clientes**: Refatorar o código para permitir a criação e gestão de múltiplas contas bancárias, utilizando classes ou dicionários para armazenar os dados de cada cliente (nome, CPF, saldo, etc.).
  * **Funções**: Organizar o código em funções (`depositar()`, `sacar()`, `exibir_extrato()`) para melhorar a modularidade e legibilidade.
  * **Interface Gráfica**: Adicionar uma interface de usuário (GUI) utilizando bibliotecas como `Tkinter` ou `PyQt`.
  * **Persistência de Dados**: Salvar os dados das contas em um arquivo (JSON, CSV) ou banco de dados para que as informações não sejam perdidas ao fechar o programa.
