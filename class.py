import os
import csv
import tkinter as tk
from tkinter import messagebox

class ObservationsForm(tk.Tk):
    def __init__(self, observaciones):
        super().__init__()
        self.title("Llenar Observaciones")
        self.observaciones = observaciones
        self.current_index = 0

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
        self.label_entry.grid(row=0, column=1)

        self.title_label = tk.Label(self, text="Title:")
        self.title_label.grid(row=1, column=0, sticky="w")
        self.title_entry = tk.Entry(self, textvariable=self.title_var)
        self.title_entry.grid(row=1, column=1)

        self.description_label = tk.Label(self, text="Description:")
        self.description_label.grid(row=2, column=0, sticky="w")
        self.description_entry = tk.Entry(self,textvariable=self.description_var, width=50)
        self.description_entry.grid(row=2, column=1, columnspan=2)

        self.type_label = tk.Label(self, text="Type:")
        self.type_label.grid(row=3, column=0, sticky="w")
        self.type_entry = tk.Entry(self, textvariable=self.type_var)
        self.type_entry.grid(row=3, column=1)

        self.priority_label = tk.Label(self, text="Priority:")
        self.priority_label.grid(row=4, column=0, sticky="w")
        self.priority_entry = tk.Entry(self, textvariable=self.priority_var)
        self.priority_entry.grid(row=4, column=1)

        self.status_label = tk.Label(self, text="Status:")
        self.status_label.grid(row=5, column=0, sticky="w")
        self.status_entry = tk.Entry(self, textvariable=self.status_var)
        self.status_entry.grid(row=5, column=1)

        self.fill_button = tk.Button(self, text="Fill", command=self.fill)
        self.fill_button.grid(row=6, column=1)

        self.next_button = tk.Button(self, text="Next", command=self.next_observation)
        self.next_button.grid(row=6, column=2)

        self.fill_first_observation()

    def fill_first_observation(self):
        self.fill_observation(self.observaciones[self.current_index])

    def fill_observation(self, observation):
        self.label_var.set(observation[0])
        self.title_var.set("")
        self.description_var.set(observation[2])
        # self.description_entry.delete('1.0', tk.END)  # Limpiar contenido previo
        # self.description_entry.insert('1.0', observation[2])
        self.type_var.set("")
        self.priority_var.set("")
        self.status_var.set("")

    def fill(self):
        if (title := self.title_var.get()) and (type := self.type_var.get()) and (priority := self.priority_var.get()) and (status := self.status_var.get()):
            observation = list(self.observaciones[self.current_index])
            observation[1] = title
            observation[3] = type
            observation[4] = priority
            observation[5] = status
            self.observaciones[self.current_index] = tuple(observation)
            messagebox.showinfo("Info", "Saved")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "All fields must be filled.")

    def clear_fields(self):
        self.title_var.set("")
        self.type_var.set("")
        self.priority_var.set("")
        self.status_var.set("")

    def next_observation(self):
        self.current_index += 1
        if self.current_index < len(self.observaciones):
            self.fill_observation(self.observaciones[self.current_index])
        else:
            self.save_to_csv()
            messagebox.showinfo("Info", "All observations filled and saved to CSV.")
            self.destroy()

    def save_to_csv(self):
        csv_folder = "csv_files"
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)
        csv_filename = "observaciones_filled.csv"
        csv_path = os.path.join(csv_folder, csv_filename)

        with open(csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Label", "Title", "Description", "Type", "Priority", "Status"])
            writer.writerows(self.observaciones)

if __name__ == "__main__":
    from package.pdf_operations import extract_text, identify_observations
    texto_extraido = extract_text("20.09.21_Minuta_Observaciones_Etapa_1.1_complementaria.pdf")
    observaciones = identify_observations(texto_extraido)
    app = ObservationsForm(observaciones)
    app.mainloop()
