import tkinter as tk
from tkinter import messagebox, N, S, E, W
from datetime import datetime
from .csv_handler import CSVHandler

class ObservationsForm(tk.Tk):
    def __init__(self, observaciones):
        super().__init__()
        self.title("Llenar Observaciones")
        self.observaciones = observaciones
        self.csv_handler = CSVHandler('csv_files', 'observaciones_filled.csv')
        self.current_index = 0
        self.observation_counter = 1
        # Establecer el tamaño mínimo de la ventana
        self.minsize(800, 500)

        # Hacer que los widgets se adapten al tamaño de la ventana
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)
        
        self.label_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.assignee_var = tk.StringVar()
        self.tags_var = tk.StringVar()

        self.label_label = tk.Label(self, text="Label:")
        self.label_label.grid(row=0, column=0, sticky="w")
        self.label_entry = tk.Entry(self, textvariable=self.label_var, state="readonly",justify='center', borderwidth=0)
        self.label_entry.grid(row=0, column=1)

        self.title_label = tk.Label(self, text="Title:")
        self.title_label.grid(row=1, column=0, sticky="w")
        self.title_entry = tk.Entry(self, textvariable=self.title_var, justify='center')
        self.title_entry.grid(row=1, column=1, sticky=E+W)

        self.description_label = tk.Label(self, text="Description:")
        self.description_label.grid(row=2, column=0, sticky="w")
        self.description_entry = tk.Text(self, width=50, height=10, wrap='word')
        self.description_entry.grid(row=2, column=1, columnspan=2, sticky=N+S+E+W)

        #self.type_options = self.read_options_from_csv('csv_files/options_menu/TipoTareas.csv')
        #self.type_options = ["Comentario", "Error", "Consulta", "Solicitud","Remark","Sin Definir", "Choque", "Problema"]
        self.type_options = self.csv_handler.read_options_from_csv('csv_options/TipoTareas.csv')
        self.type_label = tk.Label(self, text="Type:")
        self.type_label.grid(row=3, column=0, sticky="w")
        self.type_entry = tk.OptionMenu(self, self.type_var, * self.type_options)
        self.type_entry.grid(row=3, column=1, sticky=N+S+E+W)

        # Crear una lista con las opciones
        #self.priority_options = self.read_options_from_csv('csv_files/PrioridadTareas.csv')
        self.priority_options = ["Bajo", "Normal", "Alto", "Crítico"]
        # Crear el menú desplegable
        self.priority_label = tk.Label(self, text="Priority:")
        self.priority_label.grid(row=4, column=0, sticky="w")
        self.priority_menu = tk.OptionMenu(self, self.priority_var, * self.priority_options)
        self.priority_menu.grid(row=4, column=1, sticky=N+S+E+W)

        #self.status_options = self.read_options_from_csv('csv_files/options_menu/EstadoTareas.csv')
        #self.status_options = ["Nueva", "Cerrada", "Terminada", "En Progreso", "En Espera"]
        self.status_options = self.csv_handler.read_options_from_csv('csv_options/EstadoTareas.csv')
        self.status_label = tk.Label(self, text="Status:")
        self.status_label.grid(row=5, column=0, sticky="w")
        self.status_entry = tk.OptionMenu(self, self.status_var, * self.status_options)
        self.status_entry.grid(row=5, column=1, sticky=N+S+E+W)

        self.assignee_options = [""]
        self.assignee_label = tk.Label(self, text="Assignee(s):")
        self.assignee_label.grid(row=6, column=0, sticky="w")  # Asegúrate de que el número de fila sea el siguiente después de "Status"
        self.assignee_entry = tk.OptionMenu(self, self.assignee_var, * self.assignee_options)
        self.assignee_entry.grid(row=6, column=1, sticky=N+S+E+W)

        self.tags_options = ["Modelado", "Estructuras", "Diseño Geometrico", "Topografía", "Semaforización"]
        self.tags_label = tk.Label(self, text="Tags:")
        self.tags_label.grid(row=7, column=0, sticky="w")
        self.tags_entry = tk.OptionMenu(self, self.tags_var, * self.tags_options)
        self.tags_entry.grid(row=7, column=1, sticky=N+S+E+W)

        # Crear un marco para los botones
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=8, column=1, sticky=N+S+E+W)

        # Configurar las columnas del marco para que se expandan
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)

        # Colocar los botones en el marco
        self.fill_button = tk.Button(self.buttons_frame, text="Fill", command=self.fill)
        self.fill_button.grid(row=0, column=0, sticky=N+S+E+W)

        self.next_button = tk.Button(self.buttons_frame, text="Next", command=self.next_observation)
        self.next_button.grid(row=0, column=1, sticky=N+S+E+W)
        self.fill_first_observation()

    # Calcular las lineas y el espacio que tendra el widget de description
    def calculate_num_lines_required(self, text_widget, text):
        self.update_idletasks()  # Asegura que la interfaz gráfica esté actualizada
        text_widget_width_pixels = text_widget.winfo_width()
        if text_widget_width_pixels > 0:
            char_width = 7  # Ajusta esto según la fuente que estés utilizando
            text_widget_width_chars = max(1, text_widget_width_pixels // char_width)
            text_length = len(text)
            num_lines_required = text_length // text_widget_width_chars + 1
        else:
            num_lines_required = 10  # Un valor predeterminado si no se puede calcular
        return num_lines_required
    
    def fill_first_observation(self):
        self.after(100, self.fill_observation, self.observaciones[self.current_index])
        #self.fill_observation(self.observaciones[self.current_index])

    def fill_observation(self, observation):
        self.label_var.set(str(self.observation_counter) + ".")
        self.title_var.set("")
        #self.description_var.set(observation[2])
        self.description_entry.delete('1.0', tk.END)  # Limpiar contenido previo
        self.description_entry.insert('1.0', observation[2])
        self.type_var.set(self.type_options[0])
        self.priority_var.set(self.priority_options[1])
        self.status_var.set(self.status_options[0])
        self.assignee_var.set(self.assignee_options[0])
        self.tags_var.set(self.tags_options[0])
        # Comprobacion tamano
        description_text = observation[2]
        num_lines_required = self.calculate_num_lines_required(self.description_entry, description_text)
        # Ajustar la altura del widget Text
        self.description_entry.config(height=num_lines_required)

    def fill(self):
        if (title := self.title_var.get()) and (type := self.type_var.get()) and (priority := self.priority_var.get()) and (status := self.status_var.get()):
            observation = list(self.observaciones[self.current_index])
            description_text = self.description_entry.get('1.0',tk.END).strip()
            label = self.label_var.get()
            assignee = self.assignee_var.get()
            tags = self.tags_var.get()
            # Time now to colummn Created on
            time_now = datetime.now()
            time = time_now.strftime("%b %d %Y %I:%M %p CLST")
            observation[0] = label
            observation[1] = title
            observation[2] = description_text
            observation[3] = type
            observation[4] = priority
            observation[5] = status
            observation[6] = assignee
            observation[7] = tags
            observation[8] = time
            self.observaciones[self.current_index] = tuple(observation)
            self.clear_fields()
        else:
            messagebox.showerror("Error", "All fields must be filled.")

    def clear_fields(self):
        self.title_var.set("")
        self.description_entry.delete('1.0', tk.END)

    def next_observation(self):
        self.fill()
        self.current_index += 1
        self.observation_counter += 1
        if self.current_index < len(self.observaciones):
            self.fill_observation(self.observaciones[self.current_index])
        else:
            self.save_to_csv()
            messagebox.showinfo("Info", "All observations filled and saved to CSV.")
            self.destroy()

    def save_to_csv(self):
        self.csv_handler.save_observations_to_csv(self.observaciones)
        messagebox.showinfo("Info", "All observations filled and saved to CSV.")