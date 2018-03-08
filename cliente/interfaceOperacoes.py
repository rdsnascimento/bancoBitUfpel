from interfaceConfig import *
# variável referente a opção escolhida
operation = ['0']

#classe para o menu de operações
class Operacoes(object):
    def __init__(self, janela, usuario):
        self.usuario = usuario[0]
        self.janela = janela
        
        # armazena o nome completo
        nome = self.usuario[1]

        # coloca o nome do usuário no topo
        self.lbt = Label(janela, text=nome, bg=corFundo, fg=corLetraNome, font=("Verdana", 20))
        self.lbt.place(x=300, y=50)
        # botão de saque
        self.saque = Button(janela, text='Saque', width='15', height='3', bg='#115', fg='white',
                            font=('verdana', 15), command=self.sacar)
        self.saque.place(x=125, y=140)
        # botão de depósito
        self.deposito = Button(janela, text='Depósito', width='15', height='3', bg='#115', fg='white',
                               font=('verdana', 15), command=self.depositar)
        self.deposito.place(x=125, y=260)
        # botão de pagamentos
        self.pagamentos = Button(janela, text='Pagamentos', width='15', height='3', bg='#115', fg='white',
                                 font=('verdana', 15), command=self.pagamento)
        self.pagamentos.place(x=125, y=380)
        # botão de saldo
        self.saldo = Button(janela, text='Saldo', width='15',height='3', bg='#115', fg='white',
                            font=('verdana', 15), command=self.saldo)
        self.saldo.place(x=450, y=140)
        # botão de transferência
        self.transferencia = Button(janela, text='Transferência', width='15', height='3',bg='#115', fg='white',
                                    font=('verdana', 15), command=self.transferencia)
        self.transferencia.place(x=450, y=260)
        # botão de sair
        self.sair = Button(janela, text='Sair', width='15', height='3', bg='#115', fg='white', font=('verdana', 15),
                           command=self.exit)
        self.sair.place(x=450, y=380)

    # funções referentes a opção selecionada pelo usuário
    # a função .destroy() faz com que a janela desapareça, fazendo o ciclo do programa voltar para o main()
    def sacar(self):
        operation[0] = '1'
        self.janela.destroy()

    def depositar(self):
        operation[0] = '2'
        self.janela.destroy()

    def saldo(self):
        operation[0] = '3'
        self.janela.destroy()

    def transferencia(self):
        operation[0] = '4'
        self.janela.destroy()

    def pagamento(self):
        operation[0] = '6'
        self.janela.destroy()

    def exit(self):
        messagebox.showinfo('Informação', 'Saindo...')
        operation[0] = '0'
        self.janela.destroy()

# inicio() está definido no módulo interfaceConfig.py
# quando a janela é destruída, é retornado a operação selecionada.
# Essa operação é tratada no módulo interfacePrincipal.py
def main(usuario):
    inicio(Operacoes, usuario)
    return operation[0]
