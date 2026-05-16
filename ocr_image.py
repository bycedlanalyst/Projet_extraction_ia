import pytesseract
from PIL import Image

# 1. Chemin vers Tesseract 
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\boimi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# 2. Fonction OCR
def extraire_texte_image(chemin_image):
    image = Image.open(chemin_image)
    texte = pytesseract.image_to_string(image, lang="fra+eng")  # français + anglais
    return texte

# 3. Test avec une image
chemin = r"C:\Users\boimi\Downloads\image_test.png"  # remplace par ton image
texte = extraire_texte_image(chemin)

print("=== TEXTE OCR EXTRAIT ===")
print(texte)
