from tkinter import *
from tkinter import messagebox

from cryptography.fernet import Fernet
import base64, pickle
from socket import *

# módulo contendo as configurações padrões

# define a opção inicial para todas as telas
operation = ['0']

try:
    serverName='192.168.0.7'
    serverPort= 1024
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

except:
    messagebox.showinfo('Informação', 'Sistema fora do ar')
    exit()


# definição das cores usadas
corFundo = '#005'
corLetra = 'white'
corLetraNome = '#AAA'

#chave criptografica
key = base64.urlsafe_b64encode(b'BANCOBITUFPEL0123456789ABCDEFGHI') 

# número da conta e senha do login, são armazenados aqui para outras classes da interface ter acesso
numConta = 0

# função de inicialização em todas as telas
def inicio(object, usuario=None):
    # inicializa janela principal
    janela = Tk()

    # define o título da janela
    janela.title('Banco Bit-Ufpel')

    # faz com que a janela não seja redimensionável
    janela.resizable(False, False)

    # adiciona cor de fundo na janela
    janela.configure(background=corFundo)  # define cor de fundo da janela

    # define as dimensões da janela, centralizando no monitor independente do tamanho da tela
    w = 800
    h = 600
    ws = janela.winfo_screenwidth()
    hs = janela.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    janela.geometry('{}x{}+{}+{}'.format(int(w), int(h), int(x), int(y)))  # define tamanho da janela


    # envia qual a classe será iniciada
    object(janela, usuario)

    # faz com a janela apareça na tela
    janela.mainloop()

# funções para critografar e decriptografar as mensagens do servidor
def criptografar(conteudo):
        result = Fernet(key)
        return result.encrypt(conteudo)

def decriptografar(conteudo):
        result = Fernet(key)
        return result.decrypt(conteudo)