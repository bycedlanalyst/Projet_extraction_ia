import pytesseract
from PIL import Image

# Chemin vers Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\boimi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Test simple : afficher la version
print("Version Tesseract détectée par Python :")
print(pytesseract.get_tesseract_version())
