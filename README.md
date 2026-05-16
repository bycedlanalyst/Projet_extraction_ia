# 📄 Document Intelligence - Extraction IA

Un projet d'**extraction et analyse intelligente de documents** utilisant **OCR (Tesseract)** et **IA générative (Groq - LLaMA)**.

## 🎯 Objectif

Extraire automatiquement le texte des images/documents et les analyser intelligemment grâce à des modèles d'IA pour obtenir des insights et résumés pertinents.

---

## 📋 Fonctionnalités

✅ **Extraction OCR** - Reconnaissance optique de caractères (français + anglais)  
✅ **Analyse IA** - Utilise le modèle LLaMA 3.1 via l'API Groq  
✅ **Interface Web** - Application Streamlit moderne et responsive  
✅ **Support multiformat** - Images (PNG, JPG, etc.) et PDF  
✅ **Pipeline complet** - OCR → Texte → Analyse intelligente  

---

## 🛠️ Technologies Utilisées

| Technologie | Description |
|------------|------------|
| **Tesseract-OCR** | Extraction de texte depuis les images |
| **Groq API** | Modèles d'IA génératives (LLaMA 3.1-8b) |
| **Streamlit** | Framework pour l'interface web |
| **Python 3.10+** | Langage principal |
| **PIL/Pillow** | Traitement d'images |
| **pdf2image** | Conversion PDF en images |

---

## 📁 Structure du Projet

```
projet_extration_ia/
├── app.py                 # 🌐 Application Streamlit principale
├── ocr_groq.py           # 🔗 Pipeline complet (OCR + Groq)
├── ocr_image.py          # 📷 Extraction OCR simple
├── models_list.py        # 📊 Lister les modèles disponibles
├── ocr_test.py           # 🧪 Test Tesseract
├── test_groq.py          # 🧪 Test Groq API
├── test_tesseract.py     # 🧪 Vérification Tesseract
└── README.md             # 📖 Ce fichier
```

### 📝 Description des Fichiers

| Fichier | Rôle |
|---------|------|
| **app.py** | Application web Streamlit avec interface riche, gestion des fichiers et historique |
| **ocr_groq.py** | Pipeline complet : lit une image → OCR → Envoie à Groq → Retourne l'analyse |
| **ocr_image.py** | Fonction utilitaire pour extraire du texte d'une image |
| **models_list.py** | Affiche la liste des modèles disponibles via l'API Groq |
| **ocr_test.py** | Test simple pour vérifier que Tesseract fonctionne |
| **test_groq.py** | Test de la connexion et fonctionnement de l'API Groq |
| **test_tesseract.py** | Vérifie la version et la disponibilité de Tesseract |

---

## 📸 Captures d'écran

### Interface Principale
![Interface Streamlit](./interface_streamlit.png)
*Page d'accueil avec zone de téléchargement et instructions*

### Tableau de Bord avec Résultats
![Dashboard Streamlit](./Dashboard_streamlit.png)
*Affichage des résultats d'analyse avec confiance et résumé*

---

## 🚀 Installation et Configuration

### 1️⃣ Prérequis

- **Python 3.10+** installé
- **Tesseract-OCR** installé et configuré
- **Clé API Groq** (gratuit sur https://console.groq.com)

### 2️⃣ Installation de Tesseract

#### Sur Windows
Télécharger l'installeur depuis : https://github.com/UB-Mannheim/tesseract/wiki

```powershell
# Après installation, le chemin par défaut est :
C:\Users\boimi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe
```

#### Sur Linux/Mac
```bash
# Linux
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract
```

### 3️⃣ Installation des dépendances Python

```bash
pip install streamlit pytesseract pillow groq pdf2image
```

Ou via `requirements.txt` (si disponible) :
```bash
pip install -r requirements.txt
```

### 4️⃣ Configuration de l'API Groq

1. Créer un compte sur https://console.groq.com
2. Générer une clé API
3. Ajouter la clé dans vos fichiers Python ou variables d'environnement :

```python
from groq import Groq

client = Groq(api_key="votre_clé_api_groq")
```

---

## 💻 Utilisation

### Option 1 : Interface Web (Recommandé)

```bash
streamlit run app.py
```

Ouvre automatiquement http://localhost:8501

**Fonctionnalités disponibles :**
- Upload d'images ou PDF
- Affichage du texte extrait
- Analyse intelligente avec options personnalisées
- Historique et téléchargement des résultats

### Option 2 : Pipeline Python Simple

```bash
python ocr_groq.py
```

Modifiez le chemin de l'image dans le code :
```python
chemin = r"C:\Users\boimi\Downloads\image_test.png"
```

### Option 3 : Scripts Utilitaires

```bash
# Extraire du texte d'une image
python ocr_image.py

# Lister les modèles disponibles
python models_list.py

# Tester Tesseract
python test_tesseract.py

# Tester Groq
python test_groq.py
```

---

## 🔧 Fonctions Principales

### Extraction OCR
```python
from ocr_image import extraire_texte_image

texte = extraire_texte_image("chemin/vers/image.png")
print(texte)
```

### Analyse avec Groq
```python
from ocr_groq import analyser_texte_groq

resultat = analyser_texte_groq(texte)
print(resultat)
```

---

## 📊 Modèles IA Disponibles

Le projet utilise principalement :
- **llama-3.1-8b-instant** - Modèle rapide et polyvalent
- Autres modèles disponibles via Groq : lister avec `python models_list.py`

---

## 🐛 Dépannage

| Problème | Solution |
|----------|----------|
| `TesseractNotFoundError` | Installer Tesseract et configurer le chemin dans le code |
| `APIError` de Groq | Vérifier la clé API et la connexion internet |
| Texte OCR vide | Vérifier la qualité de l'image (contraste, résolution) |
| Permission denied | Vérifier les droits d'accès aux fichiers |

---

## 📈 Cas d'Utilisation

✨ **Factures & Reçus** - Extraction automatique de données  
✨ **Documents officiels** - Numérisation et archivage  
✨ **Contrats** - Analyse et extraction de clauses clés  
✨ **Livres & Articles** - Numérisation et recherche  
✨ **Rapports** - Résumés et analyses automatiques  

---

## 🔐 Sécurité & Bonnes Pratiques

⚠️ **Ne commettez jamais votre clé API Groq** dans Git  
⚠️ **Utilisez des variables d'environnement** pour les clés sensibles  
⚠️ **Validez les données** avant de les traiter  

Exemple avec variables d'environnement :
```python
import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
```

---

## 📝 Limitations Actuelles

- Support des langues : français et anglais (configurable dans le code)
- Dépendance à la qualité de l'image pour l'OCR
- Limitations de l'API Groq (rate limits, contexte max)
- Clés API codées en dur dans certains fichiers (à corriger)

---

## 🚀 Améliorations Futures

🔜 **Authentification** - Gestion des utilisateurs  
🔜 **Base de données** - Stockage de l'historique  
🔜 **Support multilingues** - Plus de langues  
🔜 **Export avancé** - CSV, Excel, PDF  
🔜 **Traitement par batch** - Traiter plusieurs fichiers  
🔜 **Webhooks** - Intégrations externes  

---

## 📞 Support & Contact

Pour toute question ou bug report, consultez les logs ou ouvrez une issue.

---

## 📄 Licence

Projet développé à des fins éducatives et professionnelles.

---

**Dernière mise à jour** : Mai 2026  
**Créateur** : Boimi  
**Status** : 🟢 Actif
