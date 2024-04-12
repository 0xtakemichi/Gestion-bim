import pdfplumber
import re

def extraer_texto(file_pdf):
    text = ""
    with pdfplumber.open(file_pdf) as pdf:
        for p_num,pagina in enumerate (pdf.pages,1):
            text += pagina.extract_text()
    return text

def identificar_observaciones(texto):
    # Patrón de expresión regular para identificar enumeraciones seguidas de texto
    patron = r'(\b\d+\.\s)(.*?)(?=\b\d+\.\s|\Z)'
    # Buscar todas las coincidencias en el texto
    coincidencias = re.findall(patron, texto, re.DOTALL)
    
    # Guardar las enumeraciones y su texto asociado en una lista de tuplas
    observaciones = [(match[0].strip(), match[1].strip()) for match in coincidencias]
    
    return observaciones

def write_text_to_txt(observaciones, txt_path):
    with open(txt_path, 'w') as file:
        for enum, texto in observaciones:
            file.write(f"{enum} {texto}\n")
        #file.write(observaciones)


txt_observaciones = "observaciones.txt"
texto_extraido = extraer_texto("20.09.21_Minuta_Observaciones_Etapa_1.1_complementaria.pdf")
observaciones = identificar_observaciones(texto_extraido)
write_text_to_txt(observaciones, txt_observaciones)