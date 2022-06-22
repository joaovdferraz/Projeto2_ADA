import csv


def le_dados()->list|None:
    """
    Tenta abrir a planilha, retorna uma lista caso consiga, caso contrário retorna None
    """
    try:
        with open("dados.csv","r",encoding='utf8') as arquivo:
            planilha = list(csv.reader(arquivo, delimiter=';', lineterminator='\n'))
            return planilha
    except:
        print("Nenhum músico está cadastrado no banco de dados, favor cadastre algum músico")
        return None


def valida_numero(tipo:str) -> int:
    """
    Função recebe uma string retorna um inteiro maior que 0
    """
    numero = -1
    while numero<0:
        try:
            numero = int(input(tipo))
            if numero <= 0 : 
                raise Exception("número deve ser maior que 0 ")
        except:
            print ("Por favor, insira um valor inteiro maior que 0 ")
    return numero


def valida_escolha_12(texto: str) -> str:
    """
    Função recebe uma string retorna uma string e retorna uma string com valor 1 ou 2
    """
    escolha = "0"
    while escolha not in ["1","2"]:
        try:
            escolha =  input(texto)
            if escolha not in ["1","2"]:
                raise Exception("Valor digitado inválido")
        except:
            print("Valor inválido, digite 1 ou 2")
    return escolha


def procura_email(email:str) -> bool:
    """
    Função recebe uma string e retorna um booleano
    """
    try:
        with open("dados.csv","r") as arquivo:
            planilha = list(csv.reader(arquivo, delimiter=';', lineterminator='\n'))
    except:
        return False
    flag = False
    for linha in planilha:
        if linha[1] == email:
            flag = True
    return flag


def valida_email() -> str|bool:
    """
    Função retorna um e-mail válido ou um booleano caso o usuário não queira mais realizar um cadastro.
    """
    caracteres = "abcdefghijklmnopqrstuvwxyz0123456789@_."
    flag = False
    while flag == False:
        try:
            email = input("Digite o e-mail para cadastro ").lower()
            if email.count("@") != 1:
                print ("e-mail deve conter apenas uma @")
                raise Exception("e-mail deve conter exatamente 1 @")
            for letra in email:
                if letra not in caracteres:
                    print("e-mail possui caracter inválido")
                    raise Exception("e-mail contém caracter inválido")   
            if  procura_email(email):
                opção = valida_escolha_12("E-mail já cadastrado, digite 1 para cadastrar outro e-mail ou 2 para cancelar o cadastro ")
                if opção =="2" : return False             
            flag=True
        except:
            print("Favor digitar um endereço de e-mail valido")        
    return email

def valida_nome() -> str:
    flag = False
    while flag == False:
        try:
            nome = input("Digite o nome para cadastro ").lower()
            for letra in nome:
                if not("a"<=letra<="z" or letra==" ") :
                    print("Nome possui caracter inválido")
                    raise Exception("Nome contém caracter inválido")  
            flag=True
        except:
            print("Favor digitar um nome válido")        
    return nome  


def realiza_cadastro(info:list,tipo:bool) -> None:
    """
    Recebe uma lista e um booleano e escreve os dados em um arquivo
    """


    try: 
        if tipo:
            with open("dados.csv","a",encoding='utf8') as arquivo:
                escritor = csv.writer(arquivo, delimiter=';', lineterminator='\n')
                escritor.writerow(info) 
                print("Usuário cadastrado com sucesso")
        else:
            with open("dados.csv","w",encoding='utf8') as arquivo:
                escritor = csv.writer(arquivo, delimiter=';', lineterminator='\n')
                escritor.writerows(info) 
                print("Usuário modificado com sucesso")
    except:
        print("Impossível abrir o arquivo do banco de dados, verifique se ele já está aberto")


def cadastrar_musicos() -> None:
    """
    Recebe as informações para realizar um cadastro
    """
    nome = valida_nome()
    email = valida_email()
    if email == False: return    
    numero_generos = valida_numero("Digite a quantidade de gêneros que deseja cadastrar ")    
    generos = [input(f"Digite o {n+1}° gênero que deseja cadastrar ").lower() for n in range(numero_generos)]
    numero_instrumentos = valida_numero("Digite a quantidade de instrumentos que deseja cadastrar ")
    instrumentos = [input(f"Digite o {n+1}° instrumento que deseja cadastrar ").lower() for n in range(numero_instrumentos)]
    confirma = valida_escolha_12("Os dados inseridos foram:\n"
                        f"nome: {nome}\n"
                        f"email: {email}\n"
                        f"genero{'s'*bool(len(generos)>1)}: {limpa_resultado(str(generos))}\n"
                        f"instrumento{'s'*bool(len(instrumentos)>1)}: {limpa_resultado(str(instrumentos))}\n"
                        "Digite 1 para confirmar os dados ou 2 para preencher os dados novamente\n ")
    if confirma =="1" : 
        lista_cadastro = [nome,email,generos,instrumentos]
        realiza_cadastro(lista_cadastro,True)
    else:
         cadastrar_musicos()
    print()
    return


def limpa_lista(lista:list)->list:
    """
    Recebe uma lista e retorna uma nova lista.
    """
    lista_limpa = [valor.replace("[","").replace("'","").replace("]","").split(", ") for valor in lista]
    return lista_limpa    

def limpa_resultado(resultado:str) -> str:
    """
    Recebe uma string e retorna uma nova string
    """
    novo_resultado = resultado.replace("[","").replace("'","").replace("]","")
    return novo_resultado
        
def compara_listas(lista:list,lista2:list,todos:bool=False) -> bool :    
    """
    Recebe 2 listas e um booleano e realiza uma comparação entre as listas retornando um booleano
    """
    auxilio = 0    
    for elemento in lista:
        for elemento2 in lista2:
            if elemento in elemento2:
                if not todos: return True
                auxilio +=  1     
    return auxilio >= len(lista)


def valida_opção_busca() -> str:
    """
    Pergunta ao usuário qual opção ele deseja e retorna uma string
    """
    opção = [""]
    while not compara_listas(opção,[["nome"],["e-mail"],["instrumento"],["gênero"]],True) or not opção:
        try:
            opção =  input("Digite as opções que deseja buscar. Selecione ao menos 1, separe as opções que deseja com um espaço\n"
                            "opções disponíveis = nome, e-mail, instrumento, gênero ").lower().split()
            if not compara_listas(opção,[["nome"],["e-mail"],["instrumento"],["gênero"]],True) or not opção:
                raise Exception("Inserido valor inválido")
        except:
            print("Valor digitado inválido")
    return opção


def buscar_musicos() -> None :  
    """
    Imprime uma lista de valores com base em informações fornecidas pelo usuário
    """  
    opções = valida_opção_busca()
    if len(opções)>1:
        modo = valida_escolha_12("Digite 1 caso deseje que os resultados batam com todas as informações digitadas\n"
                        "ou 2 caso deseja que os resultados batam pelo menos uma das informações digitadas ")
    else: modo = "1"
    valores_buscados = [input(f"Digite o {valor} que deseja buscar ") for valor in opções]
    planilha = le_dados()
    if planilha == None: return
    resultado = []
    if modo == "1":
        resultado = [linha for linha in planilha if compara_listas(valores_buscados,limpa_lista(linha),True)]  
    if modo == "2":
        resultado = [linha for linha in planilha if compara_listas(valores_buscados,limpa_lista(linha))]
    if not resultado:
            print("Não foram encontrados resultados para sua busca")
    else:
        print("Os resultados encontrados foram:")
        for indice,pessoa in enumerate(resultado):
            print(f"Músico {indice+1}:\nNome: {pessoa[0]} ; E-mail: {pessoa[1]} ; Gênero{'s'*(len(pessoa[2].split())>1)}: {limpa_resultado(pessoa[2])}"
             f" ; Instrumento{'s'*(len(pessoa[3].split())>1)}: {limpa_resultado(pessoa[3])}\n")
    return       


def valida_email_modifica() -> str|None:
    """
    Pede para o usuário digitar o e-mail e retorna uma string
    """
    flag = False
    while flag == False:   
        email = input("Digite o e-mail do usuário que deseja modificar ").lower()
        flag = procura_email(email)
        if flag == False:
            opção = valida_escolha_12("E-mail não encontrado digite 1 caso deseje modificar outro e-mail ou 2 para encerrar a modificação ")
            if opção == "2" : return None
    return email


def modifica_linha(linha:list,opção:str) ->list:
    """
    Recebe uma lista e uma string e retorna uma lista contendo informações digitadas pelo usuário
    """
    nova_linha = linha.copy()
    if opção in ["1","3"]:
        numero_generos = valida_numero("Digite a quantidade de gêneros que deseja cadastrar ")    
        nova_linha[2] = [input("Digite o gênero que deseja cadastrar ").lower() for n in range(numero_generos)]
    if opção in ["2","3"]:
        numero_instrumentos = valida_numero("Digite a quantidade de instrumentos que deseja cadastrar ")
        nova_linha[3] = [input("Digite o instrumento que deseja cadastrar ").lower() for n in range(numero_instrumentos)]
    return nova_linha


def modificar_musicos()-> None:
    """
    Modifica uma linha da planilha com base nas informações fornecidas pelo usuário
    """
    planilha = le_dados()
    if planilha == None: return   
    email = valida_email_modifica()
    if email == None: return
    for n,linha in enumerate(planilha):
        if email in linha:
            linha_a_modificar = linha
            indice = n
            break
    opção = "a"
    while opção not in ["1","2","3"]:
        try:    
            opção = input("Os dados do usuário são:\n"
                        f"nome: {linha_a_modificar[0]}\n"
                        f"email: {linha_a_modificar[1]}\n"
                        f"gênero{'s'*bool(len(linha_a_modificar[2].split())>1)}: {limpa_resultado(linha_a_modificar[2])}\n"
                        f"instrumento{'s'*bool(len(linha_a_modificar[3].split())>1)}: {limpa_resultado(linha_a_modificar[3])}\n"
                        "Digite 1 caso deseje modificar os gêneros, 2 para modificar os instrumentos ou 3 para modificar ambos ")
            if opção not in ["1","2","3"]:
                raise Exception("Opção inválida")
        except:
            print("Opção inválida, digite 1, 2 ou 3")    
    planilha[indice] = modifica_linha(linha_a_modificar,opção)
    realiza_cadastro(planilha,False)
    return


def imprime_resultado(lista)->None:
    for indice_banda,linha in enumerate(lista):
        print(f"Banda {indice_banda+1}:")        
        for indice_musico,elemento in enumerate(linha):            
            if indice_musico % 2 == 0:
                integrante = "Músico " + str(indice_musico//2+1)+ " Contato: " + elemento
            else:
                integrante += " Instrumento: " + elemento
                print(integrante)
        print()  
    return 

    
def montar_bandas():
    """
    Imprime uma lista com base em dados fornecidos pelo usuário
    """
    planilha = le_dados()
    if planilha == None: return
    numero_musicos = valida_numero("Digite a quantidade de músicos que deseja buscar ")
    lista_instrumentos = [input(f"Digite o instrumento do {n+1}° músico ").lower() for n in range(numero_musicos)]
    gênero = input("Insira o gênero da banda que deseja montar ")
    musicos_geral = [[[limpa_lista(linha)[1][0],elemento]  for linha in planilha if compara_listas([elemento,gênero],limpa_lista(linha),True)] for elemento in lista_instrumentos] 
    resultado = [[]]
    for n in range(numero_musicos):
        resultado = [x+y for ind,x in enumerate((resultado)) for y in musicos_geral[n] 
        if ((y[0] not in x)and (sorted(x+y) not in [sorted(z+k) for z in resultado[:ind]for k in musicos_geral[n]]))]    
    imprime_resultado(resultado)       
        
    #tinha criado uma função remove_repetidos porque quando eu selecionava 2  instrumentos iguais eram criadas linhas com 
    #os mesmos elementos mas em ordens diferentes, acho que consegui resolver direto na list compreension, mas não sei se ficou mais confuso kkk
    #Antes tinha criado essa função :
    # def remove_repetidos(lista_de_listas:list) -> list:         
    # nova_lista = lista_de_listas.copy()  
    # i=0    
    # while i <  len(nova_lista):        
    #     controle = 0
    #     j=0
    #     while j < len(nova_lista):
    #         if sorted(nova_lista[i]) == sorted(nova_lista[j]): controle+=1
    #         j += 1
    #     if controle >1 : 
    #         nova_lista.remove(nova_lista[i])
    #         continue
    #     i+=1
    # return nova_lista
    # e a list compreension:
    # for n in range(numero_musicos):
    # resultado = [x+y for x in resultado for y in musicos_geral[n] if (y[0] not in x)]


def escolhe_opção() -> str:
    """
    Retorna uma string com base em um dado fornecido pelo usuário
    """
    print("Digite o número que deseja selecionar a opção ")
    print("1. Cadastrar músicos")
    print("2. Buscar músicos")
    print("3. Modificar músicos")
    print("4. Montar bandas")
    print("0. Sair")
    opção = input()
    return opção

# programa principal

opções = ["0","1","2","3","4"]
opção = ""
while opção != "0":
    opção = escolhe_opção()    
    while opção not in opções:
        opção = input("Opção inválida, digite um valor entre 0 e 4 ")
    if opção == "0": continue
    seleção_opção = {
        "1":cadastrar_musicos,
        "2":buscar_musicos,
        "3":modificar_musicos,
        "4":montar_bandas  
    }
    seleção_opção[opção]()
print("Programa encerrado")