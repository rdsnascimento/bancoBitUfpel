from cryptography.fernet import Fernet
import socket, pickle, transacoes, base64

key = base64.urlsafe_b64encode(b'BANCOBITUFPEL0123456789ABCDEFGHI') #chave criptografica

def criptografar(conteudo):
    result = Fernet(key)
    return result.encrypt(conteudo)

def decriptografar(conteudo):
    result = Fernet(key)
    return result.decrypt(conteudo)

host = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1] #IP SERVIDOR
port = 1026 #PORTA USADA
mySocket = socket.socket()
mySocket.bind((host,port))
mySocket.listen(1)

print ('Servidor Banco bitUFPEL\nConectado no ip {} e porta {}'.format(host, port))
while True:
    conn, addr = mySocket.accept()
    print ("Conectado por: " + str(addr))

    try:
        #operações feitas no servidor
        while True:
            try:
                msg = conn.recv(2048) #recebendo mensagem
                msgRetorno = [None, None, None, None, None, None, None, None, None, None, None] #msgRetorno [result, nome, cpf, logradouro, complemento, bairro, cidade, uf, saldo, nomeFavorecido]
                msg = decriptografar(msg) #decriptografando mensagem
                msg = pickle.loads(msg) #msg [operacao, numContaRem, numContaDest, valor, senha]
            except:
                break
            
            #LOGIN
            if (msg[0]==0):
                print('\nLogin')
                operacoes = transacoes.operacoes()
                result = operacoes.login(msg[1], msg[4])
                if(result!=-1):
                    msgRetorno[0]=0
                    msgRetorno[1]=result[0] #nome
                    msgRetorno[2]=result[1] #cpf
                    msgRetorno[9]=result[2] #saldo
                else:
                    msgRetorno[0]=1
                msgRetorno = pickle.dumps(msgRetorno) #transformando objeto em sequencia de bytes
                msgRetorno = criptografar(msgRetorno) #criptografando mensagem
                conn.send(msgRetorno) #enviando mensagem
                pass
            
            #SAQUE
            if(msg[0]==1):
                print('\nSaque')
                operacoes = transacoes.operacoes()
                result = operacoes.saque(msg[1], msg[3]) #numContaRem, valorSaque
                if(result>=0):
                    msgRetorno[0]=0 #Sque realizado
                    msgRetorno[9]=result
                elif(result==-1):
                    msgRetorno[0]=1 #Erro não foi possível sacar o valor com as notas disponíveis
                elif(result==-2):
                    msgRetorno[0]=2 #Erro não há saldo suficiente para saque
                else:
                    msgRetorno[0]=3 #Erro saque não realizado
                msgRetorno = pickle.dumps(msgRetorno) #transformando objeto em sequencia de bytes
                msgRetorno = criptografar(msgRetorno) #criptografando mensagem
                conn.send(msgRetorno) #enviando mensagem
                pass
            
            #DEPOSITO
            elif(msg[0]==2):
                print('\nDepósito')
                operacoes = transacoes.operacoes()
                result = operacoes.deposito(msg[1], msg[3]) #numContaRem, valorDeposito
                if(result>=0):
                    msgRetorno[0]=0 #Deposito realizado com sucesso
                    msgRetorno[9]=result
                else:
                    msgRetorno[0]=1 #Erro depoósito não realizado
                msgRetorno = pickle.dumps(msgRetorno)
                msgRetorno = criptografar(msgRetorno) #criptografando mensagem
                conn.send(msgRetorno)
                pass
            
            #TRANSFERENCIA ETAPA 1
            elif(msg[0]==3):
                print('\nTransferência Etapa 1')
                operacoes = transacoes.operacoes()
                result = operacoes.transferencia(msg[1], msg[2], msg[3]) #numContaRem, valorDeposito
                if(result == '-1'):
                    msgRetorno[0]=1 #Erro conta de destino inexistente
                elif(result == '-2'):
                    msgRetorno[0]=2 #Erro nao ha saldo suficiente para transferencia
                elif(result == '-3'):
                    msgRetorno[0]=3 #Erro conta de origem e destino sao as mesmas
                else:
                    msgRetorno[0]=0 #Ok
                    msgRetorno[10]=result #Retorna nome do favorecido na transferencia
                msgRetorno = pickle.dumps(msgRetorno)
                msgRetorno = criptografar(msgRetorno)
                conn.send(msgRetorno)
                pass
            
            #TRANSFERENCIA ETAPA 2
            elif(msg[0]==4):
                print('\nTransferência Etapa 2')
                operacoes = transacoes.operacoes()
                result = operacoes.transferencia2(msg[1], msg[2], msg[3]) #numContaRem, valorDeposito
                if(result == '-1'):
                    msgRetorno[0]=1 #erro transferencia nao realizada
                else:
                    msgRetorno[0]=0 #transferencia realizada com sucesso
                    msgRetorno[9]=result #saldoAtualizado
                msgRetorno = pickle.dumps(msgRetorno)
                msgRetorno = criptografar(msgRetorno)
                conn.send(msgRetorno)
                pass
            
            #INFORMACOES CADASTRAIS 
            elif(msg[0]==5):
                #print('\nInformações Cadastrais')
                operacoes = transacoes.operacoes()
                result = operacoes.infoCadastrais(msg[1]) #numContaRem, valorDeposito
                if(result!=-1):
                    msgRetorno[0]=0
                    msgRetorno[1]=result[0] #nome
                    msgRetorno[2]=result[1] #cpf
                    msgRetorno[3]=result[2] #logradouro
                    msgRetorno[4]=result[3] #complemento
                    msgRetorno[5]=result[4] #bairro
                    msgRetorno[6]=result[5] #cidade
                    msgRetorno[7]=result[6] #uf
                    msgRetorno[8]=result[7] #cep
                    msgRetorno[9]=result[8] #saldo
                else:
                    msgRetorno[0]=1 #erro nao foi possivel consultar informacaoes cadastrais
                msgRetorno = pickle.dumps(msgRetorno)
                msgRetorno = criptografar(msgRetorno)
                conn.send(msgRetorno)
                pass
            
            #PAGAMENTO
            if(msg[0]==6):
                print('\nPagamento de contas')
                operacoes = transacoes.operacoes()
                result = operacoes.pagamento(msg[1], msg[3]) #numContaRem, valorPagamento
                if(result>=0):
                    msgRetorno[0]=0 #Pagamento realizado
                    msgRetorno[9]=result
                elif(result==-1):
                    msgRetorno[0]=1 #Não há saldo suficiente para pagamento
                else:
                    msgRetorno[0]=2 #Erro Pagamento não realizado
                msgRetorno = pickle.dumps(msgRetorno) #transformando objeto em sequencia de bytes
                msgRetorno = criptografar(msgRetorno) #criptografando mensagem
                conn.send(msgRetorno) #enviando mensagem
                pass
    finally:
        print('Conexao Encerrada\n')
        conn.close()
transacoes.conectar.close()
