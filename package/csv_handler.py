import os
import csv

class CSVHandler:
    def __init__(self, csv_folder, csv_filename):
        self.csv_folder = csv_folder
        self.csv_filename = csv_filename
        self.csv_path = os.path.join(self.csv_folder, self.csv_filename)

    def read_options_from_csv(self, csv_file_path):
        """
        Lee las opciones desde un archivo CSV y devuelve una lista con ellas.
        Asume que cada opción está en su propia fila en la primera columna.
        """
        if not os.path.exists(csv_file_path):
            return []

        options = []
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar el encabezado
            options = [row[0] for row in reader if row]  # Asegúrate de que la fila no esté vacía
        return options

    def save_observations_to_csv(self, observations):
        """
        Guarda las observaciones en un archivo CSV.
        """
        # Crear el directorio si no existe
        if not os.path.exists(self.csv_folder):
            os.makedirs(self.csv_folder)

        # Comprobar si el archivo CSV existe
        if os.path.exists(self.csv_path):
            with open(self.csv_path, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                existing_labels = [row[0] for row in reader if row]  # Lista de todos los labels existentes
                if existing_labels:
                    last_label = max(map(int, existing_labels[1:]))  # Ignorar el encabezado y encontrar el último label
                else:
                    last_label = 0
        else:
            last_label = 0

        # Actualizar los labels de las observaciones con los nuevos valores
        for i, observation in enumerate(observations):
            observations[i] = (str(last_label + i + 1),) + observation[1:]

        # Guardar las observaciones en el archivo CSV
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(observations)