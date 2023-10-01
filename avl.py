class Nodo:
    def __init__(self, chave, esquerda, direita, fb):
        self.chave = chave
        self.esquerda = esquerda
        self.direita = direita
        self.fb = fb

def altura(nodo):
    if nodo is None:
        return 0
    else:
        alt_esq = altura(nodo.esquerda)
        alt_dir = altura(nodo.direita)
        if (alt_esq > alt_dir):
            return(1 + alt_esq)
        else:
            return(1 + alt_dir)

def calcular_fb(nodo):
    return (altura(nodo.esquerda) - altura(nodo.direita))

def is_avl(nodo):
    if nodo is None:
        return True
    alt_esq = altura(nodo.esquerda)
    alt_dir = altura(nodo.direita)
    return ((alt_esq - alt_dir < 2) and
            (alt_dir - alt_esq < 2) and
            (is_avl(nodo.esquerda)) and
            (is_avl(nodo.direita)))

def rotacao_simples_direita(nodo):
    x = nodo.esquerda
    nodo.esquerda = x.direita
    x.direita = nodo
    nodo.fb = 0
    nodo = x
    return nodo

def rotacao_simples_esquerda(nodo):
    x = nodo.direita
    nodo.direita = x.esquerda
    x.esquerda = nodo
    nodo.fb = 0
    nodo = x
    return nodo

def rotacao_dupla_direita(nodo):
    x = nodo.esquerda
    y = x.direita
    x.direita = y.esquerda
    y.esquerda = x
    nodo.esquerda = y.direita
    y.direita = nodo

    if y.fb == 1:
        nodo.fb = -1
    else:
        nodo.fb = 0

    if y.fb == -1:
        x.fb = 1
    else:
        x.fb = 0
    
    nodo = y
    return nodo

def rotacao_dupla_esquerda(nodo):
    x = nodo.direita
    y = x.esquerda
    x.esqueda = y.direita
    y.direita = x
    nodo.direita = y.esquerda
    y.esquerda = nodo

    if y.fb == -1:
        nodo.fb = 1
    else:
        nodo.fb = 0

    if y.fb == 1:
        x.fb = -1
    else:
        x.fb = 0
    
    nodo = y
    return nodo

def rotacionar_direita(nodo, inseriu):
    x = nodo.esquerda
    if x.fb == 1:
        print(f"Fazendo rotação simples à direita em {nodo.chave}")
        nodo = rotacao_simples_direita(nodo)
    else:
        print(f"Fazendo rotação dupla à direita em {nodo.chave}")
        nodo = rotacao_dupla_direita(nodo)

    nodo.fb = 0
    inseriu = False
    return nodo, inseriu

def rotacionar_esquerda(nodo, inseriu):
    x = nodo.direita
    if x.fb == -1:
        print(f"Fazendo rotação simples à esquerda em {nodo.chave}")
        nodo = rotacao_simples_esquerda(nodo)
    else:
        print(f"Fazendo rotação dupla à esquerda em {nodo.chave}")
        nodo = rotacao_dupla_esquerda(nodo)
    
    nodo.fb = 0
    inseriu = False
    return nodo, inseriu

def inserir(nodo, chave, inseriu = False):
    if nodo is None:
        nodo = Nodo(chave, None, None, 0)
        inseriu = True
        return nodo, inseriu
    elif nodo.chave > chave:
        nodo.esquerda, inseriu = inserir(nodo.esquerda, chave, inseriu)
        if inseriu:
            if nodo.fb == -1:
                nodo.fb = 0
                inseriu = False
            elif nodo.fb == 0:
                nodo.fb = 1
            elif nodo.fb == 1:
                nodo, inseriu = rotacionar_direita(nodo, inseriu)
    elif nodo.chave < chave:
        nodo.direita, inseriu = inserir(nodo.direita, chave, inseriu)
        if inseriu:
            if nodo.fb == 1:
                nodo.fb = 0
                inseriu = False
            elif nodo.fb == 0:
                nodo.fb = -1
            elif nodo.fb == -1:
                nodo, inseriu = rotacionar_esquerda(nodo, inseriu)

    return nodo, inseriu

def buscar(nodo, chave):
    if nodo is None:
        return None
    elif nodo.chave == chave:
        return nodo
    elif nodo.chave > chave:
        return buscar(nodo.esquerda, chave)
    elif nodo.chave < chave:
        return buscar(nodo.direita, chave)

def minimo(nodo):
    if nodo.esquerda is None:
        return nodo
    else:
        return minimo(nodo.esquerda)
    
def maximo(nodo):
    if nodo.direita is None:
        return nodo
    else:
        return maximo(nodo.direita)

def remover(nodo, chave):
    if nodo is None:
        return False
    
    if chave < nodo.chave:
        nodo.esquerda = remover(nodo.esquerda, chave)

    elif chave > nodo.chave:
        nodo.direita = remover(nodo.direita, chave)

    else:
        if nodo.esquerda is None:
            return nodo.direita
        elif nodo.direita is None:
            return nodo.esquerda
        substituto = minimo(nodo.direita)
        nodo.chave = substituto.chave
        nodo.direita = remover(nodo.direita, substituto.chave)

    nodo.fb = calcular_fb(nodo)
    if nodo.fb > 1:
        if calcular_fb(nodo.esquerda) >= 0:
            return rotacao_simples_direita(nodo)
        else:
            return rotacao_dupla_direita(nodo)
    elif nodo.fb < -1:
        if calcular_fb(nodo.direita) <= 0:
            return rotacao_simples_esquerda(nodo)
        else:
            return rotacao_dupla_esquerda(nodo)

    return nodo
 
def listar(nodo):
    if nodo is None:
        print('Vazio')
    else:
        mostrar(nodo)
        if nodo.esquerda is not None:
            listar(nodo.esquerda)
        if nodo.direita is not None:
            listar(nodo.direita)

def mostrar(nodo):
    if nodo is None:
        print('[Vazio,0]')
    else:
        print(f'[{nodo.chave}]')

def input_number(msg):
    valor = input(msg)
    try:
        inteiro = int(valor)
        return inteiro
    except:
        print("Deve ser um número!")
        input_number(msg)
    return inteiro

def mostrar_arvore(nodo, nivel=0, prefixo="Raiz: "):
    if nodo is not None:
        print(" " * (nivel * 4) + prefixo + str(nodo.chave))
        mostrar_arvore(nodo.esquerda, nivel + 1, "ESQ: ")
        mostrar_arvore(nodo.direita, nivel + 1, "DIR: ")

def main():
    rodando = True
    nodo = None
    while rodando:
        print("1 - Inserir")
        print("2 - Buscar")
        print("3 - Listar")
        print("4 - Remover")
        print("5 - Mínimo")
        print("6 - Máximo")
        print("7 - Mostrar Árvore")
        print("8 - Inserir Sequência de Valores")
        print("9 - Remover Sequência de Valores")
        print("10 - Verificar AVL")
        print("11 - Sair")
        opcao = input_number("Escolha uma opção: ")

        
        opcao = int(opcao)
        if opcao == 1:
            resultado = inserir(nodo, input_number("Insira o valor: "))
            if resultado is False:
                print("Valor já inserido!")
            elif resultado is True:
                print("Valor inserido com sucesso!")
        elif opcao == 2:
            resultado = buscar(nodo, input_number("Insira o valor: "))
            if resultado is None:
                print("Valor não encontrado!")
            else:
                mostrar(resultado)
        elif opcao == 3:
            listar(nodo)
        elif opcao == 4:
            resultado = remover(nodo, input_number("Insira o valor: "))
            if resultado is False:
                print("Valor não encontrado!")
            else:
                nodo = resultado
        elif opcao == 5:
            resultado = minimo(nodo)
            if resultado is None:
                print("Mínimo não encontrado!")
            else:
                mostrar(resultado)
        elif opcao == 6:
            resultado = maximo(nodo)
            if resultado is None:
                print("Máximo não encontrado!")
            else:
                mostrar(resultado)
        elif opcao == 7:
            mostrar_arvore(nodo)
        elif opcao == 8:
            qtd_valores = input_number("Insira a quantidade de valores que deseja inserir: ")
            valores = []
            inseriu = False
            for i in range(qtd_valores):
                valores.append(input_number("Insira o valor: "))
            for valor in valores:
                nodo, inseriu = inserir(nodo, valor)
                if inseriu is False:
                    print(f"{valor} já foi inserido!")
        elif opcao == 9:
            qtd_valores = input_number("Insira a quantidade de valores que deseja remover: ")
            valores = []
            removeu = False
            for i in range(qtd_valores):
                valores.append(input_number("Insira o valor: "))
            for valor in valores:
                nodo = remover(nodo, valor)
                if nodo is False:
                    print(f"{valor} não encontrado!")
        elif opcao == 10:   
            if is_avl(nodo):
                print("Árvore é AVL!")
            else:
                print("Árvore não é AVL")
        elif opcao == 11:
            rodando = False
        else:
            print("Opção inválida!")
       

main()