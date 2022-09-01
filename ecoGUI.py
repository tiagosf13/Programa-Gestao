import collections
import datetime
from email.errors import MissingHeaderBodySeparatorDefect
from logging import root
from tkinter import *
import os
from tkinter.ttk import Treeview
from turtle import title

from eco import adicionar_creditos, emprestimo, enviar_email, remover_creditos, reset_carteira, resolver_emprestimo


def carregar_ficheiro():
    lst=[]
    with open("wallet.txt") as file:
        for line in file:
            lst.append(line.strip().split(","))
    for element in lst:
        element[1]=int(element[1])
    return lst

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

def adicionar_creditos(wallet_list):#modificar esta funcao
    moeda=input('Que tipo de moeda deseja adicionar?\n')
    lst_numerario=[]
    for element in wallet_list:
        lst_numerario.append(element[0])
    if moeda not in lst_numerario:
        print("moeda nao existe")
        #moeda nao existe
    quantidade=input('Quantidade da moeda a ser adicionada(se introduziu a moeda errada insira B):\n')
    quantidade=quantidade.upper()
    file='wallet.txt'
    for element in wallet_list:
        if element[0]==moeda:
            quantidade_inicial=element[1]
    quantidade_modificada=int(quantidade)+int(quantidade_inicial)
    
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

variable = 0
def radio_clicked(value, quantidade):
    
    global variable, total_label

    dic_values = {1 : 0.01, 2 : 0.02, 3 : 0.05, 4 : 0.1, 5 : 0.2, 6 : 0.5, 7 : 1, 8 : 2, 9 : 5, 10 : 10, 11 : 20, 12 : 50, 13 : 100, 14 : 500}
    total = float(quantidade)*float(dic_values[value])
    if variable == 0:
        total_label = Label(root, text="Total:"+str(dic_values[value])+"x"+str(quantidade)+"="+str(total)+"€")
        variable+=1
        total_label.grid(column=7, row=5)
    else:
        total_label.config(text="Total:"+str(dic_values[value])+"x"+str(quantidade)+"="+str(total)+"€")

lst_radio_buttons_adicionar_credito_window = []
def adicionar_credito_window():

    global radio_button1, radio_button2, radio_button3, radio_button4, radio_button5, radio_button6, radio_button7, radio_button8, radio_button9, radio_button10, radio_button11, radio_button12, radio_button13, radio_button14, previous_page_buttons_adicionar, tipo_moeda_label, total_label
    global entrada
    
    variable = 0
    previous_page_buttons_adicionar = Button(root, text="Voltar", command=back_adicionar_credito)
    previous_page_buttons_adicionar.grid(column=7, row=12)
    adicionar_credito_buttons = Button(root, text="Adicionar")#, command=adicionar_creditos
    adicionar_creditos_buttons.grid(column=8, row=12)

    instructions.destroy()
    operations.destroy()
    ver_carteira_buttons.destroy()
    adicionar_creditos_buttons.destroy()
    emprestimo_buttons.destroy()
    enviar_email_buttons.destroy()
    remover_creditos_buttons.destroy()
    consultar_emprestimo_buttons.destroy()
    consultar_extratos_buttons.destroy()
    reset_carteira_buttons.destroy()
    resolver_emprestimo_buttons.destroy()

    r = IntVar()
    r.set("7")
    canvas.grid(columnspan=15, rowspan=30)

    tipo_moeda_label = Label(root, text="MOEDA")
    tipo_moeda_label.grid(column=7, row=2)
    
    radio_button1 = Radiobutton(root, text="0.01", variable=r, value=1, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button1.grid(column=1, row=4)
    radio_button2 = Radiobutton(root, text="0.02", variable=r, value=2, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button2.grid(column=2, row=4)
    radio_button3 = Radiobutton(root, text="0.05", variable=r, value=3, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button3.grid(column=3, row=4)
    radio_button4 = Radiobutton(root, text="0.1", variable=r, value=4, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button4.grid(column=4, row=4)
    radio_button5 = Radiobutton(root, text="0.2", variable=r, value=5, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button5.grid(column=5, row=4)
    radio_button6 = Radiobutton(root, text="0.5", variable=r, value=6, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button6.grid(column=6, row=4)
    radio_button7 = Radiobutton(root, text="1", variable=r, value=7, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button7.grid(column=7, row=4)
    radio_button8 = Radiobutton(root, text="2", variable=r, value=8, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button8.grid(column=8, row=4)
    radio_button9 = Radiobutton(root, text="5", variable=r, value=9, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button9.grid(column=9, row=4)
    radio_button10 = Radiobutton(root, text="10", variable=r, value=10, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button10.grid(column=10, row=4)
    radio_button11 = Radiobutton(root, text="20", variable=r, value=11, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button11.grid(column=11, row=4)
    radio_button12 = Radiobutton(root, text="50", variable=r, value=12, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button12.grid(column=12, row=4)
    radio_button13 = Radiobutton(root, text="100", variable=r, value=13, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button13.grid(column=13, row=4)
    radio_button14 = Radiobutton(root, text="500", variable=r, value=14, command=lambda: radio_clicked(r.get(), entrada.get()))
    radio_button14.grid(column=14, row=4)

    lst_radio_buttons_adicionar_credito_window.append(radio_button1)
    lst_radio_buttons_adicionar_credito_window.append(radio_button2)
    lst_radio_buttons_adicionar_credito_window.append(radio_button3)
    lst_radio_buttons_adicionar_credito_window.append(radio_button4)
    lst_radio_buttons_adicionar_credito_window.append(radio_button5)
    lst_radio_buttons_adicionar_credito_window.append(radio_button6)
    lst_radio_buttons_adicionar_credito_window.append(radio_button7)
    lst_radio_buttons_adicionar_credito_window.append(radio_button8)
    lst_radio_buttons_adicionar_credito_window.append(radio_button9)
    lst_radio_buttons_adicionar_credito_window.append(radio_button10)
    lst_radio_buttons_adicionar_credito_window.append(radio_button11)
    lst_radio_buttons_adicionar_credito_window.append(radio_button12)
    lst_radio_buttons_adicionar_credito_window.append(radio_button13)
    lst_radio_buttons_adicionar_credito_window.append(radio_button14)

    entrada = Entry(root)
    entrada.grid(column=7, row=6)

def main_window():

    global instructions, operations, ver_carteira_buttons, adicionar_creditos_buttons, emprestimo_buttons, enviar_email_buttons, remover_creditos_buttons, consultar_emprestimo_buttons, consultar_extratos_buttons, reset_carteira_buttons, resolver_emprestimo_buttons

    canvas.grid(columnspan=3, rowspan=30)
    #instructions
    instructions = Label(root, text="Welcome to the Eco!\n\nPlease select a operation to run.")
    instructions.grid(column=1, row=0)

    #operations
    operations = Label(root, text="OPERAÇÕES")
    operations.grid(column=1, row=11)

    #operation buttons
    ver_carteira_buttons = Button(root, text="Ver Carteira", command=lambda: [print("Operation : Ver Carteira"), ver_carteira_window()], padx=30)
    ver_carteira_buttons.grid(column=1, row=12)

    adicionar_creditos_buttons = Button(root, text="Adicionar Creditos", command=lambda: [print("Operation : Adicionar Creditos"), adicionar_credito_window()], padx=11)
    adicionar_creditos_buttons.grid(column=1, row=13)

    remover_creditos_buttons = Button(root, text="Remover Creditos", command=lambda: print("Operation : Remover Creditos"), padx=13)
    remover_creditos_buttons.grid(column=1, row=14)

    emprestimo_buttons = Button(root, text="Emprestimo Creditos", command=lambda: print("Operation : Emprestimo Creditos"), padx=5)
    emprestimo_buttons.grid(column=1, row=15)

    resolver_emprestimo_buttons = Button(root, text="Resolver Emprestimo", command=lambda: print("Operation : Resolver Emprestimo"), padx=5)
    resolver_emprestimo_buttons.grid(column=1, row=16)

    consultar_emprestimo_buttons = Button(root, text="Consultar Emprestimo", command=lambda: print("Operation : Consultar Emprestimo"))
    consultar_emprestimo_buttons.grid(column=1, row=17)

    consultar_extratos_buttons = Button(root, text="Consultar Extratos", command=lambda: print("Operation : Consultar Extratos"), padx=12)
    consultar_extratos_buttons.grid(column=1, row=18)

    reset_carteira_buttons = Button(root, text="Reset Carteira", command=lambda: print("Operation : Reset Carteira"), padx=24)
    reset_carteira_buttons.grid(column=1, row=19)

    enviar_email_buttons = Button(root, text="Enviar Email", command=lambda: print("Operation : Enviar Email"), padx=28)
    enviar_email_buttons.grid(column=1, row=20)

def back_adicionar_credito():
    for element in lst_radio_buttons_adicionar_credito_window:
        element.grid_forget()
    previous_page_buttons_adicionar.destroy()
    tipo_moeda_label.destroy()
    total_label.destroy()
    main_window()

def back_ver_carteira():
    tabela.destroy()
    previous_page_buttons_ver_carteira.destroy()
    main_window()

def ver_carteira_window():

    global tabela, previous_page_buttons_ver_carteira

    instructions.destroy()
    operations.destroy()
    ver_carteira_buttons.destroy()
    adicionar_creditos_buttons.destroy()
    emprestimo_buttons.destroy()
    enviar_email_buttons.destroy()
    remover_creditos_buttons.destroy()
    consultar_emprestimo_buttons.destroy()
    consultar_extratos_buttons.destroy()
    reset_carteira_buttons.destroy()
    resolver_emprestimo_buttons.destroy()
    previous_page_buttons_ver_carteira = Button(root, text="Voltar", command=back_ver_carteira)
    previous_page_buttons_ver_carteira.grid(column=1, row=12)
    
    tabela = Treeview(root)
    #definir as colunas
    tabela["columns"] = ("TIPO DE MOEDA", "QUANTIDADE ADQUIRIDA", "TOTAL")

    #formatar as colunas
    tabela.column("#0", width=0, minwidth=0, anchor=W)
    tabela.column("TIPO DE MOEDA", width=180, minwidth=20, anchor=CENTER)
    tabela.column("QUANTIDADE ADQUIRIDA", width=180, minwidth=20, anchor=CENTER)
    tabela.column("TOTAL", width=180, minwidth=20, anchor=CENTER)

    #create headings
    tabela.heading("TIPO DE MOEDA", text="TIPO DE MOEDA", anchor=CENTER)
    tabela.heading("QUANTIDADE ADQUIRIDA", text="QUANTIDADE ADQUIRIDA", anchor=CENTER)
    tabela.heading("TOTAL", text="TOTAL", anchor=CENTER)

    #add data
    for element in carregar_ficheiro():
        tabela.insert(parent="", index="end", text="", values=(element[0], element[1], float(element[0]) * float(element[1])))
    tabela.grid(column=1, row=1)

root = Tk()

root.title("Gestão Financeira")
global canvas
canvas = Canvas(root, width=720, height=450)
main_window()
root.mainloop()