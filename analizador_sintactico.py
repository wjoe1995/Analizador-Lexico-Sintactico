import ply.yacc as yacc
from analizador_lexico import tokens
from analizador_lexico import analizador

# resultado del analisis
resultado_gramatica = []

precedence = (
    ('right','ASIGNAR'), #forma por donde se evalua la expresion eje: a = b + c
    ('left', 'SUMA', 'RESTA'), #forma por donde se evalua la expresion eje: a + b
    ('left', 'MULT', 'DIV'),
    ('right', 'MOSTRAR',),
    ('left', 'FOR', 'CONCAT',),
)
nombres = {}

def p_declaracion_mosrar(t):
    '''
    declaracion     :    MOSTRAR  PARIZQ expresion PARDER 
                    |    MOSTRAR  PARIZQ CADENA PARDER 
    ''' #ejm: mostrar(a)
        #ejm: mostrar("hola")
    t[0] = print(t[3])
    

def p_expresion_for(t):
    'expresion : ENTERO  FOR  CADENA'
    #ejm: 4 for "hola"
    t[0] = t[1]
    for i in range(t[1]):
        print(t[3])

def p_expresion_concat(t):
    '''
    expresion   :  expresion  CONCAT  expresion 
                |  expresion  CONCAT  CADENA
                |  CADENA  CONCAT  expresion
                |  CADENA  CONCAT  CADENA
    ''' 
    # a= "hola" b= "como"
    #ejm: a + b
    #ejm: a + "como estas"
    #ejm: "hola" + b
    #ejm: "hola" + "como estas"
    if len(t) == 4:
        t[0] = t[1] + t[3]
    elif len(t) == 3:
        t[0] = t[1] + t[2]
    elif len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = t[2]
        
def p_declaracion_asignar(t):
    '''
    declaracion :  IDENTIFICADOR ASIGNAR expresion  
                |  IDENTIFICADOR ASIGNAR CADENA 
    '''
    #ejm: a = 4
    #ejm: a = "hola como estas me gustaria"    
    if len(t) == 4:
        nombres[t[1]] = t[3]
    else:
        nombres[t[1]] = t[5]
    
def p_declaracion_expre(t):
    '''
    declaracion : expresion
                | CADENA
    ''' 
    #ejm: 4,a,b
    #ejm: "hola"
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
    #ejm: 4 + 5
    #ejm: 4 - 5
    #ejm: 4 * 5
    #ejm: 4 / 5
    #ejm: 4 ** 5
    #ejm: 4 % 5
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
    #ejm: (4)
    #ejm: [4]
    #ejm: {4}
    t[0] = t[2]

def p_expresion_numero(t):
    '''
    expresion : ENTERO 
    '''
    #ejm: 4
    t[0] = t[1]

def p_expresion_cadena(t):
    '''
    expresion   : COMDOB CADENA COMDOB
    '''  
    #ejm: "hola"
    t[0] = t[2]

def p_expresion_nombre(t):
    '''
    expresion : IDENTIFICADOR
    ''' 
    #ejm: a,b,c
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