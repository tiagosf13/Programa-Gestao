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


# Função para adicionar créditos à carteira
def adicionar_creditos(wallet_list):
    moeda, quantidade = operations_add_remove_loan(wallet_list, 'adicionar')

    if moeda==None and quantidade==None:
        return

    for element in wallet_list:
        if element[0]==moeda:
            quantidade_inicial=element[1]
    quantidade_modificada=int(quantidade)+int(quantidade_inicial)

    os.system('cls')
    if modificar_ficheiro(wallet_list,'wallet.csv',moeda, str(quantidade_modificada))==True:
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


# Função para remover créditos da carteira
def remover_creditos(wallet_list):
    moeda, quantidade = operations_add_remove_loan(wallet_list, 'remover')

    if moeda==None and quantidade==None:
        return

    for element in wallet_list:
        if element[0]==moeda:
            if element[1]<int(quantidade):
                os.system('cls')
                print('----------------------------------------')
                print('Não possui esta quantidade de moedas')
                print('----------------------------------------')
                return

    for element in wallet_list:
        if element[0]==moeda:
            quantidade_inicial=element[1]
    if int(quantidade)>quantidade_inicial:
        return
    quantidade_modificada=int(quantidade_inicial)-int(quantidade)
    os.system('cls')
    if modificar_ficheiro(wallet_list,'wallet.csv',moeda, str(quantidade_modificada))==True:
        transferencias(moeda,quantidade,quantidade_inicial,quantidade_modificada,int(quantidade)*int(moeda),'removido')
        print('-------------------')
        print('Removido', int(quantidade)*int(moeda),'€')
        print('-------------------')
    else:
        print('-------------------')
        print('Erro na transação')
        print('-------------------')


# Função que permite ao utilizador emprestar créditos
def emprestimo(wallet_list):
    moeda, quantidade = operations_add_remove_loan(wallet_list, 'emprestar')

    if moeda==None and quantidade==None:
        return

    for element in wallet_list:
        if element[0]==moeda:
            if element[1]<int(quantidade):
                os.system('cls')
                print('----------------------------------------')
                print('Não possui esta quantidade de moedas')
                print('----------------------------------------')
                return
    print('')
    pessoa_emprestimo=input('Insira a pessoa a quem se destina o empréstimo:\n')
    pessoa_emprestimo=pessoa_emprestimo[0].upper()+pessoa_emprestimo[1:]

    for element in wallet_list:
        if element[0]==moeda:
            quantidade_inicial=int(element[1])
            if int(quantidade)<=quantidade_inicial:
                quantidade_final=quantidade_inicial-int(quantidade)
    valor=int(moeda)*int(quantidade)
    valor=str(valor)
    codigo_ficheiro_emprestimo=str(codigo())
    situacao_emprestimo='Por Resolver'
    append_new_line('emprestimos.csv',datetime.today().strftime('%Y-%m-%d %H:%M:%S')+','+ moeda +','+quantidade+','+valor+','+pessoa_emprestimo+','+situacao_emprestimo+','+codigo_ficheiro_emprestimo)
    os.system('cls')
    if modificar_ficheiro(wallet_list,'wallet.csv',moeda,quantidade_final)==True:
        valor='-'+valor
        transferencias(moeda,quantidade,quantidade_inicial,quantidade_final,valor,'removido(emprestimo)')
        print('-----------------------------------')
        print('Emprestado', valor,'€ a',pessoa_emprestimo)
        print('')
        print('Código do Empréstimo:',codigo_ficheiro_emprestimo)
        print('-----------------------------------')
    else:
        print('-------------------')
        print('Erro na transação')
        print('--------------------')


# Função para resolver empréstimos
def resolver_emprestimo(lista_emprestimos,wallet_list):
    if lista_emprestimos==[]:
        print('---------------------------')
        print('Não tem empréstimos')
        print('---------------------------')
        return
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
        return
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
        return
    for element in lista_emprestimos:
        data=element[0]
        moeda=element[1]
        quantidade=element[2]
        valor=element[3]
        pessoa=element[4]
        codigo=element[6]
        if codigo_utilizador == codigo:
            print('')
            print('---------------------------------------------------')
            print('Empréstimo:')
            print('Data: ',data)
            print('Moeda: ',moeda)
            print('Quantidade: ',quantidade)
            print('Valor do Empréstimo: ',valor)
            print('Pessoa: ',pessoa)
            print('Código: ',codigo)
            print('---------------------------------------------------')
            file='wallet.csv'
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
                append_new_line('transactions.csv',datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ',' + str(moeda)+ ',' + quantidade+',' + quantidade_inicial_str + ',' + quantidade_modificada_str + ',' + total + ',' + tipo_operacao + ',' + ver_saldo(carregar_ficheiro()))
                file_emprestimos='emprestimos.csv'
                if modificar_ficheiro_emprestimos(carregar_ficheiro_emprestimos(),file_emprestimos,moeda,quantidade, pessoa,data,codigo):
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
        os.system('cls')
        return
    print('----------------------------------------------------------------------------------------EMPRÉSTIMOS-----------------------------------------------------------------------------------')
    print('')
    print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^16} {:^5} {:>15} {:>12} {:>15}'.format('DATA DO EMPRÉSTIMO','|','MOEDA','|','QUANTIDADE','|','VALOR EMPRESTADO','|','PESSOA','|','CÓDIGO','|','SITUAÇÃO'))
    print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for element in lista_emprestimos:
        print('{:>20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^20} {:^5} {:^16} {:^5} {:>17} {:>10} {:>17}'.format(element[0],'|',element[1],'|',element[2],'|',element[3],'|',element[4],'|',element[6],'|',element[5]))
        print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')


# Função para ver extrato
def ver_extrato(lista_extrato):
    dic_extrato={"DATA DA TRANSAÇÃO":[],"MOEDA":[],"QUANTIDADE TRANSFERIDA":[],"QUANTIDADE INICIAL":[],"QUANTIDADE FINAL":[],"TOTAL DA OPERAÇÃO":[],"SALDO":[]}
    if lista_extrato==[]:
        print('---------------------')
        print('Extrato Vazio')
        print('---------------------')
        return
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