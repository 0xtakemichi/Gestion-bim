import os
import csv
import tkinter as tk
from tkinter import messagebox, Tk, Text, N, S, E, W

class ObservationsForm(tk.Tk):
    def __init__(self, observaciones):
        super().__init__()
        self.title("Llenar Observaciones")
        self.observaciones = observaciones
        self.current_index = 0
        self.observation_counter = 1
        # Establecer el tamaño mínimo de la ventana
        self.minsize(600, 400)

        # Hacer que los widgets se adapten al tamaño de la ventana
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)
        
        self.label_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self.label_label = tk.Label(self, text="Label:")
        self.label_label.grid(row=0, column=0, sticky="w")
        self.label_entry = tk.Entry(self, textvariable=self.label_var, state="readonly")
        self.label_entry.grid(row=0, column=1, sticky=N+S+E+W)

        self.title_label = tk.Label(self, text="Title:")
        self.title_label.grid(row=1, column=0, sticky="w")
        self.title_entry = tk.Entry(self, textvariable=self.title_var)
        self.title_entry.grid(row=1, column=1, sticky=N+S+E+W)

        self.description_label = tk.Label(self, text="Description:")
        self.description_label.grid(row=2, column=0, sticky="w")
        self.description_entry = tk.Entry(self,textvariable=self.description_var, width=50)
        self.description_entry.grid(row=2, column=1, columnspan=2)

        self.description_label = tk.Label(self, text="Description:")
        self.description_label.grid(row=2, column=0, sticky="w")
        self.description_entry = tk.Text(self, width=50, height=10, wrap='word')
        self.description_entry.grid(row=2, column=1, columnspan=2, sticky=N+S+E+W)

        self.type_options = self.read_options_from_csv('csv_files/options_menu/TipoTareas.csv')
        #self.type_options = ["Comentario", "Error", "Consulta", "Solicitud","Remark","Sin Definir", "Choque", "Problema"]
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

        self.status_options = self.read_options_from_csv('csv_files/options_menu/EstadoTareas.csv')
        #self.status_options = ["Nueva", "Cerrada", "Terminada", "En Progreso", "En Espera"]
        self.status_label = tk.Label(self, text="Status:")
        self.status_label.grid(row=5, column=0, sticky="w")
        self.status_entry = tk.OptionMenu(self, self.status_var, * self.status_options)
        self.status_entry.grid(row=5, column=1, sticky=N+S+E+W)

        # Crear un marco para los botones
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=6, column=1, sticky=N+S+E+W)

        # Configurar las columnas del marco para que se expandan
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)

        # Colocar los botones en el marco
        self.fill_button = tk.Button(self.buttons_frame, text="Fill", command=self.fill)
        self.fill_button.grid(row=0, column=0, sticky=N+S+E+W)

        self.next_button = tk.Button(self.buttons_frame, text="Next", command=self.next_observation)
        self.next_button.grid(row=0, column=1, sticky=N+S+E+W)
        self.fill_first_observation()

    @staticmethod
    def read_options_from_csv(csv_file_path):
        """
        Lee las opciones desde un archivo CSV y devuelve una lista con ellas.
        Asume que cada opción está en su propia fila en la primera columna.
        """
        if not os.path.exists(csv_file_path):
            messagebox.showerror("Error", f"El archivo {csv_file_path} no existe.")
            return []

        options = []
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar el encabezado
            options = [row[0] for row in reader if row]  # Asegúrate de que la fila no esté vacía
        return options
    
    def fill_first_observation(self):
        self.fill_observation(self.observaciones[self.current_index])

    def fill_observation(self, observation):
        self.label_var.set(self.observation_counter)
        self.title_var.set("")
        #self.description_var.set(observation[2])
        self.description_entry.delete('1.0', tk.END)  # Limpiar contenido previo
        self.description_entry.insert('1.0', observation[2])
        self.type_var.set(self.type_options[0])
        self.priority_var.set(self.priority_options[1])
        self.status_var.set(self.status_options[0])

        # Calcular la cantidad de líneas en el texto
        num_lines = int(self.description_entry.index('end-1c').split('.')[0])
        # Ajustar la altura del widget Text
        self.description_entry.config(height=num_lines*1.8)

    def fill(self):
        if (title := self.title_var.get()) and (type := self.type_var.get()) and (priority := self.priority_var.get()) and (status := self.status_var.get()):
            observation = list(self.observaciones[self.current_index])
            description_text = self.description_entry.get('1.0',tk.END).strip()
            #label = str(self.label_var.get()) + '.'
            label = self.label_var.get()
            observation[0] = label
            observation[1] = title
            observation[2] = description_text
            observation[3] = type
            observation[4] = priority
            observation[5] = status
            self.observaciones[self.current_index] = tuple(observation)
            #messagebox.showinfo("Info", "Saved")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "All fields must be filled.")

    def clear_fields(self):
        self.title_var.set("")
        self.description_entry.delete('1.0', tk.END)
        #self.type_var.set("")
        #self.priority_var.set("")
        #self.status_var.set("")

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
        csv_folder = "csv_files"
        csv_filename = "observaciones_filled.csv"
        csv_path = os.path.join(csv_folder, csv_filename)
        
        # Comprobar si el archivo CSV existe
        if os.path.exists(csv_path):
            with open(csv_path, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                existing_labels = [row[0] for row in reader if row]  # Lista de todos los labels existentes
                if existing_labels:
                    last_label = max(map(int, existing_labels[1:]))  # Ignorar el encabezado y encontrar el último label
                else:
                    last_label = 0
        else:
            last_label = 0
        
        # Actualizar los labels de las observaciones con los nuevos valores
        for i, observation in enumerate(self.observaciones):
            self.observaciones[i] = (str(last_label + i + 1),) + observation[1:]
        
        # Crear el directorio si no existe
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)
        
        # Guardar los datos en el archivo CSV
        with open(csv_path, 'a', newline='') as csv_file:  # 'a' para añadir datos sin sobrescribir
            writer = csv.writer(csv_file)
            if last_label == 0:  # Si es la primera vez, escribir el encabezado
                writer.writerow(["Label", "Title", "Description", "Type", "Priority", "Status"])
            writer.writerows(self.observaciones)