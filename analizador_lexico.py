import ply.lex as lex

# resultado del analisis
resultado_lexema = []

reservada = (
    # Palabras Reservadas
    'MOSTRAR',  #imprimir en pantalla
    'FOR',      #repetir una accion varias veces
    'CONCAT',   #concatenar dos cadenas
    'CADENA',   #cadena de texto
    
)
tokens = reservada + (
    'IDENTIFICADOR',    #identificador (nombre de variable, nombre de funcion, etc)
    'ENTERO',        #numero decimal (1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0)
    'ASIGNAR',          #asignacion de valor a=5
    'SUMA',             #suma 25+30=55
    'RESTA',            #resta 25-5=20
    'MULT',             #multiplicacion 5*5=25
    'DIV',              #division 10/2 = 5
    'POTENCIA',         #potencia 6**2 = 6^2 = 6*6 = 36
    'MODULO',           #modulo 10%2 = 0
    'PARIZQ',            #simbolo (
    'PARDER',            #simbolo )
    'CORIZQ',            #simbolo [
    'CORDER',            #simbolo ]
    'LLAIZQ',            #simbolo {
    'LLADER',            #simbolo }
    'COMDOB'             #simbolo "
)

# Reglas de Expresiones Regualres para token de Contexto simple
t_SUMA          = r'\+'
t_RESTA         = r'-'
t_COMDOB        = r'\"'
t_MULT          = r'\*'
t_DIV           = r'/'
t_MODULO        = r'\%'
t_POTENCIA      = r'(\*{2} | \^)'
t_ASIGNAR       = r'='
t_PARIZQ        = r'\('
t_PARDER        = r'\)'
t_CORIZQ        = r'\['
t_CORDER        = r'\]'
t_LLAIZQ        = r'{'
t_LLADER        = r'}'

def t_FOR(t):
    r'for'
    return t

def t_MOSTRAR(t):
    r'mostrar'
    return t

def t_CONCAT(t):
    r'concat'
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFICADOR(t):  # identificador (nombre de todas las palabras reservadas y simbolos)
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_CADENA(t): #expresion regular par identificar una cadena de texto entre " "
    r'\"?(\w+ \ *\w*\d* \ *)\"?'
    return t

def t_newline(t): #expresion regular para identificar un salto de linea
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comments(t): #expresion regular para identificar un comentario de varias lineas /* */
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    print("Comentario de multiple linea")

def t_comments_ONELine(t): #expresion regular para identificar un comentario de una linea //
    r'\/\/(.)*\n'
    t.lexer.lineno += 1
    print("Comentario de una linea")
t_ignore =' \t'

def t_error( t): #manejo de errores
    global resultado_lexema
    estado = "** Token no valido en la Linea {:4} Valor {:16} Posicion {:4}".format(str(t.lineno), str(t.value),
                                                        str(t.lexpos))
    resultado_lexema.append(estado)
    t.lexer.skip(1)

# Prueba de ingreso
def prueba(data):
    global resultado_lexema

    analizador = lex.lex()
    analizador.input(data)

    resultado_lexema.clear()
    while True:
        tok = analizador.token()
        if not tok:
            break
        # print("lexema de "+tok.type+" valor "+tok.value+" linea "tok.lineno)
        estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno),str(tok.type) ,str(tok.value), str(tok.lexpos) )
        resultado_lexema.append(estado)
    return resultado_lexema

# instanciamos el analizador lexico
analizador = lex.lex()

'''if __name__ == '__main__': #prueba de ingreso para probar el analizador lexico elimine las comillas
    while True:
        data = input("ingrese: ")
        prueba(data)
        print(resultado_lexema)'''
        