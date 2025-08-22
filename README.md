# Sistema Bancário Modularizado

Este projeto é um sistema bancário simples, desenvolvido em Python, que simula operações bancárias para múltiplos clientes e contas. O código foi modularizado em funções para uma melhor organização, legibilidade e manutenção, tornando-o um excelente exemplo de refatoração e boas práticas de programação.

---

### Funcionalidades

O sistema oferece as seguintes operações, organizadas em funções para uma estrutura mais clara:

* **Depositar (`[d]`)**: Permite depositar um valor em uma conta específica.
* **Sacar (`[s]`)**: Permite sacar um valor da conta, respeitando o limite diário de 3 saques e o valor máximo de R$ 500,00 por saque. Verifica se há saldo suficiente.
* **Visualizar Extrato (`[e]`)**: Exibe o histórico de transações (depósitos e saques) com data e hora, além do saldo atual da conta.
* **Cadastrar Usuário (`[nu]`)**: Cria um novo cliente no banco. Cada usuário é identificado de forma única pelo CPF e possui um nome, data de nascimento e endereço.
* **Criar Conta Corrente (`[nc]`)**: Cria uma nova conta corrente vinculada a um usuário existente através do CPF. A agência é fixa (`0001`) e o número da conta é sequencial, começando em 1.
* **Listar Contas (`[lc]`)**: Exibe uma lista de todas as contas cadastradas.
* **Listar Usuários (`[lu]`)**: Exibe uma lista de todos os usuários cadastrados.
* **Sair (`[q]`)**: Encerra a execução do programa.

O sistema também estabelece um limite de 10 transações (depósito ou saque) por dia para cada conta.

---

### Estrutura do Código

O código utiliza um menu interativo dentro de um loop `while` para gerenciar as operações. A lógica foi reorganizada em funções, cada uma com uma responsabilidade clara.

* Os dados dos **usuários** e **contas** são armazenados em listas, onde cada item é um dicionário contendo os atributos do respectivo objeto (ex: nome, CPF, saldo).
* As funções de `saque`, `deposito` e `extrato` agora exigem que o CPF e o número da conta sejam informados para identificar a conta correta.
* As regras de passagem de argumentos foram aplicadas, com `sacar` usando argumentos nomeados, `depositar` usando argumentos posicionais e `exibir_extrato` usando uma combinação de ambos.

---

### Tecnologias Utilizadas

* **Python 3**: Linguagem de programação principal.

---

### Como Executar

Para rodar o sistema, certifique-se de ter o Python instalado em sua máquina.

1. Salve o código em um arquivo `.py` (por exemplo, `banco.py`).
2. Abra o terminal ou prompt de comando.
3. Navegue até o diretório onde você salvou o arquivo.
4. Execute o seguinte comando:

```bash
python banco.py
```

O menu de opções será exibido, permitindo que você comece a interagir com o sistema.

---

### Melhorias Futuras

* **Persistência de Dados**: Implementar o salvamento dos dados de usuários e contas em um arquivo (como JSON) ou em um banco de dados para que as informações não sejam perdidas ao fechar o programa.
* **Classes e Orientação a Objetos**: Refatorar o código para usar classes (`Cliente`, `Conta`) para encapsular dados e comportamentos, tornando o código ainda mais robusto.
* **Interfaces**: Adicionar uma interface de usuário (GUI) com bibliotecas como `Tkinter` ou `PyQt`, ou criar uma interface web com frameworks como `Flask`.
