from interfaceConfig import *

# classe de saque
class Saque(object):
    def __init__(self, janela, usuario):
        self.janela = janela
        self.conta = usuario[1]
    # vetor contendo valores que serão enviados ao servidor [operacao, numContaRem, numContaDest, valor, senha]
        vetor = [5, self.conta, None, None, None]

        # transforma objeto em sequência de byte
        s = pickle.dumps(vetor)
    
        # criptografa a mensagem
        s = criptografar(s) 

        # envia a mensagem criptografada
        clientSocket.sendall(s) 

        # recebe o retorno
        self.usuario = clientSocket.recv(2048)

        # decriptogrando mensagem
        self.usuario = decriptografar(self.usuario) 

        #transforma a sequência de byte em objeto
        self.usuario = pickle.loads(self.usuario)
        
        if self.usuario[0] == 0:
            # armazena o texto para colocar no label referente ao saldo disponível
            self.valorDisponivel = self.usuario[9]

            # pega informações do usuário e salva nas variáveis da classe
            self.dispo = 'Valor disponível: R$ {:.2f}'.format(float(self.valorDisponivel))
            if self.usuario[1] == None:
                self.user = '-'
            else:
                self.user = self.usuario[1]
            if self.usuario[2] == None:
                self.cpf = '-'
            else:
                self.cpf = self.usuario[2]
            if self.usuario[3] == None:
                self.end = '-'
            else:
                self.end = self.usuario[3]
            if self.usuario[5] == None:
                self.bairro = '-'
            else:
                self.bairro = self.usuario[5]
            if self.usuario[6] == None:
                self.cidade = '-'
            else:
                self.cidade = self.usuario[6]
            if self.usuario[7] == None:
                self.uf = '-'
            else:
                self.uf = self.usuario[7]
            if self.usuario[8] == None:
                self.cep = '-'
            else:
                self.cep = self.usuario[8]
            

            # define o label principal do topo
            self.lbt = Label(janela, text='Informações cadastrais', bg=corFundo, fg=corLetraNome, font=("Verdana", 20))
            self.lbt.place(x=250, y=10)

            # define o label Nome
            self.lbtNome = Label(janela, text='Nome: ' + self.user, bg=corFundo, fg=corLetra, font=('Verdana', 20))
            self.lbtNome.place(x=200, y=60)

            # define o label CPF
            self.lbtCpf = Label(janela, text='CPF: ' + self.cpf, bg=corFundo, fg=corLetra, font=('Verdana', 20))
            self.lbtCpf.place(x=200, y=110)

            # define o label Endereço
            self.lbtEnd = Label(janela, text='Endereço: ' + self.end, bg=corFundo, fg=corLetra, font=('Verdana', 20))
            self.lbtEnd.place(x=200, y=160)

            self.lbtBairro = Label(janela, text='Bairro: ' + self.bairro, bg=corFundo, fg=corLetra, font=('Verdana', 20))
            self.lbtBairro.place(x=200, y=210)

            self.lbtCidade = Label(janela, text='Cidade: ' + self.cidade, bg=corFundo, fg=corLetra, font=('Verdana', 20))
            self.lbtCidade.place(x=200, y=260)

            self.lbtEstado = Label(janela, text='Estado: ' + self.uf, bg=corFundo, fg=corLetra, font=('Verdana', 20))
            self.lbtEstado.place(x=200, y=310)

            self.lbtCep = Label(janela, text='CEP: ' + self.cep, bg=corFundo, fg=corLetra, font=('Verdana', 20))
            self.lbtCep.place(x=200, y=360)

            # define o label Conta
            self.lbtConta = Label(janela, text='Conta: ' + str(self.conta), bg=corFundo, fg=corLetra, font=('Verdana', 20))
            self.lbtConta.place(x=200, y=410)

            # define o label com o saldo disponível
            self.lbtDisponivel = Label(janela, text=self.dispo, bg=corFundo, fg=corLetra, font=('verdana', 20))
            self.lbtDisponivel.place(x=200, y=460)

            # define o botão  voltar
            self.btVoltar = Button(janela, text='Voltar', width='5', height='2', bg='#115', fg='white',
                                font=('verdana', 15), command=self.voltar)
            self.btVoltar.place(x=100, y=500)

            # define o botão sair
            self.btSair = Button(janela, text='Sair', width='5', height='2', bg='#115', fg='white',
                                font=('verdana', 15), command=self.exit)
            self.btSair.place(x=200, y=500)

        else:
            messagebox.showerror('Erro', 'Não foi possível acessar as informações cadastrais')
            self.voltar()

    # define as funções de voltar para a tela de operações ou para a tela de login
    def voltar(self):
        operation[0] = '5'
        self.janela.destroy()

    def exit(self):
        messagebox.showinfo('Informação', 'Saindo...')
        operation[0] = '0'
        self.janela.destroy()

# quando cair nos casos de voltar ou sair, retornará a opção escolhida
def main(usuario):
    inicio(Saque, usuario)
    return operation[0]