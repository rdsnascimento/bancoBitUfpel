from interfaceConfig import *

# classe para a opção de pagamento
class Pagamento(object):
    def __init__(self, janela, usuario):
        self.janela = janela
        self.usuario = usuario[0]
        self.conta = usuario[1]

        # pega o saldo do usuário
        self.valorDisponivel = float(self.usuario[9])

        # armazena o texto para colocar no label referente ao saldo disponível
        self.dispo = 'Valor disponível para pagamentos: R$ {:.2f}'.format(self.valorDisponivel)

        # define a mensagem do topo
        self.lbt = Label(janela, text='Pagamentos', bg=corFundo, fg=corLetraNome, font=("Verdana", 20))
        self.lbt.place(x=350, y=10)

        # define o label do valor disponível
        self.lbtDisponivel = Label(janela, text=self.dispo, bg=corFundo, fg=corLetra, font=('verdana', 15))
        self.lbtDisponivel.place(x=100, y=100)

        # define o label pedindo o código de barras
        self.lbtInfo = Label(janela, text='Informe o código de barras:', bg=corFundo, fg=corLetra, font=('verdana', 20))
        self.lbtInfo.place(x=200, y=200)

        # define a caixa de texto do código de barras
        self.entCodigo = Entry(janela, width='57', font=('verdana', 15))
        self.entCodigo.place(x=25, y=250)

        # define o label pedindo o valor de pagamento
        self.lbtInfo = Label(janela, text='Informe o valor do pagamento:  R$', bg=corFundo, fg=corLetra, font=('verdana', 20))
        self.lbtInfo.place(x=100, y=300)

        # define a caixa de texto do valor a ser pago
        self.entValor = Entry(janela, width='10', font=('verdana', 18))
        self.entValor.place(x=525, y=300)

        # defina o botão de pagar
        self.btSaque = Button(janela, text='Pagar', width='10', height='3', bg='#115', fg='white',
                              font=('verdana', 15), command=self.pagar)
        self.btSaque.place(x=300, y=400)

        # define o botão de voltar
        self.btVoltar = Button(janela, text='Voltar', width='5', height='2', bg='#115', fg='white',
                               font=('verdana', 15), command=self.voltar)
        self.btVoltar.place(x=100, y=500)

        # define o botão de sair
        self.btSair = Button(janela, text='Sair', width='5', height='2', bg='#115', fg='white',
                             font=('verdana', 15), command=self.exit)
        self.btSair.place(x=200, y=500)

    # função de pagar
    def pagar(self):
        # pegando os valores que estão nos campos
        valorDigitado = str(self.entValor.get())
        codigoBarras = str(self.entCodigo.get())

        # caso algum dos campos esteja vazio
        if not valorDigitado.isalnum() or not codigoBarras.isalnum():
            messagebox.showinfo('Informação', 'Todos os campos precisam ser preenchidos.')

        # caso todos os campos estejam preenchidos
        else:
            vetor = [6, self.conta, None, float(valorDigitado), None]

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

                if msg[0] == 0:
                    messagebox.showinfo('Informação', 'Pagamento realizado')
                    self.voltar()
                if msg[0] == 1:
                    messagebox.showerror('Erro', 'Não há saldo suficiente para o pagamento')
                    self.entValor.delete(0, END)
                    self.entValor.insert(0, '')
                if msg[0] == 2:
                    messagebox.showerror('Erro', 'Pagamento não realizado')
                    self.entValor.delete(0, END)
                    self.entValor.insert(0, '')
            except:
                messagebox.showerror('Erro', 'Não foi possível acessar o servidor')
                exit()
    # funções de voltar para a tela anterior ou voltar para o login
    def voltar(self):
        operation[0] = '5'
        self.janela.destroy()

    def exit(self):
        messagebox.showinfo('Informação', 'Saindo...')
        operation[0] = '0'
        self.janela.destroy()

# quando cair nos casos de voltar ou sair, retornará a opção escolhida
def main(usuario):
    inicio(Pagamento, usuario)
    return operation[0]