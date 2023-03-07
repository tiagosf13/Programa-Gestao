from FilesHandling import *
import MenuOperations
from datetime import datetime
from random import randrange



# Função para registar as transações no ficheiro transactions.csv
def transferencias(moeda,quantidade,quantidade_inicial,quantidade_modificada,total,tipo_operacao):
    filetransedit=open('transactions.csv', 'a+')
    append_new_line('transactions.csv',datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ',' + str(moeda)+ ',' + str(quantidade) +',' + str(quantidade_inicial) + ',' + str(quantidade_modificada) + ',' + str(total) + ',' + tipo_operacao + ',' + ver_saldo(carregar_ficheiro()))
    filetransedit.close()


# Função para ver o saldo total da carteira
def ver_saldo(wallet_list):
    total_carteira=0
    for sublist in wallet_list:
        moeda=sublist[0]
        quantidade=sublist[1]
        total=float(moeda)*float(quantidade)
        total_carteira+=total
    saldo=str(total_carteira)+'€'
    return saldo


# Função para gerar um código aleatório de 10 dígitos para o empréstimo
def codigo():
    codigo_emprestimo=str(randrange(1000000000,9999999999))
    if carregar_ficheiro_emprestimos()==[]:
        return codigo_emprestimo
    else:
        for element in carregar_ficheiro_emprestimos():
            if element[6]==codigo_emprestimo:
                return codigo()
            else:
                return codigo_emprestimo

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
        for element in wallet_list:
            lst_numerario.append(element[0])
        if moeda in lst_numerario:
            print('')
            print('')
            quantidade=input('Quantidade da moeda a ser '+dic_operations[operation]+'(se introduziu a moeda errada insira B):\n')
    return moeda, quantidade
