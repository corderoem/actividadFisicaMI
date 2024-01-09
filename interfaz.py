import tkinter as tk
import parametros

# Crear la ventana principal
root = tk.Tk()
root.title("Halterofilia")


BACKGROUND_COLOR = "lightblue"
# Crear los contenedores
container1 = tk.Frame(root,bg=BACKGROUND_COLOR)
container1.pack(side=tk.LEFT)

container2 = tk.Frame(root,bg=BACKGROUND_COLOR)
container2.pack(side=tk.LEFT)

container3 = tk.Frame(root,bg=BACKGROUND_COLOR)
container3.pack(side=tk.RIGHT)

#variables globales
marcador= ""
cuadro_desplazamiento = None
cuadro_velocidad = None
cuadro_aceleracion = None
cuadro_angulo = None
df = parametros.obtenerdata() #Dataframe limpio
marcadores = parametros.marcadores #Lista de los marcadores del CSV

def on_select(event):
    global marcador 
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        print("index: ", index)
        marcador = listbox.get(index)
        cuadro_marcador.config(text=marcador)  # Actualizar el cuadro_marcador
        print("Opción seleccionada:", marcador)  


# Botón para cargar el archivo CSV
cargar_archivo_btn = tk.Button(container1, text="Cargar Archivo CSV", command=parametros.cargar_csv)
cargar_archivo_btn.pack(padx=20, pady=10)

# Label
label_selec_marcador = tk.Label(container1, text="Seleccionar marcador: ",font=("Arial", 10, "bold"),bg=BACKGROUND_COLOR)
label_selec_marcador.pack(pady=5)

# Frame para contener el Listbox con Scrollbar (dentro del contenedor)
frame_listbox = tk.Frame(container1,bg=BACKGROUND_COLOR)
frame_listbox.pack(pady=5)

# Crear el Listbox con Scrollbar (dentro del contenedor)
listbox = tk.Listbox(frame_listbox, selectmode=tk.SINGLE, height=10)
for item in marcadores:
    listbox.insert(tk.END, item)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar.config(command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)

listbox.bind('<<ListboxSelect>>', on_select)

# Crear un nuevo Frame para los Entry (dentro del contenedor)
frame_entry = tk.Frame(container1,bg=BACKGROUND_COLOR)
frame_entry.pack()


def calcular_parametros():
    global tiempo_inicial
    global tiempo_final

    tiempo_inicial = entry_tiempo_inicial.get()
    tiempo_final = entry_tiempo_final.get()

    posicion_inicial = parametros.obtener_datos_marcador_tiempo(df, marcador ,tiempo_inicial)

    posicion_final = parametros.obtener_datos_marcador_tiempo(df, marcador, tiempo_final)

    desplazamiento, velocidad, aceleracion = parametros.calcular_parametros(posicion_inicial, posicion_final, marcador)

    if desplazamiento is not None:
        print(f"El desplazamiento del marcador '{marcador}' es: {desplazamiento} m")
        print(f"La velocidad del marcador '{marcador}' es: {velocidad} m/s")
        print(f"La aceleración del marcador '{marcador}' es: {aceleracion} m/s^2")

        cuadro_desplazamiento.config(text=str(desplazamiento)+" m")
        cuadro_velocidad.config(text=str(velocidad)+" m/s")
        cuadro_aceleracion.config(text=str(aceleracion)+" m/s^2")
    else:
        print(f"Asegúrese de escoger un marcador")  


def calcular_angulo():

    marcador_pivote = select_pivote.get()
    marcador_vector1 = select_vector1.get()
    marcador_vector2 = select_vector2.get()
    tiempo = entry_tiempo_angulo.get()

    pivote = parametros.obtener_datos_marcador_tiempo(df, marcador_pivote ,tiempo)
    vector1 = parametros.obtener_datos_marcador_tiempo(df, marcador_vector1, tiempo)
    vector2 = parametros.obtener_datos_marcador_tiempo(df, marcador_vector2, tiempo)

    angulo = parametros.calcular_angulo(pivote, vector1, vector2)
    
    if angulo is not None:
        cuadro_angulo.config(text=str("{:.2f}".format(angulo))+" grados")
    else:
        print(f"No se pudo calcular el ángulo")  

    print(f"El ángulo entre los vectores es: {angulo} grados")


# Label para el rango de tiempo (dentro del nuevo Frame)
label_tiempo = tk.Label(frame_entry, text="Ingresar rango de tiempo: ",font=("Arial", 10, "bold"),bg=BACKGROUND_COLOR)
label_tiempo.pack(side=tk.TOP, padx=10, pady=5)

# Funciones para manejar los eventos de clic y salida de los Entry
def borrar_texto_inicial(event, entry):
    if entry.get() == entry.default_text:
        entry.delete(0, tk.END)
        entry['fg'] = 'black'

def restaurar_texto_inicial(event, entry):
    if not entry.get():
        entry.insert(0, entry.default_text)
        entry['fg'] = 'grey'


# Frame para los Entry (dentro del nuevo Frame)
frame_labels_tiempo = tk.Frame(frame_entry,bg=BACKGROUND_COLOR)
frame_labels_tiempo.pack(padx=10, pady=5)

# Label para 'Tiempo inicial:'
label_tiempo_inicial = tk.Label(frame_labels_tiempo, text="Tiempo inicial:",bg=BACKGROUND_COLOR)
label_tiempo_inicial.pack(side=tk.LEFT, padx=5)

# Label para 'Tiempo final:'
label_tiempo_final = tk.Label(frame_labels_tiempo, text="Tiempo final:",bg=BACKGROUND_COLOR)
label_tiempo_final.pack(side=tk.LEFT, padx=15)

# Frame para los Entry (dentro del nuevo Frame)
frame_entry_tiempo = tk.Frame(frame_entry,bg=BACKGROUND_COLOR)
frame_entry_tiempo.pack(padx=10, pady=5)

# Entradas para el tiempo inicial y final (dentro del nuevo Frame)
entry_tiempo_inicial = tk.Entry(frame_entry_tiempo, fg='grey', width=15)
entry_tiempo_inicial.default_text = 'min:seg:mili seg'  # Texto predeterminado
entry_tiempo_inicial.insert(0, entry_tiempo_inicial.default_text)
entry_tiempo_inicial.bind("<FocusIn>", lambda event: borrar_texto_inicial(event, entry_tiempo_inicial))
entry_tiempo_inicial.bind("<FocusOut>", lambda event: restaurar_texto_inicial(event, entry_tiempo_inicial))
entry_tiempo_inicial.pack(side=tk.LEFT, padx=5)


entry_tiempo_final = tk.Entry(frame_entry_tiempo, fg='grey', width=15)
entry_tiempo_final.default_text = 'min:seg:mili seg'  # Texto predeterminado
entry_tiempo_final.insert(0, entry_tiempo_final.default_text)
entry_tiempo_final.bind("<FocusIn>", lambda event: borrar_texto_inicial(event, entry_tiempo_final))
entry_tiempo_final.bind("<FocusOut>", lambda event: restaurar_texto_inicial(event, entry_tiempo_final))
entry_tiempo_final.pack(side=tk.LEFT, padx=5)


# Botón "Enviar" para establecer el rango de tiempo (dentro del contenedor)
boton_calcular = tk.Button(container1, text="Calcular parámetros", command=calcular_parametros, relief=tk.RAISED)
boton_calcular.pack(pady=10)

# Segundo contenedor para el video
# Botón para actualizar el video
ver_video_button = tk.Button(container2, text="Ver Video")
ver_video_button.pack(padx=100)


# Tercer contenedor dividido en dos secciones
seccion_arriba = tk.Frame(container3,bg=BACKGROUND_COLOR)
seccion_arriba.pack()

seccion_abajo = tk.Frame(container3,bg=BACKGROUND_COLOR)
seccion_abajo.pack()


# Label "Parámetros" en la sección de arriba
label_parametros = tk.Label(seccion_arriba, text="Parámetros", font=("Arial", 11, "bold"),bg=BACKGROUND_COLOR)
label_parametros.pack(pady= 10)

# Label "Marcador" y cuadro de texto con la selección del usuario
label_marcador = tk.Label(seccion_arriba, text="Marcador:",font=("Arial", 10, "bold"),bg=BACKGROUND_COLOR)
label_marcador.pack()
cuadro_marcador = tk.Label(seccion_arriba, text="",bg=BACKGROUND_COLOR)
cuadro_marcador.pack()


# Label "Desplazamiento" y cuadro de texto para mostrar el resultado del cálculo
label_desplazamiento = tk.Label(seccion_arriba, text="Desplazamiento:",font=("Arial", 10, "bold"),bg=BACKGROUND_COLOR)
label_desplazamiento.pack()
cuadro_desplazamiento = tk.Label(seccion_arriba, text="",bg=BACKGROUND_COLOR)  # Mostrar el resultado
cuadro_desplazamiento.pack()

# Label "Velocidad" y cuadro de texto (puede estar vacío o con un valor inicial)
label_velocidad = tk.Label(seccion_arriba, text="Velocidad:",font=("Arial", 10, "bold"),bg=BACKGROUND_COLOR)
label_velocidad.pack()
cuadro_velocidad = tk.Label(seccion_arriba, text="",bg=BACKGROUND_COLOR)
cuadro_velocidad.pack()

# Label "Aceleración" y cuadro de texto (puede estar vacío o con un valor inicial)
label_aceleracion = tk.Label(seccion_arriba, text="Aceleración:",font=("Arial", 10, "bold"),bg=BACKGROUND_COLOR)
label_aceleracion.pack()
cuadro_aceleracion = tk.Label(seccion_arriba, text="",bg=BACKGROUND_COLOR)
cuadro_aceleracion.pack()


# Label "Angulos" en la sección de arriba
label_parametros = tk.Label(seccion_abajo, text="Ángulos", font=("Arial", 11, "bold"),bg=BACKGROUND_COLOR)
label_parametros.pack(pady=5)

# Label que indica al usuario (dentro del contenedor)
label_pivote = tk.Label(seccion_abajo, text="Seleccionar pivote: ",font=("Arial", 10, "bold"),bg=BACKGROUND_COLOR)
label_pivote.pack(padx=10)

#lista de los marcadores que seran pivote
marcadores_pivote = parametros.lista_pivotes

# Select pivote
select_pivote = tk.StringVar(root)
select_pivote.set(marcadores_pivote[0])  # Opción por defecto
dropdown3 = tk.OptionMenu(seccion_abajo, select_pivote, *marcadores_pivote)
dropdown3.pack(pady=5)

# Label que indica al usuario (dentro del contenedor)
label_vector1 = tk.Label(seccion_abajo, text="Seleccionar vector 1: ",font=("Arial", 10, "bold"),bg=BACKGROUND_COLOR)
label_vector1.pack(padx=10)

#lista de pivotes
marcadores_vector1 = parametros.lista_vector1

# Select vector 1
select_vector1 = tk.StringVar(root)
select_vector1.set(marcadores_vector1[0])  # Opción por defecto
dropdown3 = tk.OptionMenu(seccion_abajo, select_vector1, *marcadores_vector1)
dropdown3.pack(padx=5)

# Label que indica al usuario (dentro del contenedor)
label_vector2 = tk.Label(seccion_abajo, text="Seleccionar vector 2: ",font=("Arial", 10, "bold"),bg=BACKGROUND_COLOR)
label_vector2.pack(padx=10)

marcadores_vector2 = parametros.lista_vector2

# Select vector 2
select_vector2 = tk.StringVar(root)
select_vector2.set(marcadores_vector2[0])  # Opción por defecto
dropdown3 = tk.OptionMenu(seccion_abajo, select_vector2, *marcadores_vector2)
dropdown3.pack(pady=5)

# Label "Aceleración" y cuadro de texto (puede estar vacío o con un valor inicial)
label_angulo = tk.Label(seccion_abajo, text="Ángulo:",font=("Arial", 10, "bold"),bg=BACKGROUND_COLOR)
label_angulo.pack(padx = 10)
cuadro_angulo = tk.Label(seccion_abajo, text="",bg=BACKGROUND_COLOR)
cuadro_angulo.pack(pady=5)


frame_angulo = tk.Frame(container3,bg=BACKGROUND_COLOR)
frame_angulo.pack()

# Frame para los Entry (dentro del nuevo Frame)
frame_entry_angulo = tk.Frame(frame_angulo,bg=BACKGROUND_COLOR)
frame_entry_angulo.pack(padx=10, pady=5)

# Label para 'Tiempo inicial:'
label_tiempo_angulo = tk.Label(frame_entry_angulo, text="Tiempo:",bg=BACKGROUND_COLOR)
label_tiempo_angulo.pack(side=tk.LEFT, padx=5)

# Entradas para el tiempo inicial y final (dentro del nuevo Frame)
entry_tiempo_angulo = tk.Entry(frame_entry_angulo, fg='grey', width=15)
entry_tiempo_angulo.default_text = 'min:seg:mili seg'  # Texto predeterminado
entry_tiempo_angulo.insert(0, entry_tiempo_inicial.default_text)
entry_tiempo_angulo.bind("<FocusIn>", lambda event: borrar_texto_inicial(event, entry_tiempo_angulo))
entry_tiempo_angulo.bind("<FocusOut>", lambda event: restaurar_texto_inicial(event, entry_tiempo_angulo))
entry_tiempo_angulo.pack(side=tk.LEFT, padx=5)

# Botón "Enviar" para establecer el rango de tiempo (dentro del contenedor)
boton_angulo = tk.Button(container3, text="Calcular ángulo", command=calcular_angulo, relief=tk.RAISED)
boton_angulo.pack(pady=10)


# Aplicar estilos a elementos específicos
root.config(bg=BACKGROUND_COLOR)

# Ejecutar la interfaz
root.mainloop()