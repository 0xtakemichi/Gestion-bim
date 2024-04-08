import pdfplumber

# Se define funcion Extraer texto y se le entrega un argumento
def Extraer_Texto(filepath):
    # with se utiliza para trabajar con un recursos que necesitan cer liberados o cerrados
    # A la función open() del módulo pdfplumber, que se utiliza para abrir un archivo PDF. 
    with pdfplumber.open(filepath) as pdf:
        # Bucle que recorre las paginas
        for p_num,pagina in enumerate (pdf.pages,1):
            # Se realiza la extraccion de datos de la pagina actual
            print("->Pagina:", p_num,"<-")
            data = pagina.extract_text()
            print(data)
            


Extraer_Texto("20.09.21_Minuta_Observaciones_Etapa_1.1_complementaria.pdf")