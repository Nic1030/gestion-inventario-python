# Importamos la biblioteca Tkinter para la creación de la GUI.
import tkinter as tk
from tkinter import ttk

# --- Funciones de Eventos ---
def agregar_tarea():
    """
    Función que se ejecuta al presionar el botón 'Agregar'.
    Obtiene el texto del campo de entrada, lo agrega a la lista y limpia el campo.
    """
    tarea = entry_tarea.get()  # Obtenemos el texto del campo de entrada.
    if tarea:  # Verificamos que el campo no esté vacío.
        lista_tareas.insert(tk.END, tarea)  # Insertamos la tarea al final de la lista.
        entry_tarea.delete(0, tk.END)  # Limpiamos el campo de entrada.

def limpiar_todo():
    """
    Función que se ejecuta al presionar el botón 'Limpiar'.
    Borra todo el contenido de la lista de tareas y del campo de entrada.
    """
    lista_tareas.delete(0, tk.END)  # Borramos todos los elementos de la lista.
    entry_tarea.delete(0, tk.END)  # Limpiamos el campo de entrada.

# --- Configuración de la Ventana Principal ---
# Creamos la ventana principal de la aplicación.
ventana = tk.Tk()
ventana.title("Gestor de Tareas Sencillo")  # Título de la ventana.
ventana.geometry("400x300")  # Definimos el tamaño de la ventana.

# --- Creación de los Componentes GUI ---
# Etiqueta para el campo de entrada.
label_tarea = ttk.Label(ventana, text="Ingresa una nueva tarea:")
label_tarea.pack(pady=5)  # Usamos pack para organizar el widget con un relleno vertical.

# Campo de texto para que el usuario ingrese la tarea.
entry_tarea = ttk.Entry(ventana, width=40)
entry_tarea.pack(pady=5)

# Botón para agregar la tarea.
# El comando 'agregar_tarea' es la función que se llamará al hacer clic.
boton_agregar = ttk.Button(ventana, text="Agregar Tarea", command=agregar_tarea)
boton_agregar.pack(pady=5)

# Lista para mostrar las tareas.
lista_tareas = tk.Listbox(ventana, width=50, height=10)
lista_tareas.pack(pady=10)

# Botón para limpiar todos los datos.
# El comando 'limpiar_todo' es la función que se llamará al hacer clic.
boton_limpiar = ttk.Button(ventana, text="Limpiar Todo", command=limpiar_todo)
boton_limpiar.pack(pady=5)

# --- Bucle Principal de la Aplicación ---
# Este bucle mantiene la ventana abierta y escuchando eventos del usuario.
ventana.mainloop()
