from interfaceConfig import *

# classe para a opção de saque
class Saque(object):
    def __init__(self, janela, usuario):
        self.janela = janela
        self.usuario = usuario[0]
        self.conta = usuario[1]
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

            
        # pega o saldo do usuário
        self.valorDisponivel = float(self.usuario[9])

        # armazena o texto para colocar no label referente ao saldo disponível
        dispo = 'Valor disponível para saque: R$ {:.2f}'.format(self.valorDisponivel)
        
        # define label principal do topo
        self.lbt = Label(janela, text='Saque', bg=corFundo, fg=corLetraNome, font=("Verdana", 20))
        self.lbt.place(x=350, y=10)

        # define label informando saldo disponível
        self.lbtDisponivel = Label(janela, text=dispo, bg=corFundo, fg=corLetra, font=('verdana', 15))
        self.lbtDisponivel.place(x=100, y=100)

        # define label pedindo o valor de saque
        self.lbtInfo = Label(janela, text='Informe o valor de saque:  R$', bg=corFundo, fg=corLetra, font=('verdana', 20))
        self.lbtInfo.place(x=100, y=200)

        # define a caixa de texto do valor de saque
        self.entSaque = Entry(janela, width='10', font=('verdana', 18))
        self.entSaque.place(x=510, y=200)

        # define o botão de saque
        self.btSaque = Button(janela, text='Sacar', width='10', height='3', bg='#115', fg='white',
                              font=('verdana', 15), command=self.sacar)
        self.btSaque.place(x=300, y=300)

        # define os botões de voltar a tela de operações ou voltar para a tela de login
        self.btVoltar = Button(janela, text='Voltar', width='5', height='2', bg='#115', fg='white',
                               font=('verdana', 15), command=self.voltar)
        self.btVoltar.place(x=100, y=500)

        self.btSair = Button(janela, text='Sair', width='5', height='2', bg='#115', fg='white', font=('verdana', 15),
                             command=self.exit)
        self.btSair.place(x=200, y=500)
        
    # função de sacar
    def sacar(self):
        #pega o valor digitado na caixa de texto de valor de saque
        valorDigitado = str(self.entSaque.get())
        
        if not valorDigitado.isalnum():
            messagebox.showinfo('Informação', 'O campo de saque precisa ser preenchido')

        # caso a caixa não esteja vazia
        else:
            
            # vetor contendo valores que serão enviados ao servidor [operacao, numContaRem, numContaDest, valor, senha]
            vetor = [1, self.conta, None, int(valorDigitado), None]

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

                # caso o servidor tenha retornado sucesso no saque
                if msg[0] == 0:
                    messagebox.showinfo('Informação', 'Saque realizado com sucesso')
                    self.valorDisponivel = msg[9]
                    msg[9] = int(msg[9]) - int(valorDigitado)
                    self.voltar()
                    # apaga as informações dos campos

                # caso o servidor tenha retornado que não tem notas disponíveis
                if msg[0] == 1:
                    messagebox.showerror('Erro', 'Não foi possível sacar o valor com as notas disponíveis')
                    self.apagaCampos()
                
                # caso o servidor tenha retornado que não tem saldo suficiente para saque
                if msg[0] == 2:
                    messagebox.showerror('Erro', 'Não há saldo suficiente para saque')
                    self.apagaCampos()
                
                #caso o servidor tenha retornado que não foi possível realizar saque
                if msg[0] == 3:
                    messagebox.showerror('Erro', 'Não foi possível realizar saque')
                    self.apagaCampos()
            except:
                messagebox.showerror('Erro', 'Não foi possível acessar o servidor')
                exit()
    # função para apagar os campos de texto
    def apagaCampos(self):
        self.entSaque.delete(0, END)
        self.entSaque.insert(0, '')

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