import os
import sys
from shutil import move
from tracemalloc import stop
from unicodedata import name
from numpy import source
import pandas as pd
import win32com.client as win32
import win32gui, win32con
from datetime import datetime
from random import randrange

###########################################################
#       FUNÇÃO PARA GERAR UM CÓDIGO DE EMPRÉSTIMO         #
###########################################################

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

#----------------------------------------------------------

#################################################################################################################################################################################################################################################################################
#                                                                                                                     FUNÇÃO PARA RESOLVER UM EMPRÉSTIMO                                                                                                                        #
#################################################################################################################################################################################################################################################################################

def resolver_emprestimo(lista_emprestimos,wallet_list):
    if lista_emprestimos==[]:
        print('---------------------------')
        print('Não tem empréstimos')
        print('---------------------------')
        main()
    kill=0
    for element in lista_emprestimos:
        if element[5]=='Resolvido':
            kill=1
        else:
            kill=0
            break
    if kill==1:
        print('-----------------------------------------')
        print('Não tem nenhum empréstimo por resolver')
        print('-----------------------------------------')
        main()
    print('----------------------------------------------------------------------------------------EMPRESTAR CRÉDITOS----------------------------------------------------------------------------------------')
    print('')
    print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^16} {:^5} {:>15} {:>12} {:>15}'.format('DATA DO EMPRÉSTIMO','|','MOEDA','|','QUANTIDADE','|','VALOR EMPRESTADO','|','PESSOA','|','CÓDIGO','|','SITUAÇÃO'))
    print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for element in lista_emprestimos:
        print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^16} {:^5} {:>17} {:>10} {:>17}'.format(element[0],'|',element[1],'|',element[2],'|',element[3],'|',element[4],'|',element[6],'|',element[5]))
        print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('')
    print('USE 999 PARA VOLTAR ATRÁS')
    print('')
    codigo_utilizador=str(input('Insira o código do empréstimo a ser resolvido:\n'))
    if codigo_utilizador=='999':
        os.system('cls')
        main()
    for element in lista_emprestimos:
        data=element[0]
        moeda=element[1]
        quantidade=element[2]
        valor=element[3]
        pessoa=element[4]
        codigo=element[6]
        if codigo_utilizador == codigo:
            print('---------------------------------------------------')
            print('Empréstimo:')
            print('Data: ',data)
            print('Moeda: ',moeda)
            print('Quantidade: ',quantidade)
            print('Valor do Empréstimo: ',valor)
            print('Pessoa: ',pessoa)
            print('Código: ',codigo)
            print('---------------------------------------------------')
            file='wallet.txt'
            for element in wallet_list:
                if element[0]==str(moeda):
                    quantidade_inicial=element[1]
            quantidade_emprestimo_int=int(moeda)*int(quantidade)
            quantidade_modificada=quantidade_emprestimo_int+quantidade_inicial
            confirm=input('Deseja resolver este empréstimo?(Y/n)\n')
            if confirm=='Y':
                modificar_ficheiro(wallet_list,file,moeda,quantidade_modificada)
                int_moeda_emprestimo=int(moeda)
                int_quantidade_emprestimo=int(quantidade)
                total=int_moeda_emprestimo*int_quantidade_emprestimo
                total=str(total)
                tipo_operacao='adicionado(emprestimo pago)'
                quantidade_inicial_str=str(quantidade_inicial)
                quantidade_modificada_str=str(quantidade_modificada)
                append_new_line('transactions.txt',datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ',' + str(moeda)+ ',' + quantidade+',' + quantidade_inicial_str + ',' + quantidade_modificada_str + ',' + total + ',' + tipo_operacao + ',' + ver_saldo(carregar_ficheiro()))
                file_emprestimos='emprestimos.txt'
                if modificar_ficheiro_emprestimos(carregar_ficheiro_emprestimos(),file_emprestimos,moeda,quantidade, pessoa,data,codigo):
                    os.system('cls')
                    print('-------------------------')
                    print('Empréstimo Resolvido')
                    print('-------------------------')
                    main()
            else:
                os.system('cls')
                print('-----------------------------')
                print('Empréstimo Não Resolvido')
                print('-----------------------------')
                main()
    os.system('cls')
    print('---------------------')
    print('Código inválido')
    print('---------------------')
    main()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

###################################################################################################################################################################################
#                                                               FUNÇÃO PARA MODIFICAR O FICHEIRO EMPRESTIMOS                                                                      #
###################################################################################################################################################################################

def modificar_ficheiro_emprestimos(lista_emprestimos,ficheiro,moeda_emprestimo,quantidade_emprestimo, pessoa,data_emprestimo,codigo_emprestimo):
    moeda_emprestimo_int=int(moeda_emprestimo)
    for element in lista_emprestimos:
        if (element[1]==moeda_emprestimo_int) and (element[2]==quantidade_emprestimo) and(element[4]==pessoa) and (element[0]==data_emprestimo) and(element[6]==codigo_emprestimo):
            element[5]='Resolvido'
    fileop=open(ficheiro,'w')
    for element in lista_emprestimos:
        fileop.write(str(element[0])+','+str(element[1])+','+str(element[2]+','+str(element[3])+','+str(element[4])+','+str(element[5])+','+str(element[6])+'\n'))
    for element in lista_emprestimos:
        if element[4]==pessoa:
            if element[1]==moeda_emprestimo_int:
                if element[2]==quantidade_emprestimo:
                    print(element[0])
                    print(data_emprestimo)
                    if element[0]==data_emprestimo:
                        return True

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

############################################################################################################################################################################################################################
#                                                                               FUNÇÃO PARA VISUALIZAR OS EMPRÉSTIMOS                                                                                                      #
############################################################################################################################################################################################################################

def ver_emprestimos(lista_emprestimos):
    os.system('cls')
    if lista_emprestimos==[]:
        print('------------------------------')
        print('Lista de empréstimos vazia')
        print('------------------------------')
        main()
    print('----------------------------------------------------------------------------------------EMPRÉSTIMOS-----------------------------------------------------------------------------------')
    print('')
    print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^16} {:^5} {:>15} {:>12} {:>15}'.format('DATA DO EMPRÉSTIMO','|','MOEDA','|','QUANTIDADE','|','VALOR EMPRESTADO','|','PESSOA','|','CÓDIGO','|','SITUAÇÃO'))
    print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for element in lista_emprestimos:
        print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^16} {:^5} {:>17} {:>10} {:>17}'.format(element[0],'|',element[1],'|',element[2],'|',element[3],'|',element[4],'|',element[6],'|',element[5]))
        print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    main()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

##################################################################################################################################
#                                               FUNÇÃO PARA CARREGAR O FICHEIRO EMPRÉSTIMOS                                      #
##################################################################################################################################

def carregar_ficheiro_emprestimos():
    lst=[]
    with open("emprestimos.txt") as file:
        for line in file:
            lst.append(line.strip().split(","))
    newlst=[]
    for element in lst:
        if element[0]!='':
            newlst.append(element)
    file_open=open('emprestimos.txt', 'w')
    for element in newlst:
        file_open.write(element[0]+','+element[1]+','+element[2]+','+element[3]+','+element[4]+','+element[5]+','+element[6]+'\n')
        element[1]=int(element[1])
    return newlst

#---------------------------------------------------------------------------------------------------------------------------------

#############################################################################################################################################################################################################################
#                                                                                           FUNÇÃO PARA REALIZAR UM EMPRESTIMO                                                                                              #
#############################################################################################################################################################################################################################

def emprestimo(wallet_list):
    os.system('cls')
    print('------------------------EMPRESTAR CRÉDITOS------------------------')
    print('')
    print("{:^20} {:^5} {:^10} {:^5} {:^10}".format("TIPO DE MOEDA","|","QUANTIDADE ADQUIRIDA","|","TOTAL"))
    print("------------------------------------------------------------------")
    total_carteira=0
    for sublist in wallet_list:
        moeda=sublist[0]
        tipo_moeda=str(moeda)+'€'
        quantidade=sublist[1]
        total=float(moeda)*float(quantidade)
        total_carteira+=total
        y=str(total)+'€'
        print("{:^20} {:^5} {:^20} {:^5} {:^10}".format(tipo_moeda,"|", quantidade,"|", y))
        print("------------------------------------------------------------------")
    x=str(total_carteira)+'€'
    print('{:>20} {:^5} {:^20} {:^5} {:^10}'.format('','','TOTAL NA CARTEIRA','|',x))
    print("------------------------------------------------------------------")
    print('')
    print('USE 999 PARA VOLTAR ATRÁS')
    print('')
    moeda_emprestimo=input('Insira a moeda a ser sujeito a empréstimo:\n')
    if moeda_emprestimo=='999':
        os.system('cls')
        main()
    valores=[]
    for element in wallet_list:
        valores.append(element[0])
    moeda_emprestimo_int=int(moeda_emprestimo)
    if moeda_emprestimo not in valores:
        emprestimo(carregar_ficheiro())
    print('')
    quantidade_emprestimo=input('Insira a quantidade a ser sujeito a empréstmo (se introduziu a moeda errada insira 555):\n')
    if quantidade_emprestimo=='555':
        os.system('cls')
        emprestimo(carregar_ficheiro())
    quantidade_emprestimo_int=int(quantidade_emprestimo)
    for element in wallet_list:
        if element[0]==moeda_emprestimo:
            if element[1]<quantidade_emprestimo_int:
                os.system('cls')
                print('-----------------------------------------------------')
                print('Não possui o crédito necessário para o empréstimo')
                print('-----------------------------------------------------')
                main()
    print('')
    pessoa_emprestimo=input('Insira a pessoa a quem se destina o empréstimo:\n')
    pessoa_emprestimo=pessoa_emprestimo[0].upper()+pessoa_emprestimo[1:]
    file='wallet.txt'

    for element in wallet_list:
        if element[0]==moeda_emprestimo:
            quantidade_inicial=int(element[1])
            if quantidade_emprestimo_int<=quantidade_inicial:
                quantidade_final=quantidade_inicial-quantidade_emprestimo_int
    moeda_int=int(moeda_emprestimo)
    quantidade_final_int=int(quantidade_final)
    valor=moeda_int*quantidade_emprestimo_int
    valor=str(valor)
    codigo_ficheiro_emprestimo=str(codigo())
    situacao_emprestimo='Por Resolver'
    append_new_line('emprestimos.txt',datetime.today().strftime('%Y-%m-%d %H:%M:%S')+','+ moeda_emprestimo +','+quantidade_emprestimo+','+valor+','+pessoa_emprestimo+','+situacao_emprestimo+','+codigo_ficheiro_emprestimo)
    os.system('cls')
    if modificar_ficheiro(wallet_list,file,moeda_emprestimo,quantidade_final)==True:
        valor='-'+valor
        transferencias(moeda_emprestimo,quantidade_emprestimo,quantidade_inicial,quantidade_final,valor,'removido(emprestimo)')
        print('-----------------------------------')
        print('Emprestado', valor,'€ a',pessoa_emprestimo)
        print('')
        print('Código do Empréstimo:',codigo_ficheiro_emprestimo)
        print('-----------------------------------')
    else:
        print('-------------------')
        print('Erro na transação')
        print('--------------------')
    main()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

###########################################################################################################################################################################################################################################################
#                                                                                                FUNÇÃO PARA VISUALIZAR O EXTRATO                                                                                                                         #
###########################################################################################################################################################################################################################################################

def ver_extrato(lista_extrato):
    dic_extrato={"DATA DA TRANSAÇÃO":[],"MOEDA":[],"QUANTIDADE TRANSFERIDA":[],"QUANTIDADE INICIAL":[],"QUANTIDADE FINAL":[],"TOTAL DA OPERAÇÃO":[],"SALDO":[]}
    if lista_extrato==[]:
        print('---------------------')
        print('Extrato Vazio')
        print('---------------------')
        main()
    for element in lista_extrato:
        if 'removido' in element:
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
        
    main()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

################################################
# FUNÇÃO PARA CARREGAR O FICHEIRO TRANSACTIONS #
################################################

def carregar_ficheiro_extrato():
    lst=[]
    with open("transactions.txt") as file:
        for line in file:
            lst.append(line.strip().split(","))
    if lst==[]:
        os.system('cls')
        return lst
    for element in lst:
        element[1]=int(element[1])
    return lst

#-----------------------------------------------

############################################################
#    FUNÇÃO PARA ADICIONAR UMA NOVA LINHA A UM FICHEIRO    #
############################################################

def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

#-----------------------------------------------------------

###########################################################################################################################################################################################################################################################################################
#                                                                                                   FUNÇÃO PARA REGISTAR AS TRANSAÇÕES NO FICHEIRO TRANSACTIONS                                                                                                                           #
###########################################################################################################################################################################################################################################################################################

def transferencias(moeda,quantidade,quantidade_inicial,quantidade_modificada,total,tipo_operacao):
    filetrans='transactions.txt'
    filetransedit=open(filetrans, 'a+')
    string_moeda=str(moeda)
    string_quantidade=str(quantidade)
    string_quantidade_inicial=str(quantidade_inicial)
    string_quantidade_modificada=str(quantidade_modificada)
    string_total=str(total)
    append_new_line('transactions.txt',datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ',' + string_moeda+ ',' + string_quantidade +',' + string_quantidade_inicial + ',' + string_quantidade_modificada + ',' +string_total + ',' + tipo_operacao + ',' + ver_saldo(carregar_ficheiro()))
    filetransedit.close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

###############################################
#   FUNÇÃO PARA CARREGAR O FICHEIRO WALLET    #
###############################################

def carregar_ficheiro():
    lst=[]
    with open("wallet.txt") as file:
        for line in file:
            lst.append(line.strip().split(","))
    for element in lst:
        element[1]=int(element[1])
    return lst

#----------------------------------------------

############################################
#         FUNÇÃO PARA VER O SALDO          #
############################################
def ver_saldo(wallet_list):
    total_carteira=0
    for sublist in wallet_list:
        moeda=sublist[0]
        quantidade=sublist[1]
        total=float(moeda)*float(quantidade)
        total_carteira+=total
    saldo=str(total_carteira)+'€'
    return saldo

#-------------------------------------------

############################################################################################################
#                             FUNÇÃO PARA VISUALIZAR O CONTEÚDO DA CARTEIRA                                #
############################################################################################################

def ver_carteira(wallet_list):
    os.system('cls')
    print('---------------------------VER CARTEIRA---------------------------')
    print("{:^20} {:^5} {:^10} {:^5} {:^10}".format("TIPO DE MOEDA","|","QUANTIDADE ADQUIRIDA","|","TOTAL"))
    print("------------------------------------------------------------------")
    total_carteira=0
    for sublist in wallet_list:
        moeda=sublist[0]
        tipo_moeda=str(moeda)+'€'
        quantidade=sublist[1]
        total=float(moeda)*float(quantidade)
        total_carteira+=total
        y=str(total)+'€'
        print("{:^20} {:^5} {:^20} {:^5} {:^10}".format(tipo_moeda,"|", quantidade,"|", y))
        print("------------------------------------------------------------------")
    x=str(total_carteira)+'€'
    print('{:>20} {:^5} {:^20} {:^5} {:^10}'.format('','','TOTAL NA CARTEIRA','|',x))
    print("------------------------------------------------------------------")
    main()

#-----------------------------------------------------------------------------------------------------------

#####################################################################################################################
#                                               FUNÇÃO PARA ADICIONAR CRÉDITOS                                      #
#####################################################################################################################

def adicionar_creditos(wallet_list):
    os.system('cls')
    print('---------------------------------------------ADICIONAR CRÉDITOS-----------------------------------------')
    print('USE 999 PARA VOLTAR ATRÁS')
    print('')
    moeda=input('Que tipo de moeda deseja adicionar?\n')
    lst_numerario=[]
    for element in wallet_list:
        lst_numerario.append(element[0])
    if moeda=='999':
        os.system('cls')
        main()
    elif moeda not in lst_numerario:
        print('---------------------------------------')
        print('Moeda não existe. TENTE OUTRA VEZ')
        print('---------------------------------------')
        adicionar_creditos(carregar_ficheiro())
    print('')
    print('')
    quantidade=input('Quantidade da moeda a ser adicionada(se introduziu a moeda errada insira B):\n')
    quantidade=quantidade.upper()
    if quantidade=='B':
        adicionar_creditos(carregar_ficheiro())
    file='wallet.txt'
    for element in wallet_list:
        if element[0]==moeda:
            quantidade_inicial=element[1]
    quantidade_modificada=int(quantidade)+int(quantidade_inicial)
    
    os.system('cls')
    if modificar_ficheiro(wallet_list,file,moeda, str(quantidade_modificada))==True:
        moedaint=float(moeda) 
        intquant=float(quantidade)
        transferencias(moeda,quantidade,quantidade_inicial,quantidade_modificada,intquant*moedaint,'adicionar')
        print('------------------------')
        print('Adicionado', intquant*moedaint,'€')
        print('------------------------')
    else:
        print('-------------------')
        print('Erro na transação')
        print('--------------------')
    main()

#--------------------------------------------------------------------------------------------------------------------

##############################################################################################################
#                                           FUNÇÃO PARA REMOVER CRÉDITOS                                     #
##############################################################################################################

def remover_creditos(wallet_list):
    os.system('cls')
    print('-------------------------REMOVER CRÉDITOS-------------------------')
    print('')
    print("{:^20} {:^5} {:^10} {:^5} {:^10}".format("TIPO DE MOEDA","|","QUANTIDADE ADQUIRIDA","|","TOTAL"))
    print("------------------------------------------------------------------")
    total_carteira=0
    for sublist in wallet_list:
        moeda=sublist[0]
        tipo_moeda=str(moeda)+'€'
        quantidade=sublist[1]
        total=float(moeda)*float(quantidade)
        total_carteira+=total
        y=str(total)+'€'
        print("{:^20} {:^5} {:^20} {:^5} {:^10}".format(tipo_moeda,"|", quantidade,"|", y))
        print("------------------------------------------------------------------")
    x=str(total_carteira)+'€'
    print('{:>20} {:^5} {:^20} {:^5} {:^10}'.format('','','TOTAL NA CARTEIRA','|',x))
    print("------------------------------------------------------------------")
    print('')
    print('USE 999 PARA VOLTAR ATRÁS')
    print('')
    moeda=input('Que tipo de moeda deseja remover?\n')
    lst_numerario=[]
    for element in wallet_list:
        lst_numerario.append(element[0])
    if moeda=='999':
        os.system('cls')
        main()    
    elif moeda not in lst_numerario:
        remover_creditos(carregar_ficheiro())
    print('')
    quantidade=input('Quantidade da moeda a ser removida(se introduziu a moeda errada insira B):\n')
    quantidade=quantidade.upper()
    if quantidade=='B':
        remover_creditos(carregar_ficheiro())
    intquanti=int(quantidade)
    for element in wallet_list:
        if element[0]==moeda:
            if element[1]<intquanti:
                os.system('cls')
                print('----------------------------------------')
                print('Não possui esta quantidade de moedas')
                print('----------------------------------------')
                main()

    if quantidade=='555':
        remover_creditos(carregar_ficheiro())
    file='wallet.txt'
    for element in wallet_list:
        if element[0]==moeda:
            quantidade_inicial=element[1]
    inteiro_quantidade=int(quantidade)
    if inteiro_quantidade>quantidade_inicial:
        return 'ERRO: Saldo negativo'
    quantidade_modificada=int(quantidade_inicial)-int(quantidade)
    os.system('cls')
    if modificar_ficheiro(wallet_list,file,moeda, str(quantidade_modificada))==True:
        moedaint=int(moeda)
        intquant=int(quantidade)
        transferencias(moeda,quantidade,quantidade_inicial,quantidade_modificada,intquant*moedaint,'removido')
        print('-------------------')
        print('Removido', intquant*moedaint,'€')
        print('-------------------')
    else:
        print('-------------------')
        print('Erro na transação')
        print('-------------------')
    main()

#-------------------------------------------------------------------------------------------------------------

######################################################################
#   FUNÇÃO PARA MODIFICAR O FICHEIRO WALLET DEPOIS DE UMA OPERAÇÃO   #
######################################################################

def modificar_ficheiro(carteira,ficheiro,moeda,quantidade_modificada):
    for element in carteira:
        if element[0]==moeda:
            element[1]=quantidade_modificada
    fileop=open(ficheiro,'w')
    for element in carteira:
        fileop.write(str(element[0])+','+str(element[1])+'\n')
    for element in carteira:
        if element[0]==moeda:
            if element[1]==quantidade_modificada:
                return True
            else:
                return False

#---------------------------------------------------------------------

################################################################################################################################################################################################################################################
#                                                                               FUNÇÃO PARA RESETAR A CARTEIRA                                                                                                                                 #
################################################################################################################################################################################################################################################

def reset_carteira(wallet_list):
    os.system('cls')
    print('---------------------RESET DA CARTEIRA---------------------')
    print('')
    confirm=input('Tem a certeza que deseja resetar a sua carteira?(Y/n):\n')
    if confirm=='Y':
        file='wallet.txt'
        for element in wallet_list:
            element[1]=0
        modificar_ficheiro(wallet_list, file, 0, 0)
        append_new_line('transactions.txt',datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ',' + '9999999999999999'+ ',' + '9999999999999999'+',' + '9999999999999999' + ',' + '9999999999999999' + ',' + '' + ',' + '9999999999999999' + ',' + '')
        os.system('cls')
        print('---------------------')
        print('CARTEIRA RESETADA')
        print('---------------------')
    else:
        os.system('cls')
        print('--------------------------')
        print('CARTEIRA NÃO RESETADA')
        print('--------------------------')
    
    main()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

##################################################################################################################################################################    
#                                                              FUNÇÃO PARA ENVIAR OS DETALHES DA CONTA POR EMAIL                                                 #
##################################################################################################################################################################

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
        main()
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
    main()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------   

###################################################################################################
#                                             MENU                                                #
###################################################################################################

def main():
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
    print('__________________________________________________')
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
        
        main()

#--------------------------------------------------------------------------------------------------

################################################
# INICIAR O PROGRAMA COM A JANELA MAXIMIZADA   #
################################################

hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

#----------------------------------------------

###############################################
#               INICIAR O PROGRAMA            #
###############################################
if __name__ == '__main__':
    main()    
#----------------------------------------------