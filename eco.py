import os
import sys
from MenuOperations import *
from FilesHandling import *
from ProcessingOperations import *
import win32gui, win32con



# Função para processar as operações
def operations(escolha):
    if escolha=='1':
        ver_carteira(carregar_ficheiro())
    elif escolha=='2':
        adicionar_creditos(carregar_ficheiro())
    elif escolha=='3':
        remover_creditos(carregar_ficheiro())
    elif escolha=='4':
        os.system('cls')
        emprestimo(carregar_ficheiro())
    elif escolha=='5':
        os.system('cls')
        resolver_emprestimo(carregar_ficheiro_emprestimos(),carregar_ficheiro())
    elif escolha=='6':
        ver_emprestimos(carregar_ficheiro_emprestimos())
    elif escolha=='7':
        ver_extrato(carregar_ficheiro_extrato())
    elif escolha=='8':
        reset_carteira(carregar_ficheiro())
    elif escolha=='9':
        enviar_email(carregar_ficheiro_emprestimos(), carregar_ficheiro(), carregar_ficheiro_extrato())
    elif escolha=='0':
        os.system('cls')
        sys.exit(1)
    else:
        os.system('cls')
        return


# Menu
def main():

    os.system('cls')
    while True:
        print('__________________________________________________')
        print('MENU')
        print('__________________________________________________')
        print('1.Ver Carteira')
        print('')
        print('2.Adicionar crédito á Carteira')
        print('')
        print('3.Remover crédito á Carteira')
        print('')
        print('4.Empréstimo de Crédito')
        print('')
        print('5.Resolver Empréstimo')
        print('')
        print('6.Consultar Empréstimos')
        print('')
        print('7.Consultar Extrato')
        print('')
        print('8.Reset à Carteira')
        print('')
        print('9.Enviar Detalhes da Conta por Email')
        print('')
        print('0.Sair')
        print('__________________________________________________')
        escolha = input()
        operations(escolha)


# Iniciar o programa com a janela maximizada
hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


# Iniciar o programa
if __name__ == '__main__':
    main()