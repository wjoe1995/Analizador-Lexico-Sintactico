import ply.yacc as yacc
from analizador_lexico import tokens
from analizador_lexico import analizador

# resultado del analisis
resultado_gramatica = []

precedence = (
    ('right','ASIGNAR'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    ('right', 'CONCAT', 'MOSTRAR',),
    ('left', 'FOR',),
)
nombres = {}

def p_declaracion_mosrar(t):
    '''
    declaracion     :    MOSTRAR PARIZQ expresion PARDER
                    |    MOSTRAR  PARIZQ CADENA PARDER
    '''
    t[0] = print(t[3])

def p_expresion_for(t):
    'expresion : ENTERO  FOR  CADENA'
    t[0] = t[1]
    for i in range(t[1]):
        print(t[3])

def p_declaracion_concat(t):
    'declaracion : CADENA CONCAT CADENA'
    t[0] = t[1] + t[3]
    

def p_declaracion_asignar(t):
    '''
    declaracion :  IDENTIFICADOR ASIGNAR expresion
                |  IDENTIFICADOR ASIGNAR CADENA
    '''
    if len(t) == 4:
        nombres[t[1]] = t[3]
    else:
        nombres[t[1]] = t[5]

def p_declaracion_expre(t):
    'declaracion : expresion'
    # print("Resultado: " + str(t[1]))
    t[0] = t[1]

def p_expresion_operaciones(t):
    '''
    expresion  :    expresion SUMA expresion
                |   expresion RESTA expresion
                |   expresion MULT expresion
                |   expresion DIV expresion
                |   expresion POTENCIA expresion
                |   expresion MODULO expresion
    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]
    elif t[2] == '%':
        t[0] = t[1] % t[3]
    elif t[2] == '**':
        i = t[3]
        t[0] = t[1]
        while i > 1:
            t[0] *= t[1]
            i -= 1

def p_expresion_grupo(t):
    '''
    expresion  :  PARIZQ expresion PARDER
                | LLAIZQ expresion LLADER
                | CORIZQ expresion CORDER
    '''
    t[0] = t[2]

def p_expresion_numero(t):
    '''
    expresion : ENTERO
    '''
    t[0] = t[1]

def p_declaracion_cadena(t):
    'declaracion : COMDOB expresion COMDOB'
    t[0] = t[2]

def p_expresion_nombre(t):
    'expresion : IDENTIFICADOR'
    try:
        t[0] = nombres[t[1]]
    except LookupError:
        print("Nombre desconocido ", t[1])
        t[0] = 0

def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintactico de tipo {} en el valor {}".format( str(t.type),str(t.value))
        print(resultado)
    else:
        resultado = "Error sintactico {}".format(t)
        print(resultado)
    resultado_gramatica.append(resultado)

# instanciamos el analizador sistactico
parser = yacc.yacc()

def prueba_sintactica(data):
    global resultado_gramatica
    resultado_gramatica.clear()
    for item in data.splitlines():
        if item:
            gram = parser.parse(item)
            if gram:
                resultado_gramatica.append(str(gram))
        else: print("data vacia")
    print("result: ", resultado_gramatica)
    return resultado_gramatica

if __name__ == '__main__':
    while True:
        try:
            s = input(' ingresa dato >>: ')
        except EOFError:
            continue
        if not s: continue
        #gram = parser.parse(s)
        #print("Resultado ", gram)
        prueba_sintactica(s)