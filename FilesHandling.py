import os
import csv


# Função para carregar o ficheiro wallet.csv
# string -> list[string[]]
def carregar_ficheiro(file):
    lst = []
    if file not in os.listdir():
        csv_file = open(file, 'w')
        if file == 'wallet.csv':
            csv_file.write('0.01,0\n0.02,0\n0.05,0\n0.1,0\n0.2,0\n0.5,0\n1,0\n2,0\n5,0\n10,0\n20,0\n50,0\n100,0\n500,0')
        elif file == 'emprestimos.csv':
            csv_file.write('')
        csv_file.close()
    csv_reader = csv.reader(open(file), delimiter=',')
    for row in csv_reader:
        if row != []:
            lst.append(row)
    return lst


# Função para modificar o ficheiro wallet.csv
# list[string[]], string, string, int -> boolean
def modificar_ficheiro(carteira,ficheiro,moeda,quantidade_modificada):
    fileop=open(ficheiro,'w')

    for element in carteira:
        if element[0] == moeda:
            element[1] = str(quantidade_modificada)
        fileop.write(element[0] + ',' + element[1] + '\n')

    fileop.close()

    for element in carteira:
        if element[0] == moeda and element[1] == str(quantidade_modificada):    
            return True

    return False


# Função para modificar o ficheiro emprestimos.csv
# list[string[]], string, string, string, string, string, string -> boolean
def modificar_ficheiro_emprestimos(lista_emprestimos,ficheiro,moeda_emprestimo,quantidade_emprestimo, pessoa,data_emprestimo,codigo_emprestimo):
    fileop=open(ficheiro,'w')
    
    for element in lista_emprestimos:
        if (element[1]==moeda_emprestimo) and (element[2]==quantidade_emprestimo) and(element[4]==pessoa) and (element[0]==data_emprestimo) and(element[6]==codigo_emprestimo):
            element[5]='Resolvido'
        fileop.write(element[0]+','+element[1]+','+element[2]+','+element[3]+','+element[4]+','+element[5]+','+element[6]+'\n')
    
    fileop.close()
    
    for element in lista_emprestimos:
        if element[4]==pessoa and element[1]==moeda_emprestimo and element[2]==quantidade_emprestimo and element[0] == data_emprestimo:
            return True
    
    return False


# Função para adicionar uma nova linha de informação a um ficheiro
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