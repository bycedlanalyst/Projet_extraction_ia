import pytesseract

# Chemin vers ton installation Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\boimi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Affiche la version pour vérifier que tout marche
print(pytesseract.get_tesseract_version())
