import pdfplumber

def extraer_texto(filepath):
    data = ""
    with pdfplumber.open(filepath) as pdf:
        for p_num,pagina in enumerate (pdf.pages,1):
            data += pagina.extract_text()
            print(data)
    return data



def write_text_to_txt(text, txt_path):
    with open(txt_path, 'w') as file:
        file.write(text)


txt_path = "file_txt.txt"
texto_extraido = extraer_texto("20.09.21_Minuta_Observaciones_Etapa_1.1_complementaria.pdf")
write_text_to_txt(texto_extraido, txt_path)