from interfaceConfig import *
from testeUsuarios import *

# classe para as opções de transferência
class Transferencia(object):
    def __init__(self, janela, usuario):
        self.usuario = usuario[0]
        self.janela = janela
        self.conta = usuario[1]

        # pega o saldo disponível do usuário
        self.valorDisponivel = float(self.usuario[9])

        # armazena o texto para colocar no label referente ao saldo disponível
        self.dispo = 'Valor disponível para transferência: R$ {:.2f}'.format(float(self.valorDisponivel))

        # define a mensagem do topo
        self.lbt = Label(janela, text='Transferência', bg=corFundo, fg=corLetraNome,
                         font=("Verdana", 20))
        self.lbt.place(x=350, y=10)

        # define a mensagem sobre o valor disponível
        self.lbtDisponivel = Label(janela, text=self.dispo, bg=corFundo, fg=corLetra, font=('verdana', 15))
        self.lbtDisponivel.place(x=100, y=100)

        # define o label com o texto Conta
        self.lbtConta = Label(janela, text='Conta: ', bg=corFundo, fg=corLetra, font=('verdana', 15))
        self.lbtConta.place(x=100, y=200)

        # define o campo de texto Conta
        self.entConta = Entry(janela, width='10', font=('verdana', 13))
        self.entConta.place(x=485, y=200)

        # define o label com o texto sobre o valor da transferencia
        self.lbtInfo = Label(janela, text='Informe o valor de transferência:  R$', bg=corFundo, fg=corLetra, font=('verdana', 15))
        self.lbtInfo.place(x=100, y=250)

        # define o campo de texto referente ao valor a ser digitado
        self.entValor = Entry(janela, width='10', font=('verdana', 13))
        self.entValor.place(x=485, y=250)

        # define o botão Transferir
        self.btTransferir = Button(janela, text='Transferir', width='10', height='3', bg='#115', fg='white',
                              font=('verdana', 15), command=self.transferir)
        self.btTransferir.place(x=300, y=350)

        #define o botão Voltar
        self.btVoltar = Button(janela, text='Voltar', width='5', height='2', bg='#115', fg='white',
                               font=('verdana', 15), command=self.voltar)
        self.btVoltar.place(x=100, y=500)

        #define o botão Sair
        self.btSair = Button(janela, text='Sair', width='5', height='2', bg='#115', fg='white', font=('verdana', 15),
                             command=self.exit)
        self.btSair.place(x=200, y=500)

    # função para transferir dinheiro para outra conta
    def transferir(self):
        # pegando os valores que estão nos campos
        valorDigitado = str(self.entValor.get())
        contaDigitada = str(self.entConta.get())

        # informar um alerta caso um dos campos não esteja preenchido
        if len(valorDigitado) == 0 or len(contaDigitada) == 0:
            messagebox.showinfo('Informação', 'Todos os campos precisam ser preenchidos')

        # caso todos os campos estejam preenchidos
     
        else:
            # vetor contendo valores que serão enviados ao servidor [operacao, numContaRem, numContaDest, valor, senha]
            vetor = [3, self.conta, int(contaDigitada), int(valorDigitado), None]

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
                
                # caso encontre a conta de destino
                if msg[0] == 0:
                    # pergunta se realmente quer enviar para o destinatário
                    op = messagebox.askquestion('Informação', 'Deseja fazer a transferência para:\nNome: ' + msg[10] +
                                                        '\nConta: ' + contaDigitada + '\nValor: ' + valorDigitado + ' R$')
                    # caso a resposta seja sim, envia para o servidor a solicitação
                    if op == 'yes':
                        # faz uma nova solicitação confirmando a transferência
                        vetor = [4, self.conta, int(contaDigitada), int(valorDigitado), None]

                        # transforma objeto em sequência de byte
                        s = pickle.dumps(vetor)
                    
                        # criptografa a mensagem
                        s = criptografar(s) 

                        # envia a mensagem criptografada
                        clientSocket.sendall(s) 

                        # recebe o retorno
                        msg = clientSocket.recv(2048)

                        # decriptogrando mensagem
                        msg = decriptografar(msg) 

                        #transforma a sequência de byte em objeto
                        msg = pickle.loads(msg)

                        # caso a transferência seja realizada com sucesso
                        if msg[0] == 0:
                            messagebox.showinfo('Informação', 'Transferência realizada com sucesso')
                            self.voltar()
                        # caso ocorra erro na transferência
                        else:
                            messagebox.showerror('Erro', 'Transferência não realizada')
                            self.limparCampo()
                    # caso o usuário coloque em não transferir 
                    else:
                        messagebox.showinfo('Informação', 'Transferência cancelada')
                        self.voltar()
                # caso a conta de destino não existir        
                if msg[0] == 1:
                    messagebox.showerror('Erro', 'Conta de destino inexistente')
                    self.limparCampo()
                
                # caso não tenha saldo suficiente para transferir
                if msg[0] == 2:
                    messagebox.showerror('Erro', 'Não há saldo suficiente para transferência')
                    self.limparCampo()
                
                # caso tente enviar para a própria conta
                if msg[0] == 3:
                    messagebox.showerror('Erro', 'Conta de origem e destino são as mesmas')
                    self.limparCampo()
            except:
                messagebox.showerror('Erro', 'Não foi possível acessar o servidor')
                exit()
            
    # funções de voltar para a tela de operações ou de voltar para a tela de login
    def voltar(self):
        operation[0] = '5'
        self.janela.destroy()

    def exit(self):
        messagebox.showinfo('Informação', 'Saindo...')
        operation[0] = '0'
        self.janela.destroy()

    # função que limpa os campos de texto
    def limparCampo(self):
        self.entValor.delete(0, END)
        self.entValor.insert(0, '')
        self.entConta.delete(0, END)
        self.entConta.insert(0, '')

# quando cair nos casos de voltar ou sair, retornará a opção escolhida
def main(usuario):
    inicio(Transferencia, usuario)
    return operation[0]