from interfaceConfig import *

login = []

# classe para o login
class Login(object):
    def __init__(self, janela, usuarios):
        self.usuarios = usuarios
        self.janela = janela
       
        # armazena o texto para colocar no label referente ao texto superior
        self.lbt = Label(janela, text='Tela de Login', bg=corFundo, fg=corLetra, font=("Verdana", 24))
        self.lbt.place(x=300, y=50)

        # define o campo de texto referente ao número da conta
        self.entLogin = Entry(janela, width='18', font=('verdana', 18))
        self.entLogin.place(x=300, y=200)

        # define o campo de texto referente a senha
        self.entSenha = Entry(janela, show="*", width='18', font=('verdana', 18))
        self.entSenha.place(x=300, y=300)

        # define a label com o texto Login
        self.lbLogin = Label(janela, text="Conta", bg=corFundo, fg=corLetra, font=('verdana', 20))
        self.lbLogin.place(x=200, y=200)

        # define a label com o texto senha
        self.lbSenha = Label(janela, text="Senha", bg=corFundo, fg=corLetra, font=('verdana', 20))
        self.lbSenha.place(x=200, y=300)

        # define o botão entrar
        self.btEntrar = Button(janela, text="Entrar", bg="#115", fg="white", width='8', height='3',
                               font=('verdana', 20), command=self.entrar)
        self.btEntrar.place(x=350, y=400)

        # define o botão sair
        self.btSair = Button(janela, text="Sair", bg="#115", fg="white", width='10', height='3', command=self.exit)
        self.btSair.place(x=50, y=450)

    # função para solicitar acesso de usuário no servidor
    def entrar(self):
        # pega as informações inseridas nos campos de texto
        numConta = str(self.entLogin.get())
        senhaCripto = str.encode(self.entSenha.get())

        if len(numConta) == 0 or len(senhaCripto) == 0:
            messagebox.showinfo('Informação', 'Todos os campos precisam ser preenchidos')
        else:
            # vetor contendo valores enviados ao servidor [operacao, numContaRem, numContaDest, valor, senha]
            vetor = [0, numConta, None, None, senhaCripto]
        
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

                # caso o retorno do servidor seja 0, então o login foi executado com sucesso
                if(msg[0] == 0):
                    messagebox.showinfo('Informação', 'Login executado com sucesso')

                    # adiciona o retorno do servidor [0] e o número da conta [1]
                    login.append(msg)
                    login.append(vetor[1])
                    
                    self.janela.destroy()

                # caso o retorno do servidor seja 1, então ocorreu um erro ao tentar acessar a conta
                else:
                    messagebox.showinfo('Informação', 'Erro ao tentar acessar a conta')
            except:
                messagebox.showerror('Erro', 'Não foi possível acessar o servidor')
                exit()
    # função para encerrar a aplicação
    def exit(self):
        messagebox.showinfo('Informação', 'Saindo...')
        exit()

    

# quando o login for feito com sucesso, irá retornar o vetor contendo as informações da conta
def main(usuarios):
    inicio(Login, usuarios)
    return login



