import PyPDF2
import csv
import re

def count_pdf_pages():
    """Count the number of pages in the document"""
    try:
        with open('cartillamed.pdf', 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if reader.is_encrypted:
                reader.decrypt('')
            
            page_count = len(reader.pages)
            print(page_count)

    except Exception as e:
        print(f"Ocurrio el error {e} al intentar leer el pdf")

def select_pages(start, end):
    """Extract text from the selected range of pages"""
    try:
        with open('cartillamed.pdf', 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if reader.is_encrypted:
                reader.decrypt('')  # Si el PDF está encriptado, intenta desencriptarlo (puede que necesites una contraseña)
        
            all_text = ""
            for n in range(start, end + 1):
                page = reader.pages[n]
                text = page.extract_text()
                all_text += text + "\n"  # Agregar salto de línea entre páginas
            
            return all_text
        
    except Exception as e:
        print(f"Ocurrió un error al procesar el PDF: {e}")
        return None  # última línea agregada

def extract_information(text):
    """Extract information and return a list of dictionaries"""
    pattern = re.compile(r'(.+?)\n(.+?)\nTel\. (.+?)(?: \((?:011|Solo WhatsApp)\))?\n([\w\.-]+@[\w\.-]+)')
    matches = pattern.findall(text)
    
    data = []
    for match in matches:
        professional = match[0]
        address = match[1]
        phone = match[2]
        email = match[3]
        data.append({
            'Profesional': professional,
            'Direccion': address,
            'Telefono': phone,
            'Mail': email
        })
    
    return data

def save_to_csv(data, filename='cartilla_tabla_rango.csv'):
    """Saves the extracted data to a CSV file"""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Profesional', 'Direccion', 'Telefono', 'Mail'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    start_page = int(input("Ingresa la página de inicio: "))
    end_page = int(input("Ingresa la página de fin: "))
    text = select_pages(start_page, end_page)
    if text:
        data = extract_information(text)
        save_to_csv(data)
