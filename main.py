from package.export import export_text_to_csv
from package.pdf_operations import extract_text, identify_observations

texto_extraido = extract_text("20.09.21_Minuta_Observaciones_Etapa_1.1_complementaria.pdf")
observaciones = identify_observations(texto_extraido)
export_text_to_csv(observaciones)