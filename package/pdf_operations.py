from tkinter import filedialog
import re
import pdfplumber

def select_pdf_file():
    filetypes = [('PDF files', '.pdf'), ('All files', '.*')]
    filepath = filedialog.askopenfilename(title='Open a file', filetypes=filetypes)
    return filepath

def extract_text(file_pdf):
    text = ""
    with pdfplumber.open(file_pdf) as pdf:
        for p_num,pagina in enumerate (pdf.pages,1):
            text += pagina.extract_text()
    return text

def identify_observations(texto):
    # Patrón de expresión regular para identificar enumeraciones seguidas de texto
    patron = r'(\b\d+\.\s)(.*?)(?=\b\d+\.\s|\Z)'
    # Buscar todas las coincidencias en el texto
    coincidencias = re.findall(patron, texto, re.DOTALL)
    # Guardar las enumeraciones y su texto asociado en una lista de tuplas
    observaciones = [(match[0].strip(),"", match[1].strip(),"","","") for match in coincidencias]
    return observaciones

# filepdf = select_pdf_file()
# text = extract_text(filepdf)
# observaciones = identify_observations(text)
# print(observaciones)