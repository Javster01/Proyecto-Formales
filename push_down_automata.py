from stack import Pila
import re
from tkinter import *
#se exporta filedialog de tkinder para poder guardar archivos y abrir archivos de cualquier tipo
from tkinter.filedialog import asksaveasfilename, askopenfilename


#se crea una instancia de tkinder llamada tk y se le pone un titulo
compiler = Tk()
compiler.title('Compilador Ruby/Julia')
#se crea un arreglo de texto vacio para poner el path del archivo a abrir o a guardar
file_path = ''
class AutomataRuby:
    def __init__(self):
        self.estado_actual = 'inicial'
        self.states = 0
        self.analisis = ""
        self.errors = []
        self.symbol_table = {'global': {}}
        self.current_scope = 'global'

    def estados(self, simbolo, stack, count,pos):
        try:
            self.analisis+="q" + str(count) + " Stack:" + str(stack.items)+ "\n"

            if re.search('^print',simbolo) or re.search('^puts ',simbolo):
                print('entra')
                stack.apilar("salida en linea "+str(pos))
                self.states = count+1
                simbolo = simbolo.replace('print','').replace('puts','')
                self.estados(simbolo,stack,self.states,pos)
            elif re.search('^\w+ =', simbolo):
                stack.apilar("variable en linea "+str(pos))
                self.states = count+1
                self.estados(re.sub('^\w+ ','',simbolo),stack,self.states,pos)
            elif re.search('^= .+', simbolo):
                stack.desapilar()
            elif re.search('^(?!println\()\w+\(',simbolo):
                stack.apilar("funcion en linea "+str(pos))
                self.states = count+1
                self.estados(re.sub('^(?!println\()\w+','',simbolo),stack,self.states,pos)
            elif (re.search('^\(.+\)$', simbolo) or re.search('^".+"$', simbolo)or re.search('^ .+$', simbolo)) \
                    and len(stack.items)!=0 and(re.findall(stack.items[len(stack.items)-1],'salida en linea \d+')!=None or re.findall(stack.items[len(stack.items)-1],'funcion en linea \d+')!=None):
                stack.desapilar()
            elif re.search('^if\s+[^;\n]+;?', simbolo):
                stack.apilar("condicional en linea "+str(pos))
            elif re.search('^elsif\s+[^;\n]+;?', simbolo):
                stack.desapilar()
                stack.apilar("condicional  en linea "+str(pos))
            elif re.search('^else\s+[^;\n]+;?', simbolo):
                stack.desapilar()
                stack.apilar("condicional en linea "+str(pos))
            elif re.search('^end', simbolo):
                stack.desapilar()
            elif re.search('^\s*for\s+\w+\s+in\s+.+\s*;?\s*d?o?$', simbolo) :
                stack.apilar("Ciclo en linea "+str(pos))
            elif re.search('^\s*while\s+[^;\n]+;?\s*', simbolo):
                stack.apilar("Ciclo en linea "+str(pos))
            elif re.search('^\s*loop do;?\s*', simbolo):
                stack.apilar("Ciclo en linea "+str(pos))
            elif re.search('^\s*until\s+[^;\n]+ do;?\s*', simbolo):
                stack.apilar("Ciclo en linea "+str(pos))
        except:
            stack.apilar("Error en linea "+str(pos))
            pass


    def analizar(self, codigo):
        pila = Pila()
        count = 0
        countSupport = 0
        for i,simbolo in enumerate(codigo):
            simbolo = re.sub(r'^\s+','',simbolo)
            self.estados(simbolo , pila, self.states,i)

        # Una vez analizado todo el código, verifica si la pila está vacía
        if pila.esta_vacia():
            return self.analisis,pila,"Ruby"
        else:
            return self.analisis, pila,False

    def analyze_ruby_semantics(self, code):
        # Verificar la correcta definición y uso de variables
        variables = re.findall(r'\b(\w+)\s*=\s*(.+?)\b', code)

        # en el caso de que detecte que una variable se intancion mas de una vez en codigo genera el error semantico
        for variable, value in variables:
            if variable in self.symbol_table[self.current_scope]:
                self.errors.append(f"Advertencia: Variable '{variable}' ya definida en el ámbito actual.")
            else:
                self.symbol_table[self.current_scope][variable] = value

        # Verificar llamadas a funciones y sus argumentos
        function_calls = re.findall(r'\b(\w+)\((.*?)\)\b', code)
        # en el caso de que detecte que se hace llamado a una funcion no instanciada genera el error
        for function, arguments in function_calls:
            if function not in self.symbol_table[self.current_scope]:
                self.errors.append(f"Error: Función '{function}' no definida.")
            else:
                # Verificar la correspondencia entre los argumentos de la función y sus parámetros
                expected_parameters = re.findall(r'\bdef\s+%s\((.*?)\)' % function, code)
                # en el caso de que detecte que se hizo envio de variables erroneas a una funcion
                if expected_parameters:
                    expected_parameters = expected_parameters[0].split(',')
                    provided_arguments = arguments.split(',')
                    if len(expected_parameters) != len(provided_arguments):
                        self.errors.append(f"Error: Número incorrecto de argumentos para la función '{function}'.")
    def report_errors(self):
        return "\n".join(self.errors)
    
class AutomataJulia:
    def __init__(self):
        self.estado_actual = 'inicial'
        self.states = 0
        self.analisis = ""
        self.errors = []
        self.current_scope = 'global'
        self.symbol_table = {'global': {}}

    def estados(self, simbolo, stack, count,pos):
        self.analisis+="q" + str(count) + " Stack:" + str(stack.items)+ "\n"
        print(simbolo)
        try:
            if re.search('^println|print',simbolo):
                stack.apilar("salida en linea "+str(pos))
                self.states = count+1
                self.estados(simbolo.replace('println',''),stack,self.states,pos)
            elif re.search('^puts ".+"$', simbolo) or re.search('^gets.chomp+', simbolo) or re.search('^def +', simbolo) or re.search('^loop +', simbolo) or re.search('^until +', simbolo) :
                stack.apilar('Ruby en linea '+str(pos))
            elif re.search('^\w+ =', simbolo):
                stack.apilar("variable en linea "+str(pos))
                self.states = count+1
                self.estados(re.sub('^\w+ ','',simbolo),stack,self.states,pos)
            elif re.search('^= \[?\d+(?:,\s*\d+)*\]$|^= \d+$|^= [A-Za-z]*\((\d|,)*\)$', simbolo):
                stack.desapilar()
            elif re.search('^(?!(println|mean|median|var|std|mode)\()\w+\(',simbolo):
                stack.apilar("funcion en linea "+str(pos))
                self.states = count+1
                self.estados(re.sub('^(?!println\()\w+','',simbolo),stack,self.states,pos)
            elif re.search('^\(.+\)$', simbolo) and len(stack.items)!=0 and(re.findall(stack.items[len(stack.items)-1],'salida en linea \d+')!=None or re.findall(stack.items[len(stack.items)-1],'funcion en linea \d+')!=None):
                stack.desapilar()
            elif re.search('^if\s+[^;\n]+;?', simbolo):
                stack.apilar("condicional en linea "+str(pos))
            elif re.search('^elseif\s+[^;\n]+;?', simbolo):
                stack.desapilar()
                stack.apilar("condicional en linea "+str(pos))
            elif re.search('^else\s+[^;\n]+;?', simbolo):
                stack.desapilar()
                stack.apilar("condicional en linea "+str(pos))
            elif re.search('^end', simbolo):
                stack.desapilar()
            elif re.search('^for\s+\w+\s+in\s+[^;\n]+;?\s*$', simbolo):
                stack.apilar("Ciclo en linea "+str(pos))
            elif re.search('^\s*while\s+[^;\n]+;?\s*', simbolo):
                stack.apilar("Ciclo en linea "+str(pos))
            elif re.search('^(mean|median|var|std|mode)\(',simbolo):
                stack.apilar("estadistica en linea "+str(pos))
                self.estados(re.sub('^(mean|median|var|std|mode)','',simbolo),stack,self.states,pos)
            elif re.search('^\(([A-Za-z]|\[([0-9]*(\.|,|;)*)*\])(,\s*dims\s*=\s*(\(\s*\d+,\s*\d+\)|\d*))?\)$', simbolo) and len(stack.items)!=0 and(re.findall(stack.items[len(stack.items)-1],'estadistica en linea \d+')!=None):
                stack.desapilar()

        except:
            stack.apilar("Error en linea "+str(pos))
            pass

    def analizar(self, codigo):
        pila = Pila()
        count = 0
        countSupport = 0
        for i,simbolo in enumerate(codigo):
            simbolo = re.sub(r'^\s+','',simbolo)
            self.estados(simbolo , pila, self.states,i)

        # Una vez analizado todo el código, verifica si la pila está vacía
        if pila.esta_vacia():
            return self.analisis,pila,"Julia"
        else:
            return self.analisis, pila,False


    def analyze_julia_semantics(self, code):
        # Verificar la correcta definición y uso de variables en Julia
        variables = re.findall(r'\b(\w+)\s*=\s*(.+?)\b', code)
        for variable, value in variables:
            if variable in self.symbol_table[self.current_scope]:
                self.errors.append(f"Advertencia: Variable '{variable}' ya definida en el ámbito actual.")
            else:
                self.symbol_table[self.current_scope][variable] = value

        # Verificar llamadas a funciones y sus argumentos en Julia
        function_calls = re.findall(r'\b(\w+)\((.*?)\)\b', code)
        for function, arguments in function_calls:
            if function not in self.symbol_table[self.current_scope]:
                self.errors.append(f"Error: Función '{function}' no definida.")
            else:
                # Verificar la correspondencia entre los argumentos de la función y sus parámetros
                expected_parameters = re.findall(r'\bfunction\s+%s\((.*?)\)' % function, code)
                if expected_parameters:
                    expected_parameters = expected_parameters[0].split(',')
                    provided_arguments = arguments.split(',')
                    if len(expected_parameters) != len(provided_arguments):
                        self.errors.append(f"Error: Número incorrecto de argumentos para la función '{function}'.")
    def report_errors(self):
        return "\n".join(self.errors)


def open_file():
    # guarda en path la ubicacion del archivo con el askopenfilename, en este caso solo busca archivoz .jl y .rb
    path = askopenfilename(filetypes=[('Julia/Ruby Files', '*.jl .rb')])
    with open(path, 'r') as file:
        # con el archivo detectado, hace el read para mandar el codigo a memoriam, lo pone en el espacio de texto de code_output y
        # llama la funcion detected_language para verificar el lenguaje
        code = file.read()
        code_output.delete("1.0", END)
        detected_language = detect_language(code)

        
        # AQUI SE PONE EL OUTPUT DEL ANALISIS EN ESTE CASO EL TIPO DE LENGUAJE



        # AQUI SE PONE EL CODIGO EN EL ESPACIO DE TEXTO DE ARRIBA
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)
        codigo_julia = code

        if(len(codigo_julia)>500):
                code_output.insert("1.0","El codigo supera los 500 caracteres teniendo "+str(len(codigo_julia)))
                return
        if(len(codigo_julia)<50):
                code_output.insert("1.0","El codigo es inferior a 50 caracteres teniendo "+str(len(codigo_julia)))
                return
        
        print("La cadena es de tamaño: ", len(codigo_julia))
        automata = AutomataJulia()
        codigo = re.split('\n|\r|\b" "', codigo_julia)
        code_output.insert("1.0", "El total de caracteres de la cadena es de: " + str(len(codigo_julia)) + "\n")
        analisis, pila, result = automata.analizar(codigo)
        matches = [item for item in pila.items if re.search('Ruby en linea \d+', item)]
        if result != False:
            code_output.insert("1.0", "Código de Julia\n")
            code_output.insert("1.0", analisis)
            automata.analyze_julia_semantics(codigo_julia)
            errors = automata.report_errors()
            code_output.insert("1.0", errors)
        elif matches:
            print('entraruby')
            automataRuby = AutomataRuby()
            analisis, pila, result = automataRuby.analizar(codigo)
            automataRuby.analyze_ruby_semantics(codigo_julia)

            if result != False:
                code_output.insert("1.0", "Código de ruby\n")
                code_output.insert("1.0", analisis)
                errors = automataRuby.report_errors()
                code_output.insert("1.0", errors)
                print(errors)
            else:
                code_output.insert("1.0", "Código de ruby con problemas en la estructura\n")
                code_output.insert("1.0", analisis)
                code_output.insert("1.0", "problemas con: " + str(pila.items) + " En el codigo\n")
                errors = automataRuby.report_errors()
                code_output.insert("1.0", errors)

        else:
            code_output.insert("1.0", "Código de Julia pero con errores de estructura\n")
            code_output.insert("1.0", analisis)
            code_output.insert("1.0", "problemas con: " + str(pila.items) + " En el codigo\n")
            errors = automata.report_errors()
            code_output.insert("1.0", errors)




def detect_language(content):
    #se ponen los lenguajes julia y ruby con sus expresiones regulares usadas para cada lenguajes

    patterns = {
        'julia': r'\b(julia|function|using|global|let|struct|importall|println)\b',
        'ruby': r'\b(ruby|require|puts|def|alias|class|elsif|module)\b'
    }

    detected_language = None
    #se hace un for para analizar si alguna expresion regular corresponde a las presentes en patterns para decir que lenguaje es
    for language, pattern in patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            detected_language = language
            break


    #retorna el lenguaje detectado
    return detected_language

def set_file_path(path):
    global file_path
    file_path = path

# Ejemplo de uso
if __name__ == "__main__":

    menu_bar = Menu(compiler)

    # se agrega el menu desplegable a tkinder
    file_menu = Menu(menu_bar, tearoff=0)
    # se agregan al menu desplegable los comando de open, save, save as, exit
    file_menu.add_command(label='Open', command=open_file)
    file_menu.add_command(label='Exit', command=exit)
    

    # se pone despligue de tipo cascada con todos los items de file_menu y se añade a menu bar
    menu_bar.add_cascade(label='File', menu=file_menu)

    # COMANDO NO NECESARIO, PROGRAMA NO REQUIERE EL RUN

    # run_bar = Menu(menu_bar, tearoff=0)
    # menu_bar.add_cascade(label='Run', menu=run_bar)

    compiler.config(menu=menu_bar)

    # se agrega un espacio de texto para el codigo y se empaqueta con el resto de la interfaz tkinder
    editor = Text()
    editor.pack()

    # se agrega un espacio de texto para el output del codigo que contendra analisis de lenguaje, semantico y sintactico
    code_output = Text(height=10)
    code_output.pack()

    compiler.mainloop()
