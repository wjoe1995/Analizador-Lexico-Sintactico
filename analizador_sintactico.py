import ply.yacc as yacc
from analizador_lexico import tokens
from analizador_lexico import analizador

# resultado del analisis
resultado_gramatica = []

precedence = (
    ('right','ASIGNAR'), #forma por donde se evalua la expresion eje: a = b + c
    ('left', 'SUMA', 'RESTA'), #forma por donde se evalua la expresion eje: a + b
    ('left', 'MULT', 'DIV'),
    ('right', 'CONCAT', 'MOSTRAR',),
    ('left', 'FOR',),
)
nombres = {}

def p_declaracion_mosrar(t):
    '''
    declaracion     :    MOSTRAR PARIZQ expresion PARDER #ejm: mostrar(a)
                    |    MOSTRAR  PARIZQ CADENA PARDER   #ejm: mostrar("hola")
    '''
    t[0] = print(t[3])

def p_expresion_for(t):
    'expresion : ENTERO  FOR  CADENA' #ejm: 4 for "hola"
    t[0] = t[1]
    for i in range(t[1]):
        print(t[3])

def p_declaracion_concat(t):
    '''
    declaracion : CADENA CONCAT CADENA CONCAT CADENA CONCAT CADENA CONCAT CADENA
    ''' #ejm: "hola" concat "mundo" concat "!" concat "como" concat "estas"
    t[0] = t[1] + t[3] + t[5] + t[7] + t[9]  
    
def p_declaracion_asignar(t):
    '''
    declaracion :  IDENTIFICADOR ASIGNAR expresion  #ejm: a = 4
                |  IDENTIFICADOR ASIGNAR CADENA     #ejm: a = "hola"
    '''
    if len(t) == 4:
        nombres[t[1]] = t[3]
    else:
        nombres[t[1]] = t[5]

def p_declaracion_expre(t):
    'declaracion : expresion' #ejm: 4,a,b
    t[0] = t[1]

def p_expresion_operaciones(t):
    '''
    expresion  :    expresion SUMA expresion        #ejm: 4 + 5
                |   expresion RESTA expresion       #ejm: 4 - 5
                |   expresion MULT expresion        #ejm: 4 * 5
                |   expresion DIV expresion         #ejm: 4 / 5
                |   expresion POTENCIA expresion    #ejm: 4 ** 5
                |   expresion MODULO expresion      #ejm: 4 % 5
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
    expresion  :  PARIZQ expresion PARDER   #ejm: (4)
                | LLAIZQ expresion LLADER   #ejm: [4]
                | CORIZQ expresion CORDER   #ejm: {4}
    '''
    t[0] = t[2]

def p_expresion_numero(t):
    '''
    expresion : ENTERO #ejm: 4
    '''
    t[0] = t[1]

def p_declaracion_cadena(t):
    'declaracion : COMDOB expresion COMDOB' #ejm: "hola"
    t[0] = t[2]

def p_expresion_nombre(t):
    'expresion : IDENTIFICADOR' #ejm: a,b,c
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