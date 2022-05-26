from itertools import islice
from typing import Any
from copy import deepcopy


# função para pegar cada row de um txt e tranformar em matriz
def transformMatrixToFloat(fileName: str) -> list[list[float]]:
    matrix = []

    # coloca cada row do arquivo a partir da 2 linha como uma row na matrix
    with open(fileName) as file:
        for row in islice(file, 1, None):  # cria um loop pulando a primeira linha do arquivo
            matrix.append([float(item) for item in row.strip().split(" ")])

    return matrix  # retorna a matriz somente com números reais


""" Aqui começa as funções para verificar se a matrix é valida """


# função pra validar se a divisão entre rows resulta em alguma igualdade
def lookForEqualElements(matrix: list[list[float]]) -> bool:
    divisionList = []

    for numeratorLine in range(len(matrix) - 1):  # pega uma linha para ser o numerador
        denominatorLine = numeratorLine + 1  # a linha do denominador é a do numerador + 1
        # cria um loop que vai da linha do numerador até o final da matrix
        for row in range(numeratorLine, len(matrix) - 1):
            divisionList.clear()
            for column in range(len(matrix[0]) - 1):  # percorre cada coluna na linha
                try:
                    divisionList.append(round(matrix[numeratorLine][column] / matrix[denominatorLine][column], 2))
                except ZeroDivisionError:  # se tentar dividir por zero
                    divisionList.append(0)
            # retorna True se todos elementos na linha forem iguais
            if all(value == divisionList[0] for value in divisionList):
                return True
            else:
                denominatorLine += 1

    return False


# função para verificar se a matrix é quadrada
def isSquareMatrix(matrix: list[list[float]]) -> bool:
    rows = 0
    columns = 0

    for row in range(len(matrix)):
        rows += 1
        for columns in range(len(matrix[0]) - 1):
            columns += 1

    # retorna True se linha for igual a coluna ou False se não for
    return bool(rows == columns)


""" Aqui terminam as funções para verificar se a matrix é valida """


# checa se existem zeros na diagonal principal
def zeroCheck(matrix: list[list[float]], ordR, ordC) -> int:
    amountOfZeros = 0
    posicao = 0
    while posicao < len(matrix):
        if matrix[ordR[posicao]][ordC[posicao]] == 0:
            amountOfZeros += 1
        posicao += 1
    return amountOfZeros > 0


# coloca o número 1 na diagonal principal na linha recebida como parâmetro
def getRidOfZeros(matrix: list[list[float]]) -> list[Any] | None:
    perms = permutations(list(range(len(matrix))))

    for row in range(len(perms)):
        for column in range(len(perms)):
            if not zeroCheck(matrix, perms[row], perms[column]):
                return [perms[row], perms[column]]

    return None


# função que gera todas as permutações possíveis entre as linhas
def permuta(row: list, perm: list, perms: list):
    if row == []:
        perms.append(perm)
    else:
        for lin in range(len(row)):
            permuta(row[0:lin] + row[lin + 1:len(row)], perm + [row[lin]], perms)


# recebe uma lista com os valores a serem permutados (as linhas)
def permutations(row: list) -> list:
    perms = []
    permuta(row, [], perms)

    return perms


# função para trocar as rows, caso não haja 0, retorna a matriz com as rows trocadas
# row, row2  são as linhas a serem trocadas
def rowSwap(matrix: list[list[float]], row: int, row2: int) -> list[list[float]]:
    for i in range(len(matrix)):
        temp = matrix[row]
        matrix[row] = matrix[row2]
        matrix[row2] = temp

        return matrix


# função para trocar as columnas, caso não haja 0, retorna a matriz com as columns trocadas
# col, col2  são as colunas a serem trocadas
def columnSwap(matrix: list[list[float]], col: int, col2: int) -> list[list[float]]:
    for row in range(len(matrix)):
        m = deepcopy(matrix[row])
        matrix[row][col] = m[col2]
        matrix[row][col2] = m[col]

    return matrix


def setOneAtGivenRow(row: int, matrix: list[list[float]]):
    divisor = matrix[row][row]

    for column in range(len(matrix[row])):
        try:
            matrix[row][column] /= divisor
        except ZeroDivisionError:
            pass
    # após deixar 1 na diagonal principal, chama uma função para colocar 0 na coluna da diagonal principal
    return setZeroBelowRow(row, matrix)


# row = linha da diagonal principal que foi setado 1, m= matriz
def setZeroBelowRow(row: int, matrix: list[list[float]]):
    col = row
    # Is it the last row
    if row == len(matrix) - 1:
        return matrix

    for line in range(row + 1, len(matrix)):
        # deixa o número da linha desejada ser o inverso dele para multiplicar pela linha da diag pric
        negativeScalar = -1 * matrix[line][col]
        # multiplica a linha que está sendo usadada pelo valor negativo do item de baixo
        tempTopRow = [itens * negativeScalar for itens in matrix[row]]
        for column in range(len(matrix[line])):
            matrix[line][column] = float(tempTopRow[column] + matrix[line][column])
    return matrix


# row = linha da diagonal principal que foi setado 1, m= matriz
def setZeroAboveRow(row: int, matrix: list[list[float]]):
    col = row
    # Is it the last row
    if row == 0:
        return matrix

    for line in range(0, row):
        # deixa o número da linha desejada ser o inverso dele para multiplicar pela linha da diag pric
        negativeScalar = -1 * matrix[line][col]
        # multiplica a linha que está sendo usadada pelo valor negativo do item de baixo
        tempTopRow = [itens * negativeScalar for itens in matrix[row]]
        for column in range(len(matrix[line])):
            matrix[line][column] = float(tempTopRow[column] + matrix[line][column])

    return matrix


def printFinalResult(matrix: list[list[float]]):
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if column < len(matrix[row]) - 1:
                print("\33[32m\33[4m" + str(int(matrix[row][column])), end=" | ")
            else:
                print(str(round(matrix[row][column], 3)), end=" ")
        print()

    print()
    for items in range(len(matrix)):
        print("O ", str(items + 1) + "º valor é: ", round(matrix[items][-1], 3))
    print()


while True:
    try:
        fileName = input("\33[33mInsira o nome do arquivo que contém o sistema linear: ")
        matrix = transformMatrixToFloat(fileName)

        if not lookForEqualElements(matrix) and isSquareMatrix(matrix) and matrix != []:
            hasZero = getRidOfZeros(matrix)

            if hasZero is None:
                print("\33[31mPoxa vida! Não conseguimos nos livrar dos 0 na diagonal principal :( ")
                print("Tente com outro sistema linear!")
                break
            else:
                print("Ah que beleza! A matriz pode ser resolvida \n")

            while hasZero[1] != [*range(len(matrix[0]) - 1)]:
                for position in range(len(hasZero[1]) - 1):
                    hasZero = getRidOfZeros(rowSwap(matrix, hasZero[1][position], hasZero[1][position + 1]))
                break
            while hasZero[0] != [*range(len(matrix[0]) - 1)]:
                for position in range(len(hasZero[1]) - 1):
                    hasZero = getRidOfZeros(columnSwap(matrix, hasZero[1][position], hasZero[1][position + 1]))
                break

            for row in range(len(matrix)):
                matrix = setOneAtGivenRow(row, matrix)
            for row in range(len(matrix) - 1, 0, -1):
                setZeroAboveRow(row, matrix)

            printFinalResult(matrix)

            print("\33[33mFim do programa!")
            break
        else:
            print("\33[31mPoxa vida! A matriz não pode ser resolvida, pois ela não é válida na resolução de Gauss \n")
    except FileNotFoundError:
        print("\33[31mOps! O arquivo não existe \n")
    except ValueError:
        print(
            "\33[31mOps! O arquivo deve conter um sistema que forma uma matriz quadrada apenas com números naturais \n")
