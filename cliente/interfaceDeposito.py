from interfaceConfig import *

# classe para a opção de saque
class Saque(object):
    def __init__(self, janela, usuario):
        self.janela = janela
        self.usuario = usuario[0]
        self.conta = usuario[1]

        # armazena o texto para colocar no label referente ao saldo disponível
        self.dispo = 'Valor disponível: R$ {}'.format(float(self.usuario[9]))

        # pega o saldo do usuário
        self.valorDisponivel = float(self.usuario[9])

        # define a mensagem do topo
        self.lbt = Label(janela, text='Depósito', bg=corFundo, fg=corLetraNome, font=("Verdana", 20))
        self.lbt.place(x=350, y=10)

        # define o label sobre o saldo disponível
        self.lbtDisponivel = Label(janela, text=self.dispo, bg=corFundo, fg=corLetra, font=('verdana', 15))
        self.lbtDisponivel.place(x=100, y=100)

        # define o label sobre o valor de depósito
        self.lbtInfo = Label(janela, text='Informe o valor de depósito:  R$', bg=corFundo, fg=corLetra, font=('verdana', 20))
        self.lbtInfo.place(x=100, y=200)

        # define a caixa de texto do valor de depósito
        self.entDeposito = Entry(janela, width='10', font=('verdana', 18))
        self.entDeposito.place(x=545, y=200)

        # define o botão de depósito
        self.btSaque = Button(janela, text='Depositar', width='10', height='3', bg='#115', fg='white',
                              font=('verdana', 15), command=self.depositar)
        self.btSaque.place(x=300, y=300)

        # define o botão de voltar
        self.btVoltar = Button(janela, text='Voltar', width='5', height='2', bg='#115', fg='white',
                               font=('verdana', 15), command=self.voltar)
        self.btVoltar.place(x=100, y=500)

        # define o botão de sair
        self.btSair = Button(janela, text='Sair', width='5', height='2', bg='#115', fg='white',
                             font=('verdana', 15), command=self.exit)
        self.btSair.place(x=200, y=500)

    # função depositar
    def depositar(self):
        # pega o valor digitado na caixa de texto
        valorDigitado = str(self.entDeposito.get())

        # caso a caixa de texto esteja vazia
        if not valorDigitado.isalnum():
            messagebox.showinfo('Informação', 'O campo de depósito precisa ser preenchido')

        # caso a caixa de texto não esteja vazia
        else:
            # vetor contendo valores que serão enviados ao servidor [operacao, numContaRem, numContaDest, valor, senha]
            vetor = [2, self.conta, None, int(valorDigitado), None]

            # transforma objeto em sequência de byte
            s = pickle.dumps(vetor)
        
            # criptografa a mensagem
            s = criptografar(s) 

            try:
                # envia a mensagem criptografada
                clientSocket.sendall(s) 

                # recebe o retorno
                msg = clientSocket.recv(2048)

                # decriptogrando mensagem
                msg = decriptografar(msg) 

                #transforma a sequência de byte em objeto
                msg = pickle.loads(msg)

                # caso retorne do servidor que o depósito foi realizado com sucesso
                if msg[0] == 0:
                    messagebox.showinfo('Informação', 'Depósito realizado com sucesso')
                    self.valorDisponivel = msg[9]
                    self.lbtDisponivel['text'] = 'Valor disponível: R$ {:.2f}'.format(float(self.valorDisponivel))
                    self.voltar()
                
                # caso retorne do servidor que o depósito não foi realizado com sucesso
                else:
                    messagebox.showerror('Erro', 'Não foi possível realizar o depósito')
                    self.entDeposito.delete(0, END)
                    self.entDeposito.insert(0, '')
            except:
                messagebox.showerror('Erro', 'Não foi possível acessar o servidor')
                exit()
    # funções de voltar para a tela de operações ou voltar para a tela de login
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