import os
import pandas as pd
import win32com.client as win32
from FilesHandling import *
from ProcessingOperations import *
from shutil import move



# Função para ver o conteúdo da carteira
def ver_carteira(wallet_list):
    os.system('cls')
    print('-----------------------------CARTEIRA-----------------------------')
    print("{:^20} {:^5} {:^10} {:^5} {:^10}".format("TIPO DE MOEDA","|","QUANTIDADE ADQUIRIDA","|","TOTAL"))
    print("------------------------------------------------------------------")
    total_carteira = 0
    for sublist in wallet_list:
        total=float(sublist[0])*float(sublist[1])
        total_carteira+=total
        print("{:^20} {:^5} {:^20} {:^5} {:^10}".format(str(sublist[0])+'€',"|", sublist[1],"|", str(total)+'€'))
        print("------------------------------------------------------------------")
    print('{:>20} {:^5} {:^20} {:^5} {:^10}'.format('','','TOTAL NA CARTEIRA','|',str(total_carteira)+'€'))
    print("------------------------------------------------------------------")


# Função para adicionar créditos à carteira
# list[string[]] -> void
def adicionar_creditos(wallet_list):
    moeda, quantidade = operations_add_remove_loan(wallet_list, 'adicionar')

    if moeda==None and quantidade==None:
        return

    for element in wallet_list:
        if element[0]==moeda:
            quantidade_inicial = int(element[1])

    quantidade_modificada=int(quantidade) + quantidade_inicial

    os.system('cls')
    if modificar_ficheiro(wallet_list,'wallet.csv',moeda, quantidade_modificada)==True:
        transactions(moeda,quantidade,quantidade_inicial,quantidade_modificada,'adicionar')
        print('------------------------')
        print('Adicionado', int(quantidade)*float(moeda),'€')
        print('------------------------')
    else:
        print('--------------------')
        print('Erro na transação')
        print('--------------------')


# Função para remover créditos da carteira
# list[string[]] -> void
def remover_creditos(wallet_list):
    moeda, quantidade = operations_add_remove_loan(wallet_list, 'remover')

    if moeda == None and quantidade == None:
        return

    for element in wallet_list:
        if element[0] == moeda:
            if int(element[1]) < int(quantidade):
                os.system('cls')
                print('----------------------------------------')
                print('Não possui esta quantidade de moedas')
                print('----------------------------------------')
                return
            else:
                quantidade_inicial = int(element[1])

    quantidade_final = quantidade_inicial - int(quantidade)

    os.system('cls')
    
    if modificar_ficheiro(wallet_list,'wallet.csv',moeda,quantidade_final)==True:
        transactions(moeda,quantidade,quantidade_inicial,quantidade_final,'removido')
        print('-------------------')
        print('Removido', int(quantidade)*float(moeda),'€')
        print('-------------------')
    else:
        print('-------------------')
        print('Erro na transação')
        print('-------------------')


# Função que permite ao utilizador emprestar créditos
# list[string[]] -> void
def emprestimo(wallet_list):
    moeda, quantidade = operations_add_remove_loan(wallet_list, 'emprestar')

    if moeda==None and quantidade==None:
        return

    for element in wallet_list:
        if element[0] == moeda:
            if int(element[1]) < int(quantidade):
                os.system('cls')
                print('----------------------------------------')
                print('Não possui esta quantidade de moedas')
                print('----------------------------------------')
                return
            else:
                quantidade_inicial = int(element[1])

    quantidade_final = quantidade_inicial - int(quantidade)

    print('')
    pessoa_emprestimo = input('Insira a pessoa a quem se destina o empréstimo:\n')
    pessoa_emprestimo = pessoa_emprestimo[0].upper() + pessoa_emprestimo[1:]

    if '.' in moeda:
        valor = float(moeda) * int(quantidade)
    else:
        valor = int(moeda) * int(quantidade)

    codigo_emprestimo = codigo()
    
    append_new_line('emprestimos.csv',datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ',' + moeda + ',' + quantidade + ',' + str(valor) + ',' + pessoa_emprestimo + ',' + 'Por Resolver' + ',' + codigo_emprestimo)
    
    os.system('cls')
    
    if modificar_ficheiro(wallet_list,'wallet.csv',moeda,quantidade_final)==True:
        transactions(moeda,quantidade,quantidade_inicial,quantidade_final,'removido(emprestimo)')
        print('-----------------------------------')
        print('Emprestado', valor,'€ a',pessoa_emprestimo)
        print('')
        print('Código do Empréstimo:',codigo_emprestimo)
        print('-----------------------------------')
    else:
        print('-------------------')
        print('Erro na transação')
        print('--------------------')


# Função para resolver empréstimos
# list[string[]], list[string[]] -> void
def resolver_emprestimo(lista_emprestimos,wallet_list):
    if lista_emprestimos==[]:
        print('---------------------------')
        print('Não tem empréstimos')
        print('---------------------------')
        return
    
    flag = False
    for emprestimo in lista_emprestimos:
        if emprestimo[5] == 'Por Resolver':
            flag = True
            break

    if flag == False:
        print('-----------------------------------------')
        print('Não tem nenhum empréstimo por resolver')
        print('-----------------------------------------')
        return
    
    print('----------------------------------------------------------------------------------------EMPRESTAR CRÉDITOS----------------------------------------------------------------------------------------')
    print('')
    print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^16} {:^5} {:>15} {:>12} {:>15}'.format('DATA DO EMPRÉSTIMO','|','MOEDA','|','QUANTIDADE','|','VALOR EMPRESTADO','|','PESSOA','|','CÓDIGO','|','SITUAÇÃO'))
    print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for emprestimo in lista_emprestimos:
        print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^16} {:^5} {:>17} {:>10} {:>17}'.format(emprestimo[0],'|',emprestimo[1],'|',emprestimo[2],'|',emprestimo[3],'|',emprestimo[4],'|',emprestimo[6],'|',emprestimo[5]))
        print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('')
    print('USE B PARA VOLTAR ATRÁS')
    print('')
    codigo_utilizador = input('Insira o código do empréstimo a ser resolvido:\n')
    if codigo_utilizador=='B':
        os.system('cls')
        return

    for element in lista_emprestimos:
        if codigo_utilizador == element[6]:
            print('')
            print('---------------------------------------------------')
            print('Empréstimo:')
            print('Data: ',element[0])
            print('Moeda: ',element[1]+'€')
            print('Quantidade: ',element[2])
            print('Valor do Empréstimo: ',element[3]+'€')
            print('Pessoa: ',element[4])
            print('Código: ',element[6])
            print('---------------------------------------------------')

            for row in wallet_list:
                if row[0]==element[1]:
                    quantidade_inicial=row[1]

            if '.' in element[1]:
                element[1] = float(element[1])
            else:
                element[1] = int(element[1])

            confirm=input('Deseja resolver este empréstimo?(Y/n)\n')
            if confirm=='Y':
                if modificar_ficheiro_emprestimos(carregar_ficheiro('emprestimos.csv'),'emprestimos.csv',str(element[1]),element[2], element[4],element[0],element[6]):
                    print(str(int(element[2])+int(quantidade_inicial)))
                    modificar_ficheiro(wallet_list,'wallet.csv',str(element[1]),str(int(element[2])+int(quantidade_inicial)))
                    append_new_line('transactions.csv',datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ',' + str(element[1])+ ',' + str(int(element[2])) +',' + str(int(quantidade_inicial)) + ',' + str(int(element[2])+int(quantidade_inicial)) + ',' + str(element[1]*int(element[2])) + ',' + 'adicionado(emprestimo pago)' + ',' + ver_saldo(carregar_ficheiro('wallet.csv')))
                    os.system('cls')
                    print('-------------------------')
                    print('Empréstimo Resolvido')
                    print('-------------------------')
                    return
            else:
                os.system('cls')
                print('-----------------------------')
                print('Empréstimo Não Resolvido')
                print('-----------------------------')
                return
    os.system('cls')
    print('---------------------')
    print('Código inválido')
    print('---------------------')


# Função para ver empréstimos
def ver_emprestimos(lista_emprestimos):
    os.system('cls')
    if lista_emprestimos==[]:
        print('------------------------------')
        print('Lista de empréstimos vazia')
        print('------------------------------')
        return
    print('----------------------------------------------------------------------------------------EMPRÉSTIMOS-----------------------------------------------------------------------------------')
    print('')
    print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^16} {:^5} {:>15} {:>12} {:>15}'.format('DATA DO EMPRÉSTIMO','|','MOEDA','|','QUANTIDADE','|','VALOR EMPRESTADO','|','PESSOA','|','CÓDIGO','|','SITUAÇÃO'))
    print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for element in lista_emprestimos:
        if element != []:
            print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^16} {:^5} {:>17} {:>10} {:>17}'.format(element[0],'|',element[1],'|',element[2],'|',element[3],'|',element[4],'|',element[6],'|',element[5]))
            print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')


# Função para ver extrato
def ver_extrato(lista_extrato):
    dic_extrato={"DATA DA TRANSAÇÃO":[],"MOEDA":[],"QUANTIDADE TRANSFERIDA":[],"QUANTIDADE INICIAL":[],"QUANTIDADE FINAL":[],"TOTAL DA OPERAÇÃO":[],"SALDO":[]}
    if lista_extrato==[]:
        os.system('cls')
        print('---------------------')
        print('Extrato Vazio')
        print('---------------------')
        return
    for element in lista_extrato:
        if 'removido' in element[6]:
            element[5]='-'+element[5]
    os.system('cls')
    print('--------------------------------------------------------------------------------EXTRATO------------------------------------------------------------------------------------------------------')
    print('')
    print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^12} {:^10} {:^12} {:<5} {:^13} {:>5}'.format('DATA DA TRANSAÇÃO','|','MOEDA','|','QUANTIDADE TRANSFERIDA','|','QUANTIDADE INICIAL','|','QUANTIDADE FINAL','|','TOTAL DA OPERAÇÃO','|','SALDO'))
    print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for element in lista_extrato:
        dic_extrato["DATA DA TRANSAÇÃO"].append(element[0])
        dic_extrato["MOEDA"].append(element[1])
        dic_extrato["QUANTIDADE TRANSFERIDA"].append(element[2])
        dic_extrato["QUANTIDADE INICIAL"].append(element[3])
        dic_extrato["QUANTIDADE FINAL"].append(element[4])
        dic_extrato["TOTAL DA OPERAÇÃO"].append(element[5]+'€')
        dic_extrato["SALDO"].append(element[7])
        print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^10} {:^20} {:^5} {:^20} {:^12} {:>10} {:>14} {:>15}'.format(element[0],'|',element[1],'|',element[2],'|',element[3],'|',element[4],'|',element[5]+'€','|',element[7]))
        print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for element in lista_extrato:
        if '9999999999999999' in element:
            decisao=1
        else:
            decisao=0
    if decisao==1:
        print('______________________________________________________________')
        print('O código 9999999999999999 representa um RESET da carteira')
        print('______________________________________________________________')
    dados = pd.DataFrame(data=dic_extrato)
    data = str(datetime.today().strftime('%d-%m-%Y'))
    dados.to_excel(data+"_extrato.xlsx", index=False)

    directory = os.getcwd()
    if ("Detalhes" not in os.listdir(directory)):
        os.mkdir("Detalhes")
        move(data+"_extrato.xlsx", "Detalhes")
    else:
        if (data+"_extrato.xlsx" not in os.listdir(directory+"/Detalhes")):
            move(data+"_extrato.xlsx", "Detalhes")
        else:
            os.remove(directory+"/Detalhes/"+data+"_extrato.xlsx")
            move(data+"_extrato.xlsx", "Detalhes")


# Função para fazer o reset da carteira
def reset_carteira(wallet_list):
    os.system('cls')
    print('---------------------RESET DA CARTEIRA---------------------')
    print('')
    confirm=input('Tem a certeza que deseja resetar a sua carteira?(Y/n):\n')
    if confirm=='Y':
        file='wallet.csv'
        for element in wallet_list:
            element[1]=0
        modificar_ficheiro(wallet_list, file, 0, 0)
        append_new_line('transactions.csv',datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ',' + '9999999999999999'+ ',' + '9999999999999999'+',' + '9999999999999999' + ',' + '9999999999999999' + ',' + '' + ',' + '9999999999999999' + ',' + '')
        os.system('cls')
        print('---------------------')
        print('CARTEIRA RESETADA')
        print('---------------------')
    else:
        os.system('cls')
        print('--------------------------')
        print('CARTEIRA NÃO RESETADA')
        print('--------------------------')


# Função para enviar os detalhes da conta por email
def enviar_email(lst_emprestimos, lst_carteira, lst):
    dic_emprestimos = {"DATA DO EMPRÉSTIMO" : [],"MOEDA":[],"QUANTIDADE":[],"VALOR EMPRESTADO":[],"PESSOA":[], "CÓDIGO" : [], "SITUAÇÃO" : []}
    dic_carteira = {"MOEDA" : [],"QUANTIDADE": [],"QUANTIA" : [], "Saldo" : ["","","","","","","","","","","","",""]}
    dic_extrato={"DATA DA TRANSAÇÃO":[],"MOEDA":[],"QUANTIDADE TRANSFERIDA":[],"QUANTIDADE INICIAL":[],"QUANTIDADE FINAL":[],"TOTAL DA OPERAÇÃO":[], "SALDO" : []}
    dic_meses={"01":"Janeiro", "02":"Fevereiro", "03":"Março", "04":"Abril", "05":"Maio", "06":"Junho", "07":"Julho", "08":"Agosto", "09":"Setembro", "10":"Outubro", "11":"Novembro", "12":"Dezembro"}
    total = 0
    for element in lst_carteira:
        dic_carteira["MOEDA"].append(element[0])
        dic_carteira["QUANTIDADE"].append(element[1])
        dinheiro_moeda = float(element[1]) * float(element[0])
        total+=dinheiro_moeda
        dic_carteira["QUANTIA"].append(dinheiro_moeda)
    dic_carteira["Saldo"].append(str(total)+"€")

    for element in lst_emprestimos:
        dic_emprestimos["DATA DO EMPRÉSTIMO"].append(element[0])
        dic_emprestimos["MOEDA"].append(element[1])
        dic_emprestimos["QUANTIDADE"].append(element[2])
        dic_emprestimos["VALOR EMPRESTADO"].append(element[3])
        dic_emprestimos["PESSOA"].append(element[4])
        dic_emprestimos["CÓDIGO"].append(element[6])
        dic_emprestimos["SITUAÇÃO"].append(element[5])
    
    for element in lst:
        if 'removido' in element:
            element[5]='-'+element[5]
        dic_extrato["DATA DA TRANSAÇÃO"].append(element[0])
        dic_extrato["MOEDA"].append(element[1])
        dic_extrato["QUANTIDADE TRANSFERIDA"].append(element[2])
        dic_extrato["QUANTIDADE INICIAL"].append(element[3])
        dic_extrato["QUANTIDADE FINAL"].append(element[4])
        dic_extrato["TOTAL DA OPERAÇÃO"].append(element[5]+'€')
        dic_extrato["SALDO"].append(element[7])
            
    os.system('cls')
    print("-------------------------------ENVIAR EXTRATO POR EMAIL-----------------------------------")
    print('')
    print('USE 999 PARA VOLTAR ATRÁS')
    print('')
    destino = input('Introduza o email do destinatário:\n')
    if destino=='999':
        os.system('cls')
        return
    os.system('cls')

    data = str(datetime.today().strftime('%d-%m-%Y'))
    dia = str(datetime.today().strftime('%d'))
    extrato = pd.DataFrame(data=dic_extrato)
    carteira = pd.DataFrame(data=dic_carteira)
    emprestimos = pd.DataFrame(data=dic_emprestimos)

    extrato.to_excel(data+"_extrato.xlsx", index=False)
    emprestimos.to_excel(data+"_emprestimos.xlsx", index=False)
    carteira.to_excel(data+"_carteira.xlsx", index=False)

    outlook = win32.Dispatch("outlook.application")
    email = outlook.CreateItem(0)
    email.To = destino
    email.Subject = "Detalhes da sua conta a "+dia + " de "+dic_meses[str(datetime.today().strftime('%m'))]+" de "+datetime.today().strftime('%Y')
    email.HTMLBody = "Aqui estão os detalhes da sua conta.<br> Data: "+data
    directory = os.getcwd()

    email.attachments.Add(directory+"\\"+data+"_extrato.xlsx")
    email.attachments.Add(directory+"\\"+data+"_emprestimos.xlsx")
    email.attachments.Add(directory+"\\"+data+"_carteira.xlsx")

    lst_ficheiros = [data+"_extrato.xlsx", data+"_emprestimos.xlsx", data+"_carteira.xlsx"]
    if ("Anexos Email" not in os.listdir(directory)):
        os.mkdir("Anexos Email")
        os.mkdir("Anexos Email\\"+data)
        move(data+"_extrato.xlsx", "Anexos Email/"+data)
        move(data+"_emprestimos.xlsx", "Anexos Email/"+data)
        move(data+"_carteira.xlsx", "Anexos Email/"+data)
    else:
        if (data not in os.listdir("Anexos Email")):
            os.mkdir("Anexos Email/"+data)
            move(data+"_extrato.xlsx", "Anexos Email/"+data)
            move(data+"_emprestimos.xlsx", "Anexos Email/"+data)
            move(data+"_carteira.xlsx", "Anexos Email/"+data)
        else:
            for element in lst_ficheiros:
                os.remove(directory+"/Anexos Email/"+data+"/"+element)
                move(element, "Anexos Email/"+data)

    print('Email Destinatário: '+destino)
    confirmacao = input("Confirma o email?(Y/n):\n")
    if confirmacao=='Y':
        os.system('cls')
        email.Send()
        print('----------------------------------------')
        print('Email enviado com sucesso')
        print('----------------------------------------')
    else:
        os.system('cls')
        print('----------------------------------------')
        print('Email não enviado')
        print('----------------------------------------')