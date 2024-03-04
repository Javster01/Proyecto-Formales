
#Se exporta tkinder para usar la interfaz grafica
from tkinter import *
#se exporta filedialog de tkinder para poder guardar archivos y abrir archivos de cualquier tipo
from tkinter.filedialog import asksaveasfilename, askopenfilename
#se importa re para poder hacer uso de expresiones regulares
import re


#se crea una instancia de tkinder llamada tk y se le pone un titulo
compiler = Tk()
compiler.title('Compilador Ruby/Julia')
#se crea un arreglo de texto vacio para poner el path del archivo a abrir o a guardar
file_path = ''


#funcion se encarga de guardar el path en una variable global

def set_file_path(path):
    global file_path
    file_path = path


#se encarga del analisis semantico del codigo 
class SemanticsAnalyzer:
    def __init__(self):
        self.symbol_table = {'global': {}}
        self.current_scope = 'global'
        self.errors = []  # Lista para almacenar mensajes de error semántico

    #se encarga de escoger uno de los 2 analizadores semanticos, le llega su propia intancia, el codigo y el tipo de lenguaje que es para saber si se requiere
    #analisis de ruby o julia
    def analyze_semantics(self, code, language):
        if language == 'ruby':
            self.analyze_ruby_semantics(code)
        elif language == 'julia':
            self.analyze_julia_semantics(code)

    #funcion de analisis semantico de ruby, haciendo uso de for's y la funcion rindall de regula expresion
    def analyze_ruby_semantics(self, code):
        # Verificar la correcta definición y uso de variables
        variables = re.findall(r'\b(\w+)\s*=\s*(.+?)\b', code)

        #en el caso de que detecte que una variable se intancion mas de una vez en codigo genera el error semantico
        for variable, value in variables:
            if variable in self.symbol_table[self.current_scope]:
                self.errors.append(f"Advertencia: Variable '{variable}' ya definida en el ámbito actual.")
            else:
                self.symbol_table[self.current_scope][variable] = value

        # Verificar llamadas a funciones y sus argumentos
        function_calls = re.findall(r'\b(\w+)\((.*?)\)\b', code)
        #en el caso de que detecte que se hace llamado a una funcion no instanciada genera el error
        for function, arguments in function_calls:
            if function not in self.symbol_table[self.current_scope]:
                self.errors.append(f"Error: Función '{function}' no definida.")
            else:
                # Verificar la correspondencia entre los argumentos de la función y sus parámetros
                expected_parameters = re.findall(r'\bdef\s+%s\((.*?)\)' % function, code)
                #en el caso de que detecte que se hizo envio de variables erroneas a una funcion
                if expected_parameters:
                    expected_parameters = expected_parameters[0].split(',')
                    provided_arguments = arguments.split(',')
                    if len(expected_parameters) != len(provided_arguments):
                        self.errors.append(f"Error: Número incorrecto de argumentos para la función '{function}'.")


    #
    #LAS MISMAS FUNCIONALIDADES SE APLICAN PARA EL ANALIZADOR DE JULIA
    #

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


#funcion de detecion de tipo de lenguaje, se hace uso de RE para listas 2 tipos de lenguajes con sus respectivas expresiones regulares

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

#funcion para abrir archivos en el tkinder
def open_file():
    #guarda en path la ubicacion del archivo con el askopenfilename, en este caso solo busca archivoz .jl y .rb
    path = askopenfilename(filetypes=[('Julia/Ruby Files', '*.jl .rb')])
    with open(path, 'r') as file:
        #con el archivo detectado, hace el read para mandar el codigo a memoriam, lo pone en el espacio de texto de code_output y 
        #llama la funcion detected_language para verificar el lenguaje
        code = file.read()
        code_output.delete("1.0", END)
        detected_language = detect_language(code)

        #AQUI SE PONE EL OUTPUT DEL ANALISIS EN ESTE CASO EL TIPO DE LENGUAJE

        code_output.insert("1.0", detected_language)

        #AQUI SE PONE EL CODIGO EN EL ESPACIO DE TEXTO DE ARRIBA
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)
        #ya con el lenguaje verificado se llama la funcion semantic_analyzer para hacer la detecion de semantica, se le manda el codigo y el tipo de lenguaje
        semantic_analyzer = SemanticsAnalyzer()
        semantic_analyzer.analyze_semantics(code, detected_language)

        error_message = semantic_analyzer.report_errors()

        #AQUI SE PONE LOS ERRORES SEMANTICOS DEL LENGUAJE, EN CASO DE QUE ERROR_MESSAGE ESTE VACIO SOLO MANDA UN TEXTO DICIENDO QUE NO HAY ERRORES SEMANTICOS
        if error_message:
            code_output.insert(END, f"\n\nErrores Semánticos:\n{error_message}")
        else:
            code_output.insert(END, "\n\nNo hay errores semánticos.")


#EN EL CASO DE QUE SE QUIERA ESCRIBIR USANDO TKINDER Y GUARDAR EL ARCHIVO SE TIENE LA FUNCION SAVE_AS
def save_as():
    #si no hay path, pregunta por el nombre del archivo para guardarlo
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    #con el nombre del archivo guarda el codigo presente en code desde la linea 1.0 hasta el end y le pone el path que contiene el nombre que le dimos la archivo
        #para guardar el archivo
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)


#se agrega el menu a la interfaz de tkinder

menu_bar = Menu(compiler)

#se agrega el menu desplegable a tkinder
file_menu = Menu(menu_bar, tearoff=0)
#se agregan al menu desplegable los comando de open, save, save as, exit 
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)

#se pone despligue de tipo cascada con todos los items de file_menu y se añade a menu bar
menu_bar.add_cascade(label='File', menu=file_menu)


#COMANDO NO NECESARIO, PROGRAMA NO REQUIERE EL RUN

#run_bar = Menu(menu_bar, tearoff=0)
#menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)

#se agrega un espacio de texto para el codigo y se empaqueta con el resto de la interfaz tkinder
editor = Text()
editor.pack()

#se agrega un espacio de texto para el output del codigo que contendra analisis de lenguaje, semantico y sintactico
code_output = Text(height=10)
code_output.pack()

compiler.mainloop()