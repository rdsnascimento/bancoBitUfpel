from tkinter import messagebox

import interfaceDeposito
import interfaceLogin
import interfaceOperacoes
import interfacePagamento
import interfaceSaldo
import interfaceSaque
import interfaceTransferencia
from testeUsuarios import *
from interfaceConfig import *

def atualizarInfo(conta):
    vetor = [5, conta, None, None, None]

    # transforma objeto em sequência de byte
    s = pickle.dumps(vetor)

    # criptografa a mensagem
    s = criptografar(s) 
    try:
        # envia a mensagem criptografada
        clientSocket.sendall(s) 

        # recebe o retorno
        usuario = clientSocket.recv(2048)

        # decriptogrando mensagem
        usuario = decriptografar(usuario) 

        #transforma a sequência de byte em objeto
        usuario = pickle.loads(usuario)

        return usuario
    except:
        messagebox.showerror('Erro', 'Não foi possível acessar o servidor')
        exit()
# importa as classes referente as opções do terminal e a tela de login
# programa começa aqui, ele fica rodando até ser uma opção de login inválida
while True:
    usuarios = []
    # pega informações digitadas na tela de login, retorna um dicionário referente ao usuário
    login = interfaceLogin.main(usuarios)
    # caso o usuário seja válido
    if len(login) > 0:
        # entra no terminal de operações, vai retornar uma das opções escolhidas
        op = interfaceOperacoes.main(login)
        login[0] = atualizarInfo(login[1])
        # enquanto a opção não seja de voltar para o login, ficará rodando em uma das opções do terminal
        while op != '0':
            # caso a opção seja de saque
            if op == '1':
                op = interfaceSaque.main(login)
                login[0] = atualizarInfo(login[1])

            # caso a opção seja de depósito
            if op == '2':
                op = interfaceDeposito.main(login)
                login[0] = atualizarInfo(login[1])

            # caso a opção seja de saldo
            if op == '3':
                op = interfaceSaldo.main(login)
                login[0] = atualizarInfo(login[1])

            # caso a opção seja de transferência
            if op == '4':
                op = interfaceTransferencia.main(login)
                login[0] = atualizarInfo(login[1])

            # caso a opção seja de pagamento
            if op == '6':
                op = interfacePagamento.main(login)
                login[0] = atualizarInfo(login[1])

            # caso a opção dentro de uma das operações seja voltar, isso fará ir para as operações novamente
            if op == '5':
                op = interfaceOperacoes.main(login)
                login[0] = atualizarInfo(login[1])

    # caso a opção seja não especificada ou decida sair, encerra o programa
    else:
        break


