import tkinter as tk
from tkinter import filedialog, font, ttk
from bvh import Bvh
import pandas as pd
import parametros
import interpolacion
import lectorbvh

#variables globales
BACKGROUND_COLOR = "lightblue"
marcador= ""
cuadro_desplazamiento = None
cuadro_velocidad = None
cuadro_aceleracion = None
cuadro_angulo = None
df_limpio = None
frame_listbox = None
nombres_marcadores = None
button_style = None
marcadores_pivote = None

def centrar_ventana(ventana,aplicacion_ancho,aplicacion_largo):    
    pantall_ancho = ventana.winfo_screenwidth()
    pantall_largo = ventana.winfo_screenheight()
    x = int((pantall_ancho/2) - (aplicacion_ancho/2))
    y = int((pantall_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")


# Función para cargar un archivo CSV
def cargar_csv():

    # Mostrar el cuadro de diálogo para seleccionar un archivo
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path:
        # Leer el archivo CSV seleccionado utilizando pandas (aquí puedes adaptar el tratamiento del archivo según tus necesidades)
        df_leido = pd.read_csv(file_path, header=None)  
        print("Archivo CSV cargado exitosamente:", file_path)
        print("TIPO DE DATO DF",type(df_leido))
        return df_leido
    else:
        print("No se seleccionó ningún archivo.")


def cargar_bvh():
    file_path = filedialog.askopenfilename(filetypes=[("BVH Files", "*.bvh")])

    if file_path:
        with open(file_path, 'r') as bvh_file:
            bvh_data = lectorbvh.Bvh(bvh_file.read())
        print("Archivo BVH cargado exitosamente:", file_path)

        
        # Llamar a la función plot_all_frames del módulo lectorbvh
        bvh_data.plot_all_frames(save_path='animacion.mp4')

        return bvh_data
    else:
        print("No se seleccionó ningún archivo BVH.")

def mostrar_modal():
    modal = tk.Tk()
    centrar_ventana(modal,400,200)
    modal.title("Proyecto Halterofilia")
    
    container = tk.Frame(modal,bg=BACKGROUND_COLOR)
    container.pack(fill='x', expand=True)

    mensaje = tk.Label(container, text="Por favor, carga un archivo CSV y BVH para comenzar.", font=("Arial", 11, "bold"), bg=BACKGROUND_COLOR)
    mensaje.pack(pady=5, padx=5)

    # Crear un objeto Style para usarlo en el botón
    global button_style
    button_style = ttk.Style()

    # Establecer el estilo del botón
    button_style.configure('BotonEstilo.TButton', foreground='black', background='#4caf50', font=('Arial', 9, 'bold'))

    # Crear el botón con el estilo personalizado
    boton_cargar = ttk.Button(container, text="Añadir Archivo CSV", command=lambda: iniciar_interfaz(modal), style='BotonEstilo.TButton')
    boton_cargar.pack(pady=5)

    # Crear el botón para cargar archivos BVH
    boton_cargar_bvh = ttk.Button(container, text="Añadir Archivo BVH", command=lambda: cargar_bvh())
    boton_cargar_bvh.pack(pady=5)

    modal.config(bg=BACKGROUND_COLOR)

    # Ejecutar la interfaz
    modal.mainloop()


def iniciar_interfaz(root):
    archivo_csv_cargado = cargar_csv()
    archivo_bvh_cargado = cargar_bvh()
    if archivo_csv_cargado is not None and archivo_bvh_cargado is not None:
        mostrar_interfaz(root, archivo_csv_cargado)


def mostrar_interfaz(root_to_destroy, archivo_csv_cargado):
    root_to_destroy.destroy()  # Cerrar la ventana actual

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Halterofilia")
    centrar_ventana(root, 820,650)

    # Crear los contenedores
    container_top = tk.Frame(root,bg="#1f2329",  height= 10)
    container_top.pack(side=tk.TOP, fill='both')

    container1 = tk.Frame(root,bg=BACKGROUND_COLOR)
    container1.pack(side=tk.LEFT, fill='x', expand=True)

    frame_separador = tk.Frame(root, bg="#f0f0f0", width=2, height=root.winfo_height())
    frame_separador.pack(side='left', fill='y', padx=5)

    container2 = tk.Frame(root,bg=BACKGROUND_COLOR)
    container2.pack(side=tk.LEFT, fill='x', expand=True)

    frame_separador = tk.Frame(root, bg="#f0f0f0", width=2, height=root.winfo_height())
    frame_separador.pack(side='left', fill='y', padx=5)

    container3 = tk.Frame(root,bg=BACKGROUND_COLOR)
    container3.pack(side=tk.RIGHT, fill='x', expand=True)

    global df_limpio

    df_limpio = parametros.cleaning(archivo_csv_cargado)
    encabezados = parametros.obtener_encabezados(df_limpio)
    patron = parametros.obtener_patron(encabezados)
    marcadores = parametros.obtener_marcadores(patron, encabezados)

    def on_select(event):
        global marcador 
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            print("index: ", index)
            marcador = patron + "-" + listbox.get(index)
            cuadro_marcador.config(text=marcador,bg="#f0f0f0")  # Actualizar el cuadro_marcador
            print("Opción seleccionada:", marcador)  

    label_archivo_cargado = tk.Label(container_top, text="Subir nuevo archivo ",font=("Arial", 10, "bold"),bg="#1f2329", fg="white")
    label_archivo_cargado.pack(pady=5,side=tk.LEFT)

    # Botón para cargar el archivo CSV
    cargar_archivo_btn = tk.Button(container_top, text="\uf093", command= cargar_csv)
    cargar_archivo_btn.pack(side=tk.LEFT)

    # Label
    label_selec_marcador = tk.Label(container1, text="Seleccionar marcador: ",font=("Arial", 12, "bold"),bg=BACKGROUND_COLOR)
    label_selec_marcador.pack()
    
    global frame_listbox
    # Frame para contener el Listbox con Scrollbar (dentro del contenedor)
    frame_listbox = tk.Frame(container1,bg=BACKGROUND_COLOR)
    frame_listbox.pack(pady=6)

    # Crear el Listbox con Scrollbar (dentro del contenedor)
    global nombres_marcadores
    listbox = tk.Listbox(frame_listbox, selectmode=tk.SINGLE, height=15)
    nombres_marcadores = [elemento.replace(patron+"-", "") for elemento in marcadores]
    for item in nombres_marcadores:
        listbox.insert(tk.END, item)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    scrollbar.config(command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)

    listbox.bind('<<ListboxSelect>>', on_select)

    def calcular_parametros():

        tiempo_inicial = entry_tiempo_inicial.get()
        tiempo_final = entry_tiempo_final.get()

        posicion_inicial = parametros.obtener_datos_marcador_tiempo(df_limpio, marcador ,tiempo_inicial)
        posicion_final = parametros.obtener_datos_marcador_tiempo(df_limpio, marcador, tiempo_final)

        desplazamiento, velocidad, aceleracion = parametros.calcular_parametros(posicion_inicial, posicion_final, marcador)

        if posicion_inicial:
            # Obtener los valores x, y, z del diccionario
            valores_inicial = posicion_inicial[marcador]
            x1, y1, z1 = valores_inicial[0], valores_inicial[1], valores_inicial[2]
            delta_x1, delta_y1, delta_z1,errorTotal_interpolado = interpolacion.calcular_error(x1,y1,z1)

            valores_final = posicion_final[marcador]
            x2, y2, z2 = valores_final[0], valores_final[1], valores_final[2]
            delta_x2, delta_y2, delta_z2,errorTotal_interpolado = interpolacion.calcular_error(x2,y2,z2)

            error_desplazamiento= round(float(parametros.error_desplazamiento(x1, y1, z1, x2, y2, z2, delta_x1, delta_y1, delta_z1, delta_x2, delta_y2, delta_z2)),3)
            error_velocidad= round(float(parametros.error_velocidad(desplazamiento, tiempo_inicial, tiempo_final, error_desplazamiento)),3)
            error_aceleracion= round(float(parametros.error_aceleracion(velocidad, tiempo_inicial, tiempo_final, error_velocidad)),3)

        else:
            print("No se encontraron datos para el marcador y tiempo proporcionados.")


        if desplazamiento is not None:
            cuadro_desplazamiento.config(text=str(desplazamiento)+ " \u00B1 " + str(error_desplazamiento)+ " m",bg="#f0f0f0")
            cuadro_velocidad.config(text=str(velocidad)+ " \u00B1 " + str(error_velocidad) +" m/s",bg="#f0f0f0")
            cuadro_aceleracion.config(text=str(aceleracion)+ " \u00B1 " + str(error_aceleracion) +" m/s^2",bg="#f0f0f0")
        else:
            print(f"Asegúrese de escoger un marcador")  

    def calcular_angulo():
        marcador_pivote = patron + "-" + select_pivote.get()
        marcador_vector1 = patron + "-" + cuadro_vector1["text"]
        marcador_vector2 = patron + "-" + cuadro_vector2["text"]

        tiempo = entry_tiempo_angulo.get()

        pivote = parametros.obtener_datos_marcador_tiempo(df_limpio, marcador_pivote ,tiempo)
        vector1 = parametros.obtener_datos_marcador_tiempo(df_limpio, marcador_vector1, tiempo)
        vector2 = parametros.obtener_datos_marcador_tiempo(df_limpio, marcador_vector2, tiempo)

        angulo = parametros.calcular_angulo(pivote, vector1, vector2)

        if pivote:
            valores_pivote = pivote[marcador_pivote]
            x1, y1, z1 = valores_pivote[0], valores_pivote[1], valores_pivote[2]

            valores_vector1 = vector1[marcador_vector1]
            x2, y2, z2 = valores_vector1[0], valores_vector1[1], valores_vector1[2]

            valores_vector2 = vector2[marcador_vector2]
            x3, y3, z3 = valores_vector2[0], valores_vector2[1], valores_vector2[2]

            vector_1 = [x2-x1, y2-y1, z2-z1]
            v_x1, v_y1, v_z1 = vector_1[0], vector_1[1], vector_1[2]
            delta_v_x1, delta_v_y1, delta_v_z1,errorTotal_interpolado = interpolacion.calcular_error(v_x1,v_y1,v_z1)
            
            vector_2 = [x3-x1, y3-y1, z3-z1]    
            v_x2, v_y2, v_z2 = vector_2[0], vector_2[1], vector_2[2]
            delta_v_x2, delta_v_y2, delta_v_z2,errorTotal_interpolado = interpolacion.calcular_error(v_x2,v_y2,v_z2)

            error_productopunto= round(float(parametros.error_productopunto(v_x1, v_y1, v_z1, v_x2, v_y2, v_z2, delta_v_x1, delta_v_y1, delta_v_z1, delta_v_x2, delta_v_y2, delta_v_z2)),3)
            error_magnitud_vector1= round(float(parametros.error_magnitud(vector_1,delta_v_x1, delta_v_y1, delta_v_z1)),3)
            error_magnitud_vector2= round(float(parametros.error_magnitud(vector_2,delta_v_x2, delta_v_y2, delta_v_z2)),3)
            error_angulo= round(float(parametros.error_angulo(vector_1,vector_2, error_productopunto, error_magnitud_vector1, error_magnitud_vector2)),3)
            
        else:
            print("No se encontraron datos para el marcador y tiempo proporcionados.")
        
        if angulo is not None:
            cuadro_angulo.config(text=str("{:.2f}".format(angulo))+ " \u00B1 " + str(error_angulo)+" grados",bg="#f0f0f0")
        else:
            print(f"No se pudo calcular el ángulo")  

        print(f"El ángulo entre los vectores es: {angulo} grados")

        # Label "Marcador" y cuadro de texto con la selección del usuario
    
    label_marcador = tk.Label(container1, text="Marcador seleccionado:",font=("Arial", 11, "bold"),bg=BACKGROUND_COLOR)
    label_marcador.pack(pady=(8,0))
    cuadro_marcador = tk.Label(container1, text="",bg=BACKGROUND_COLOR)
    cuadro_marcador.pack(pady=5)

    # Nuevo Frame para los Entry (dentro del contenedor)
    frame_entry = tk.Frame(container1,bg=BACKGROUND_COLOR)
    frame_entry.pack()

    # Label para el rango de tiempo (dentro del nuevo Frame)
    label_tiempo = tk.Label(frame_entry, text="Ingresar rango de tiempo: ",font=("Arial", 12, "bold"),bg=BACKGROUND_COLOR)
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
    
    def validar_tiempo_input(entry, *args):
        nuevo_valor = entry.get()
        if len(nuevo_valor) == 2 or len(nuevo_valor) == 5:
            entry.insert(tk.END, ":")  # Agregar ":" al final
            entry.after(1, lambda: entry.icursor(tk.END))  # Mover el cursor al final
    
    # Frame para los Entry (dentro del nuevo Frame)
    frame_labels_tiempo = tk.Frame(frame_entry,bg=BACKGROUND_COLOR)
    frame_labels_tiempo.pack(padx=10, pady=5)

    # Label para 'Tiempo inicial:'
    label_tiempo_inicial = tk.Label(frame_labels_tiempo, text="Tiempo inicial:",bg=BACKGROUND_COLOR,font=("Arial", 10))
    label_tiempo_inicial.pack(side=tk.LEFT, padx=5)

    # Label para 'Tiempo final:'
    label_tiempo_final = tk.Label(frame_labels_tiempo, text="Tiempo final:",bg=BACKGROUND_COLOR, font=("Arial", 10))
    label_tiempo_final.pack(side=tk.LEFT, padx=5)

    # Frame para los Entry (dentro del nuevo Frame)
    frame_entry_tiempo = tk.Frame(frame_entry, bg=BACKGROUND_COLOR)
    frame_entry_tiempo.pack(padx=10, pady=5)

    # Entradas para el tiempo inicial y final (dentro del nuevo Frame)
    entry_tiempo_inicial_var = tk.StringVar()
    entry_tiempo_inicial_var.trace_add("write", lambda *args: validar_tiempo_input(entry_tiempo_inicial, *args))
    entry_tiempo_inicial = tk.Entry(frame_entry_tiempo, fg='grey', width=15, textvariable=entry_tiempo_inicial_var)
    entry_tiempo_inicial.default_text = 'min:seg:mili seg'  # Texto predeterminado
    entry_tiempo_inicial.insert(0, entry_tiempo_inicial.default_text)
    entry_tiempo_inicial.bind("<FocusIn>", lambda event: borrar_texto_inicial(event, entry_tiempo_inicial))
    entry_tiempo_inicial.bind("<FocusOut>", lambda event: restaurar_texto_inicial(event, entry_tiempo_inicial))
    entry_tiempo_inicial.pack(side=tk.LEFT, padx=5)

    entry_tiempo_final_var = tk.StringVar()
    entry_tiempo_final_var.trace_add("write", lambda *args: validar_tiempo_input(entry_tiempo_final, *args))
    entry_tiempo_final = tk.Entry(frame_entry_tiempo, fg='grey', width=15, textvariable=entry_tiempo_final_var)
    entry_tiempo_final.default_text = 'min:seg:mili seg'  # Texto predeterminado
    entry_tiempo_final.insert(0, entry_tiempo_final.default_text)
    entry_tiempo_final.bind("<FocusIn>", lambda event: borrar_texto_inicial(event, entry_tiempo_final))
    entry_tiempo_final.bind("<FocusOut>", lambda event: restaurar_texto_inicial(event, entry_tiempo_final))
    entry_tiempo_final.pack(side=tk.LEFT, padx=5)

    # Botón "Enviar" para establecer el rango de tiempo (dentro del contenedor)
    boton_calcular = tk.Button(container1, text="Calcular parámetros", command=calcular_parametros, relief=tk.RAISED)
    boton_calcular.pack(pady=10)

    # Botón para actualizar el video
    ver_video_button = tk.Button(container2, text="Ver Video")
    ver_video_button.pack(padx=100)

    # Tercer contenedor dividido en dos secciones
    seccion_arriba = tk.Frame(container3,bg=BACKGROUND_COLOR)
    seccion_arriba.pack()

    seccion_abajo = tk.Frame(container3,bg=BACKGROUND_COLOR)
    seccion_abajo.pack()

    # Label "Parámetros" en la sección de arriba
    label_parametros = tk.Label(seccion_arriba, text="Parámetros", font=("Arial", 12, "bold"),bg=BACKGROUND_COLOR)
    label_parametros.pack(pady= 8)

    # Label "Desplazamiento" y cuadro de texto para mostrar el resultado del cálculo
    label_desplazamiento = tk.Label(seccion_arriba, text="Desplazamiento:",font=("Arial", 11, "bold"),bg=BACKGROUND_COLOR)
    label_desplazamiento.pack(pady=(1,0))
    cuadro_desplazamiento = tk.Label(seccion_arriba, text="",bg=BACKGROUND_COLOR)  # Mostrar el resultado
    cuadro_desplazamiento.pack()

    # Label "Velocidad" y cuadro de texto (puede estar vacío o con un valor inicial)
    label_velocidad = tk.Label(seccion_arriba, text="Velocidad:",font=("Arial", 11, "bold"),bg=BACKGROUND_COLOR)
    label_velocidad.pack(pady=(10,0))
    cuadro_velocidad = tk.Label(seccion_arriba, text="",bg=BACKGROUND_COLOR)
    cuadro_velocidad.pack()

    # Label "Aceleración" y cuadro de texto (puede estar vacío o con un valor inicial)
    label_aceleracion = tk.Label(seccion_arriba, text="Aceleración:",font=("Arial", 11, "bold"),bg=BACKGROUND_COLOR)
    label_aceleracion.pack(pady=(10,0))
    cuadro_aceleracion = tk.Label(seccion_arriba, text="",bg=BACKGROUND_COLOR)
    cuadro_aceleracion.pack()

    # Label "Angulos" en la sección de arriba
    label_angulos = tk.Label(seccion_abajo, text="Ángulos", font=("Arial", 12, "bold"),bg=BACKGROUND_COLOR)
    label_angulos.pack(pady=(22,0))

    def actualizar_vectores(*args):
        opcion_seleccionada = select_pivote.get()

        valores_asociados = marcadores_pivote[opcion_seleccionada]

        cuadro_vector1.config(text=valores_asociados[0])
        cuadro_vector2.config(text=valores_asociados[1])

    # Label que indica al usuario (dentro del contenedor)
    label_pivote = tk.Label(seccion_abajo, text="Seleccionar pivote: ",font=("Arial", 11, "bold"),bg=BACKGROUND_COLOR)
    label_pivote.pack(padx=10)

    #lista de los marcadores que seran pivote
    global marcadores_pivote
    marcadores_pivote = parametros.diccionario_pivotes()
    lista_pivote = list(marcadores_pivote.keys())
    #pivotes = [elemento.replace(patron+"-", "") for elemento in lista_pivote]

    # Select pivote
    select_pivote = tk.StringVar(root)
    select_pivote.set(lista_pivote[0])  # Opción por defecto
    select_pivote.trace_add('write', actualizar_vectores)  # Registrar la función de actualización
    dropdown1 = tk.OptionMenu(seccion_abajo, select_pivote, *lista_pivote)
    dropdown1.pack(pady=5)

    # Label que indica al usuario (dentro del contenedor)
    label_vector1 = tk.Label(seccion_abajo, text="Vector 1: ",font=("Arial", 11, "bold"),bg=BACKGROUND_COLOR)
    label_vector1.pack(padx=10)
    cuadro_vector1 = tk.Label(seccion_abajo, text=marcadores_pivote[lista_pivote[0]][0], bg='lightgray')  # Mostrar el resultado
   
    cuadro_vector1.pack(pady=5)

    label_vector2 = tk.Label(seccion_abajo, text="Vector 2: ",font=("Arial", 11, "bold"),bg=BACKGROUND_COLOR)
    label_vector2.pack(padx=10)
    cuadro_vector2 = tk.Label(seccion_abajo, text=marcadores_pivote[lista_pivote[0]][1], bg='lightgray')  # Mostrar el resultado
    cuadro_vector2.pack(pady=5)

    label_angulo = tk.Label(seccion_abajo, text="Ángulo:",font=("Arial", 11, "bold"),bg=BACKGROUND_COLOR)
    label_angulo.pack(padx = 10)
    cuadro_angulo = tk.Label(seccion_abajo, text="",bg=BACKGROUND_COLOR)
    cuadro_angulo.pack(pady=5)

    frame_angulo = tk.Frame(container3,bg=BACKGROUND_COLOR)
    frame_angulo.pack()

    frame_entry_angulo = tk.Frame(frame_angulo,bg=BACKGROUND_COLOR)
    frame_entry_angulo.pack(padx=10, pady=5)

    label_tiempo_angulo = tk.Label(frame_entry_angulo, text="Tiempo:",bg=BACKGROUND_COLOR, font=("Arial", 10))
    label_tiempo_angulo.pack(side=tk.LEFT, padx=5)

    entry_tiempo_angulo_var = tk.StringVar()
    entry_tiempo_angulo_var.trace_add("write", lambda *args: validar_tiempo_input(entry_tiempo_angulo, *args))
    entry_tiempo_angulo = tk.Entry(frame_entry_angulo, fg='grey', width=15, textvariable=entry_tiempo_angulo_var)
    entry_tiempo_angulo.default_text = 'min:seg:mili seg'  # Texto predeterminado
    entry_tiempo_angulo.insert(0, entry_tiempo_angulo.default_text)
    entry_tiempo_angulo.bind("<FocusIn>", lambda event: borrar_texto_inicial(event, entry_tiempo_angulo))
    entry_tiempo_angulo.bind("<FocusOut>", lambda event: restaurar_texto_inicial(event, entry_tiempo_angulo))
    entry_tiempo_angulo.pack(side=tk.LEFT, padx=5)

    # Botón "Enviar" para establecer el rango de tiempo (dentro del contenedor)
    boton_angulo = tk.Button(container3, text="Calcular ángulo", command=calcular_angulo, relief=tk.RAISED)
    boton_angulo.pack(pady=10)

    root.config(bg=BACKGROUND_COLOR)

    root.mainloop()


# Mostrar el pop-up inicial para cargar el archivo CSV
mostrar_modal()
