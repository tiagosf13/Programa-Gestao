from FilesHandling import *
import MenuOperations
from datetime import datetime
from random import randrange



# Função para registar as transações no ficheiro transactions.csv
# string, string, int, int, string -> void
def transactions(moeda,quantidade,quantidade_inicial,quantidade_modificada,tipo_operacao):
    filetransedit=open('transactions.csv', 'a+')
    if '.' in moeda:
        total = float(moeda) * float(quantidade)
    else:
        total = int(moeda) * int(quantidade)
    
    append_new_line('transactions.csv',datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ',' + moeda+ ',' + quantidade +',' + str(quantidade_inicial) + ',' + str(quantidade_modificada) + ',' + str(total) + ',' + tipo_operacao + ',' + ver_saldo(carregar_ficheiro('wallet.csv')))
    filetransedit.close()


# Função para ver o saldo total da carteira
# list[string[]] -> string
def ver_saldo(wallet_list):
    total_carteira=0

    for sublist in wallet_list:
        total_carteira += float(sublist[0])*float(sublist[1])

    return str(total_carteira)+'€'


# Função para gerar um código aleatório de 10 dígitos para o empréstimo
# void -> string
def codigo():
    codigo_emprestimo=str(randrange(1000000000,9999999999))
    if carregar_ficheiro('emprestimos.csv')==[]:
        return codigo_emprestimo
    else:
        for element in carregar_ficheiro('emprestimos.csv'):
            if element[6]==codigo_emprestimo:
                return codigo()
            else:
                return codigo_emprestimo


# list[string[]], string -> string, string
def operations_add_remove_loan(wallet_list, operation):
    dic_operations = {'adicionar': 'adicionada', 'remover': 'removida', 'emprestar': 'emprestada'}
    lst_numerario=[]
    quantidade = 'B'
    while quantidade == 'B' or quantidade.isdigit()==False:
        os.system('cls')
        MenuOperations.ver_carteira(wallet_list)
        print('USE B PARA VOLTAR ATRÁS')
        print('')
        moeda=input('Que tipo de moeda deseja '+operation+'?\n')
        if moeda=='B':
            os.system('cls')
            return None, None
        [lst_numerario.append(element[0]) for element in wallet_list]
        if moeda in lst_numerario:
            print(2*'\n')
            quantidade=input('Quantidade da moeda a ser '+dic_operations[operation]+'(se introduziu a moeda errada insira B):\n')
    return moeda, quantidade
