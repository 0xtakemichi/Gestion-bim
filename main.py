def main():
    from package.pdfs_operations import select_pdf_files, extract_texts, identify_observations
    from package.observations_form import ObservationsForm
    
    filepdf = select_pdf_files()
    texto_extraido = extract_texts(filepdf)
    observaciones = identify_observations(texto_extraido)
    app = ObservationsForm(observaciones)
    app.mainloop()

if __name__ == "__main__":
    main()