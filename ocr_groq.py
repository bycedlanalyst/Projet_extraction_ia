import pytesseract
from PIL import Image
from groq import Groq

# 1. Chemin vers Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\boimi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# 2. Fonction OCR
def extraire_texte_image(chemin_image):
    image = Image.open(chemin_image)
    texte = pytesseract.image_to_string(image, lang="fra+eng")
    return texte

# 3. Fonction Groq
def analyser_texte_groq(texte):
    client = Groq(api_key="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")

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Tu es un expert en analyse de documents."},
            {"role": "user", "content": f"Analyse ce texte :\n\n{texte}"}
        ]
    )

    # 🔥 Correction ici
    return completion.choices[0].message.content

# 4. Pipeline complet
chemin = r"C:\Users\boimi\Downloads\image_test.png"
texte_ocr = extraire_texte_image(chemin)

print("=== TEXTE OCR ===")
print(texte_ocr)

print("\n=== ANALYSE GROQ ===")
analyse = analyser_texte_groq(texte_ocr)
print(analyse)
