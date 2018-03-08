import clientes

def menuPrincipal():
    while True:
        print('\n')
        titulo = 'Banco bitUfpel'
        print("=" * len(titulo), titulo, "=" * len(titulo), sep="\n")
        print("[1] - Criar Banco de Dados (caso não exista)\n[2] - Cadastrar Nova Conta\n[3] - Logar\n[4] - Sair")
        op = input("Opção: ")
        if op.isdigit():
            if int(op) == 4:
                break
            elif int(op) == 1:
                criarBD()
                continue
            elif int(op) == 2:
                novaConta()
                continue
            elif int(op) == 3:
                consultarSenha()
                continue
            '''
            elif int(op) == 3:
                transacao()
                continue
            '''
        print('Opção inválida\n')

def criarBD():
    clientes.criar_db()

def novaConta():
    print('\n')
    titulo = 'Cadastrar nova conta'
    print("=" * len(titulo), titulo, "=" * len(titulo), sep="\n")
    clientes.menuCadastro()
    print('')

def consultarSenha():
    print('\n')
    titulo = 'Consultar senha'
    print("=" * len(titulo), titulo, "=" * len(titulo), sep="\n")
    op = input("numConta: ")
    senha = str.encode(input("senha: "))
    clientes.usuario_autenticado(op, senha)
    print('')
    
menuPrincipal()
