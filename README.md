# banco-bit-ufpel
Trabalho da disciplina de Redes de Computadores. Criação de um banco fictício onde há interação entre cliente e servidor. O projeto foi realizado em Python, por Gleider Campos e Rafael Nascimento.

# Como executar no Linux
Para executar o cliente em ambiente linux, é só ir na raíz do projeto e digitar:

       >> sh cliente.sh

Para executar o servidor:

       >> sh servidor.sh

Isso executará o script.

Foram, cadastrados 11 clientes no banco (todos com a senha 123456), para facilitar os nossos testes, embora pudessem receber qualquer senha alfanumérica na hora do cadastramento. Para cadastro de novos clientes basta executar servidor/cadastro.py

# O que precisa para rodar?
1. Python3

2. TKinter para python3. Caso não tenha digitar:

       >> apt-get install python3-tk

3. Pacote de criptografia. Para instalar

       >> pip3 install cryptography

4. Sqlite3 (apenas para o lado do servidor). Para instalar:

       >> apt-get install libsqlite3-dev
       
5. Bcrypt para python3 (apenas para o lado do servidor). Para Debian e Ubuntu, o seguinte comando garante as dependências necessárias do Bcrypt sejam instaladas:
       
       >> apt-get install build-essential libffi-dev python-dev

5.1 Para instalar o Bcrypt:
       
       >> pip3 install bcrypt

5.2 Caso não tenha o pip (gerenciador de pacotes do Python):

       >> apt-get install python3-pip
