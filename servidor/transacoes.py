import sqlite3
import bcrypt

conectar = sqlite3.connect('bancoBitUFPEL.db')
c = conectar.cursor()

class operacoes(object):
    def login(self, numConta, senha):
        try:
            c.execute('Select senha from Cliente where numConta = ?', (numConta,))
            dados = c.fetchone()
            hash_senha = dados[0]
            if bcrypt.checkpw(senha, hash_senha):
                print('Usuário logado')
                for row in c.execute('Select nome, cpf, saldo from Cliente where numConta = ?', (numConta,)):
                    return row
            else:
                raise
        except:
            print('Login ou senha incorretos')
            return -1
        
    def saque(self, numConta, valor):
        try:         
            c.execute('Select saldo from Cliente where numConta = ?', (numConta,))
            saldoConta = c.fetchone()
            saldoConta = saldoConta[0]
            
            if saldoConta >= valor:
                temp = valor % 5
                if temp == 0:
                    saldoConta = saldoConta - valor
                    c.execute('Update Cliente set saldo = ? Where numConta = ?', (saldoConta, numConta,))
                    conectar.commit()
                    print('Saque realizado com sucesso')
                    return saldoConta
                else:
                    print('Não é possível sacar este valor com as notas disponíveis')
                    return -1
                    raise
            else:
                print('Não há saldo suficiente para saque')
                return -2
                raise
        except:
            print('Saque não realizado')
            return -3

    def deposito(self, numConta, valor):
        try:
            c.execute('Select saldo from Cliente where numConta = ?', (numConta,))
            saldoConta = c.fetchone()
            saldoConta = saldoConta[0]
            saldoConta = saldoConta + valor
            c.execute('Update Cliente set saldo = ? Where numConta = ?', (saldoConta, numConta,))
            conectar.commit()
            print('Deposito realizado com sucesso')
            return saldoConta
        except:
            print('Depósito não realizado')
            return -1
        
    def transferencia(self, numContaRem, numContaDest, valor):
        try:
            if(numContaRem != numContaDest):
                c.execute('Select saldo from Cliente where numConta = ?', (numContaRem,))
                saldoRemetente = c.fetchone()
                saldoRemetente = saldoRemetente[0]
        
                if(saldoRemetente >= valor):
                    c.execute('Select nome from Cliente where numConta = ?', (numContaDest,))
                    nomeDest = c.fetchone()
                    nomeDest = nomeDest[0]
                    print('Nome conta destino enviado com sucesso')
                    return nomeDest
                else:
                    print('Erro: Não há saldo suficiente para transferência')
                    return '-2'
                    raise
            else:
                print('Erro: Conta de origem e destino é mesma');
                return '-3'
                raise
        except:
            print('Transferência não realizada')
            return '-1'

    def transferencia2(self, numContaRem, numContaDest, valor):
        try:
            c.execute('Select saldo from Cliente where numConta = ?', (numContaRem,))
            saldoRemetente = c.fetchone()
            saldoRemetente = saldoRemetente[0]
            c.execute('Select saldo from Cliente where numConta = ?', (numContaDest,))
            saldoDestino = c.fetchone()
            saldoDestino = saldoDestino[0]

            saldoDestino = saldoDestino + valor
            saldoRemetente = saldoRemetente - valor
            c.execute('Update Cliente set saldo = ? Where numConta = ?', (saldoRemetente, numContaRem))
            c.execute('Update Cliente set saldo = ? Where numConta = ?', (saldoDestino, numContaDest))
            conectar.commit()
            print('Transferência realizada com sucesso')
            return saldoRemetente
        except:
            print('Transferência não realizada')
            return -1

    def infoCadastrais(self, numConta):
        try:
            for row in c.execute('Select nome, cpf, logradouro, complemento, bairro, cidade, uf, cep, saldo from Cliente where numConta = ?', (numConta,)):
                return row
        except:
            print('Erro ao buscar os dados cadastrais')
            return -1

    def pagamento(self, numConta, valor):
        try:         
            c.execute('Select saldo from Cliente where numConta = ?', (numConta,))
            saldoConta = c.fetchone()
            saldoConta = saldoConta[0]
            
            if saldoConta >= valor:
                saldoConta = saldoConta - valor
                c.execute('Update Cliente set saldo = ? Where numConta = ?', (saldoConta, numConta,))
                conectar.commit()
                print('Pagamento realizado com sucesso')
                return saldoConta
            else:
                print('Não há saldo suficiente para pagamento')
                return -1
                raise
        except:
            print('Pagamento não realizado')
            return -2
