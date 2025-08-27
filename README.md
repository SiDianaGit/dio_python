
# Sistema de Banco Moderno em Python

Este projeto é uma simulação de um sistema bancário simples, focado em operações básicas como depósito, saque e visualização de extrato. Ele foi refatorado para usar uma arquitetura orientada a objetos, seguindo o diagrama de classes UML anexo, tornando o código mais modular, organizado e fácil de manter.

## Diagrama de Classes UML

O sistema oferece as seguintes operações:

### Principais Classes e Funções

  * **`Cliente`**: Uma classe base que representa o cliente do banco. Pode ter uma ou várias `Contas`.
  * **`PessoaFisica`**: Herda de `Cliente` e adiciona atributos específicos como `nome`, `cpf` e `data_nascimento`.
  * **`Conta`**: Classe base para contas bancárias. Gerencia o `saldo`, `número`, `agência` e o histórico de transações.
  * **`ContaCorrente`**: Herda de `Conta` e implementa a lógica de `limite` e `limite_saques` diários.
  * **`Historico`**: Responsável por armazenar e gerenciar todas as transações de uma conta.
  * **`Transacao`**: Uma classe abstrata que serve como interface para todas as transações.
  * **`Deposito`** e **`Saque`**: Classes que herdam de `Transacao` e implementam a lógica específica para registrar as respectivas operações.

## Funcionalidades do Sistema

O sistema oferece as seguintes operações através de um menu interativo:

  * **`[d]` Depositar**: Permite depositar um valor em uma conta específica.
  * **`[s]` Sacar**: Permite sacar um valor, respeitando os limites da conta corrente.
  * **`[e]` Extrato**: Exibe o extrato completo de uma conta, listando todas as transações realizadas.
  * **`[nu]` Novo Usuário**: Cadastra um novo cliente (Pessoa Física) no sistema.
  * **`[nc]` Nova Conta**: Cria uma nova conta corrente e a vincula a um cliente existente.
  * **`[lc]` Listar Contas**: Exibe uma lista de todas as contas cadastradas.
  * **`[lu]` Listar Usuários**: Exibe uma lista de todos os usuários cadastrados.
  * **`[q]` Sair**: Encerra a aplicação.

## Como Executar

Para rodar o sistema, basta ter o Python 3.8 ou superior instalado. Execute o arquivo `main.py` diretamente pelo terminal:

```bash
python desafio4.py
```

## Estrutura do Projeto

  * `desfio4.py`: Contém a lógica principal do programa, as definições de classes e a função `main` para o loop interativo.
  * `README.md`: Este arquivo, que fornece uma visão geral do projeto.
  * `UML Desafio4.jpg`: O diagrama UML que serviu de base para a arquitetura do código.

## Autor

Este projeto foi desenvolvido por: *Simone*
https://github.com/SiDianaGit

### Melhorias Futuras

* **Persistência de Dados**: Implementar o salvamento dos dados de usuários e contas em um arquivo (como JSON) ou em um banco de dados para que as informações não sejam perdidas ao fechar o programa.
* **Interfaces**: Adicionar uma interface de usuário (GUI) com bibliotecas como `Tkinter` ou `PyQt`, ou criar uma interface web com frameworks como `Flask`.
