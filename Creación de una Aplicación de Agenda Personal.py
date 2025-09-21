import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from tkcalendar import Calendar  # Es una librería externa, necesitas instalarla

# Para instalar tkcalendar:
# pip install tkcalendar

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("800x600")

        # Almacena los eventos en una lista de diccionarios
        self.events = []

        # --- Frames para organizar la interfaz ---
        self.input_frame = tk.Frame(self.root, padx=10, pady=10)
        self.input_frame.pack(side=tk.TOP, fill=tk.X)

        self.tree_frame = tk.Frame(self.root, padx=10, pady=10)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.root, padx=10, pady=10)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # --- Componentes de la Interfaz ---
        self.create_input_widgets()
        self.create_treeview()
        self.create_buttons()

    def create_input_widgets(self):
        """Crea los campos de entrada para la fecha, hora y descripción."""
        tk.Label(self.input_frame, text="Fecha:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = tk.Entry(self.input_frame)
        self.date_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.date_entry.bind("<FocusIn>", self.show_calendar) # Vincula el evento de clic al widget del calendario

        tk.Label(self.input_frame, text="Hora (HH:MM):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.time_entry = tk.Entry(self.input_frame)
        self.time_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        tk.Label(self.input_frame, text="Descripción:").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.desc_entry = tk.Entry(self.input_frame)
        self.desc_entry.grid(row=0, column=5, sticky="ew", padx=5, pady=5)

    def show_calendar(self, event):
        """Muestra el DatePicker para seleccionar una fecha."""
        top = tk.Toplevel(self.root)
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=10, pady=10)

        def set_date():
            selected_date = cal.get_date()
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, selected_date)
            top.destroy()

        tk.Button(top, text="Seleccionar", command=set_date).pack(pady=5)

    def create_treeview(self):
        """Crea el TreeView para mostrar la lista de eventos."""
        columns = ("Fecha", "Hora", "Descripción")
        self.event_tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        self.event_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for col in columns:
            self.event_tree.heading(col, text=col)
            self.event_tree.column(col, width=200, anchor=tk.CENTER)
            
        # Añadir un scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.event_tree.yview)
        self.event_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_buttons(self):
        """Crea los botones de acción."""
        self.add_button = tk.Button(self.button_frame, text="Agregar Evento", command=self.add_event)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Eliminar Evento", command=self.delete_event)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.exit_button = tk.Button(self.button_frame, text="Salir", command=self.root.quit)
        self.exit_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def add_event(self):
        """Agrega un nuevo evento a la lista y al TreeView."""
        date = self.date_entry.get()
        time = self.time_entry.get()
        desc = self.desc_entry.get()

        if date and time and desc:
            event_id = len(self.events) # Genera un ID simple para el evento
            self.events.append({"id": event_id, "date": date, "time": time, "desc": desc})
            self.event_tree.insert("", "end", iid=event_id, values=(date, time, desc))
            
            # Limpiar los campos de entrada
            self.date_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos para agregar un evento.")

    def delete_event(self):
        """Elimina el evento seleccionado del TreeView y de la lista."""
        selected_item = self.event_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, selecciona un evento para eliminar.")
            return

        # Diálogo de confirmación
        if messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que quieres eliminar este evento?"):
            for item in selected_item:
                item_id = int(self.event_tree.item(item)['iid'])
                self.event_tree.delete(item)
                # Opcional: eliminar también de la lista interna self.events
                self.events = [e for e in self.events if e['id'] != item_id]

# --- Punto de entrada de la aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
