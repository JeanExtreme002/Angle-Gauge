import math

def getHypotenuse(b,c):
    """
    Retorna a hipotenusa de um triângulo retângulo 
    utilizando os seus catetos.

    Fórmula: a² = b² + c²
    """
    return ((b**2) + (c**2)) ** 0.5


def cos2degrees(x):
    """
    Retorna o cosseno em graus.
    """
    return math.degrees(math.acos(x))
