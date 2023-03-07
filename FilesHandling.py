import os



# Função para carregar o ficheiro wallet.csv
def carregar_ficheiro():
    lst=[]
    with open("wallet.csv") as file:
        for line in file:
            lst.append(line.strip().split(","))
    for element in lst:
        element[1]=int(element[1])
    return lst


# Função para carregar o ficheiro emprestimos.csv
def carregar_ficheiro_emprestimos():
    lst=[]
    with open("emprestimos.csv") as file:
        for line in file:
            lst.append(line.strip().split(","))
    newlst=[]
    for element in lst:
        if element[0]!='':
            newlst.append(element)
    file_open=open('emprestimos.csv', 'w')
    for element in newlst:
        file_open.write(element[0]+','+element[1]+','+element[2]+','+element[3]+','+element[4]+','+element[5]+','+element[6]+'\n')
        element[1]=int(element[1])
    return newlst


# Função para carregar o ficheiro transactions.csv
def carregar_ficheiro_extrato():
    lst=[]
    with open("transactions.csv") as file:
        for line in file:
            lst.append(line.strip().split(","))
    if lst==[]:
        os.system('cls')
        return lst
    for element in lst:
        element[1]=int(element[1])
    return lst


# Função para modificar o ficheiro wallet.csv
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


# Função para modificar o ficheiro emprestimos.csv
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