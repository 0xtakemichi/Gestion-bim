from tkinter import filedialog
import re
import pdfplumber

def select_pdf_files():
    filetypes = [('PDF files', '*.pdf'), ('All files', '*.*')]
    filepath = filedialog.askopenfilenames(title='Open a file', filetypes=filetypes)
    return filepath

def extract_texts(files):
    all_texts = []  # Lista para almacenar el texto de todos los archivos
    for file in files:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # Asegurarse de que la página contenga texto
                    page_text = re.sub(r'\n', ' ', page_text) # Eliminar saltos de linea
                    text += page_text
        all_texts.append(text)  # Agregar el texto de este archivo a la lista
    return all_texts

def identify_observations(textos):
    observaciones = []
    patron = r'(\b\d+\.\s)(.*?)(?=\b\d+\.\s|\Z)'
    for texto in textos:  # Procesar cada texto individualmente
        coincidencias = re.findall(patron, texto, re.DOTALL)
        for match in coincidencias:
            observaciones.append((match[0].strip(), "", match[1].strip(), "", "", "", "", "", ""))
    return observaciones