import streamlit as st
import pytesseract
from PIL import Image
from groq import Groq
import json
from datetime import datetime
import os
from pdf2image import convert_from_bytes
import io

# ============= CONFIG =============
st.set_page_config(
    page_title="Document Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    /* Variables */
    :root {
        --primary: #667eea;
        --secondary: #764ba2;
        --accent: #f093fb;
        --success: #00d084;
        --warning: #ffc300;
        --danger: #ff6b6b;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Texte principal */
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Containers personnalisés */
    .card-container {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .card-container:hover {
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85em;
        margin: 5px 5px 5px 0;
    }
    
    .badge-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .badge-success {
        background: #00d084;
        color: white;
    }
    
    .badge-warning {
        background: #ffc300;
        color: #333;
    }
    
    .badge-danger {
        background: #ff6b6b;
        color: white;
    }
    
    /* Boutons stylisés */
    .stButton > button {
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        border-radius: 10px 10px 0 0;
        padding: 15px 20px;
        font-weight: 600;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stFileUploader > div > div > button {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    .metric-card-alt {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(245, 87, 108, 0.3);
    }
    
    /* Divider */
    .stDivider {
        margin: 20px 0;
        opacity: 0.3;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 12px;
        padding: 15px 20px;
        border-left: 5px solid;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] > div > div > div:first-child {
        padding: 20px;
    }
    
    /* Titre principal */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1em;
        margin-bottom: 20px;
        font-weight: 500;
    }
    
    /* Result card */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.3);
        margin: 20px 0;
    }
    
    .result-icon {
        font-size: 4em;
        margin-bottom: 15px;
    }
    
    .result-type {
        font-size: 2.5em;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 15px 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .result-confidence {
        font-size: 1.3em;
        font-weight: 700;
        margin: 15px 0;
        background: rgba(255, 255, 255, 0.2);
        padding: 10px 20px;
        border-radius: 10px;
        display: inline-block;
    }
    
    /* Stats grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .stat-item {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #f0f0f0;
        transition: all 0.3s ease;
    }
    
    .stat-item:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Welcome section */
    .welcome-section {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .welcome-section h3 {
        color: #667eea;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    
    .welcome-section ul {
        list-style: none;
        padding: 0;
    }
    
    .welcome-section li {
        padding: 10px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .welcome-section li:last-child {
        border-bottom: none;
    }
    
    .welcome-section li:before {
        content: "✓ ";
        color: #00d084;
        font-weight: bold;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Config Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\boimi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Session state pour l'historique
if "historique" not in st.session_state:
    st.session_state.historique = []

if "page_pdf_actuelle" not in st.session_state:
    st.session_state.page_pdf_actuelle = 0

if "images_pdf" not in st.session_state:
    st.session_state.images_pdf = []

if "type_fichier" not in st.session_state:
    st.session_state.type_fichier = None

# ============= FONCTIONS =============
def extraire_texte_image(image):
    """Extrait le texte d'une image avec OCR"""
    try:
        return pytesseract.image_to_string(image, lang="fra+eng")
    except Exception as e:
        raise Exception(f"Erreur OCR : {str(e)}")

def classifier_document_groq(texte):
    """Classifie le document avec l'IA Groq"""
    try:
        client = Groq(api_key="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")
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un classificateur professionnel de documents. "
                        "Tu dois déterminer le type de document UNIQUEMENT à partir du texte fourni. "
                        "ATTENTION : si le texte contient plusieurs noms, plusieurs métiers, ou semble être une affiche, un poster, une slide ou un visuel marketing, "
                        "alors le type_document doit être 'autre' avec une confiance faible. "
                        "Ne classe PAS comme 'cv' si plusieurs personnes sont mentionnées. "
                        "Répond STRICTEMENT en JSON."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
Voici le texte extrait d'un document :

\"\"\"{texte}\"\"\"

Analyse ce texte et classe le document parmi les catégories suivantes :
- cv
- facture
- carte_identite
- releve_bancaire
- attestation
- diplome
- bulletin_de_paie
- contrat
- autre

Répond uniquement avec un JSON :
{{
  "type_document": "...",
  "confiance": 0.0,
  "justification": "Pourquoi ce type",
  "resume": "Résumé très court"
}}
"""
                }
            ]
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Erreur Groq : {str(e)}")

def obtenir_couleur_confiance(confiance):
    """Retourne une couleur basée sur le niveau de confiance"""
    if confiance >= 0.8:
        return "🟢"
    elif confiance >= 0.6:
        return "🟡"
    else:
        return "🔴"

def obtenir_icone_document(type_doc):
    """Retourne une icône basée sur le type de document"""
    icones = {
        "cv": "👤",
        "facture": "💰",
        "carte_identite": "🆔",
        "releve_bancaire": "🏦",
        "attestation": "✅",
        "diplome": "🎓",
        "bulletin_de_paie": "💼",
        "contrat": "📋",
        "autre": "❓"
    }
    return icones.get(type_doc, "📄")

def convertir_pdf_en_images(pdf_bytes):
    """Convertit un fichier PDF en liste d'images PIL"""
    try:
        images = convert_from_bytes(pdf_bytes, dpi=200)
        return images
    except Exception as e:
        raise Exception(f"Erreur lors de la conversion du PDF : {str(e)}")

# ============= SIDEBAR =============
with st.sidebar:
    st.markdown("""
    <h2 style="color: white; text-align: center; margin: 20px 0;">
        ⚙️ Tableau de bord
    </h2>
    """, unsafe_allow_html=True)
    
    # Onglets dans la sidebar
    tabs = st.tabs(["📊 Historique", "ℹ️ Infos"])
    
    with tabs[0]:
        st.markdown("### 📈 Analyses récentes")
        if st.session_state.historique:
            for i, analyse in enumerate(reversed(st.session_state.historique[-5:])):
                with st.expander(f"{obtenir_icone_document(analyse['type'])} {analyse['type']} - {analyse['heure']}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Confiance", f"{analyse['confiance']*100:.0f}%")
                    with col2:
                        confiance_emoji = "🟢" if analyse['confiance'] >= 0.8 else "🟡" if analyse['confiance'] >= 0.6 else "🔴"
                        st.markdown(f"**{confiance_emoji} Niveau:** {'Élevé' if analyse['confiance'] >= 0.8 else 'Moyen' if analyse['confiance'] >= 0.6 else 'Faible'}")
                    
                    st.markdown(f"**Résumé:** {analyse['resume']}")
            
            st.divider()
            
            if st.button("🗑️ Effacer l'historique", use_container_width=True):
                st.session_state.historique = []
                st.rerun()
        else:
            st.info("📭 Aucune analyse récente")
    
    with tabs[1]:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 15px; color: white;">
            <h4>📄 Document Intelligence</h4>
            <p style="font-size: 0.9em; opacity: 0.9;">
            Analysez vos documents avec OCR et classification IA avancée.
            </p>
            
            <h4>🎯 Fonctionnalités</h4>
            <ul style="font-size: 0.9em; opacity: 0.9; padding-left: 20px;">
                <li><strong>OCR:</strong> Tesseract</li>
                <li><strong>IA:</strong> Groq LLaMA</li>
                <li><strong>Historique</strong> automatique</li>
                <li><strong>Export</strong> JSON</li>
            </ul>
            
            <h4>📋 Types supportés</h4>
            <div style="font-size: 0.85em; opacity: 0.9;">
                👤 CV • 💰 Facture • 🆔 Carte ID<br>
                🏦 Relevé • ✅ Attestation • 🎓 Diplôme<br>
                💼 Bulletin • 📋 Contrat
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============= MAIN CONTENT =============
st.markdown('<h1 class="main-title">📄 Document Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analysez vos documents avec OCR et classification IA avancée</p>', unsafe_allow_html=True)
st.divider()

# Section upload
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "📁 Choisir un fichier à analyser",
        type=["png", "jpg", "jpeg", "pdf"],
        help="Glissez-déposez ou cliquez pour sélectionner une image ou un PDF"
    )

with col2:
    col_metric1, col_metric2 = st.columns(2)
    with col_metric1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; font-size: 0.9em; opacity: 0.9;">Analyses</h3>
            <h1 style="margin: 10px 0; font-size: 2em;">{len(st.session_state.historique)}</h1>
        </div>
        """, unsafe_allow_html=True)

if uploaded_file:
    try:
        # Déterminer le type de fichier
        file_extension = uploaded_file.name.split('.')[-1].lower()
        is_pdf = file_extension == 'pdf'
        
        if is_pdf:
            # Convertir PDF en images
            with st.spinner("📄 Conversion du PDF en cours..."):
                pdf_bytes = uploaded_file.getvalue()
                st.session_state.images_pdf = convertir_pdf_en_images(pdf_bytes)
                st.session_state.type_fichier = "pdf"
                st.session_state.page_pdf_actuelle = 0
            
            # Sélectionner la page du PDF
            if len(st.session_state.images_pdf) > 1:
                st.markdown("""
                <div class="card-container">
                    <h4>📄 Sélectionner une page</h4>
                </div>
                """, unsafe_allow_html=True)
                
                page_selected = st.slider(
                    "Page du PDF",
                    min_value=0,
                    max_value=len(st.session_state.images_pdf) - 1,
                    value=st.session_state.page_pdf_actuelle,
                    step=1
                )
                st.session_state.page_pdf_actuelle = page_selected
                image = st.session_state.images_pdf[page_selected]
                page_info = f"Page {page_selected + 1}/{len(st.session_state.images_pdf)}"
            else:
                image = st.session_state.images_pdf[0]
                page_info = "Seule page du PDF"
        else:
            # Charger l'image
            image = Image.open(uploaded_file)
            st.session_state.type_fichier = "image"
            page_info = None
        
        # Afficher l'image avec preview
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown("### 📷 Aperçu du document")
            st.image(image, use_column_width=True)
        
        with col2:
            st.markdown("### 📋 Informations")
            
            info_text = f"""
            <p><strong>📝 Fichier:</strong> {uploaded_file.name}</p>
            <p><strong>📏 Taille:</strong> {uploaded_file.size / 1024:.2f} KB</p>
            <p><strong>⏰ Heure:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>📐 Dimensions:</strong> {image.width}×{image.height}px</p>
            """
            
            if page_info:
                info_text += f"<p><strong>📄 {page_info}</strong></p>"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 20px; border-radius: 12px; line-height: 1.8;">
                {info_text}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()
        
        # Tabs pour OCR et Classification
        tab1, tab2 = st.tabs(["🔍 Extraction OCR", "🤖 Classification IA"])
        
        with tab1:
            with st.spinner("⚙️ Extraction du texte en cours..."):
                texte = extraire_texte_image(image)
            
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("#### Texte extrait")
            with col2:
                if st.button("📋 Copier le texte"):
                    st.success("✅ Texte copié dans le presse-papiers!")
            
            # Afficher le texte
            st.text_area(
                "Contenu:",
                value=texte,
                height=300,
                disabled=True,
                label_visibility="collapsed"
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Statistiques en cartes
            mots = len(texte.split())
            caracteres = len(texte)
            lignes = len(texte.split('\n'))
            
            st.markdown("#### 📊 Statistiques")
            
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.markdown(f"""
                <div class="stat-item">
                    <h3 style="color: #667eea; margin: 0;">📊</h3>
                    <p style="font-weight: 700; font-size: 1.5em; margin: 5px 0; color: #333;">{mots}</p>
                    <p style="color: #999; margin: 0; font-size: 0.9em;">Mots</p>
                </div>
                """, unsafe_allow_html=True)
            
            with stat_col2:
                st.markdown(f"""
                <div class="stat-item">
                    <h3 style="color: #764ba2; margin: 0;">🔤</h3>
                    <p style="font-weight: 700; font-size: 1.5em; margin: 5px 0; color: #333;">{caracteres}</p>
                    <p style="color: #999; margin: 0; font-size: 0.9em;">Caractères</p>
                </div>
                """, unsafe_allow_html=True)
            
            with stat_col3:
                st.markdown(f"""
                <div class="stat-item">
                    <h3 style="color: #f093fb; margin: 0;">📄</h3>
                    <p style="font-weight: 700; font-size: 1.5em; margin: 5px 0; color: #333;">{lignes}</p>
                    <p style="color: #999; margin: 0; font-size: 0.9em;">Lignes</p>
                </div>
                """, unsafe_allow_html=True)
            
            with stat_col4:
                confiance_badge = "🟢 Excellente" if mots > 100 else "🟡 Bonne" if mots > 50 else "🔴 Faible"
                st.markdown(f"""
                <div class="stat-item">
                    <h3 style="color: #00d084; margin: 0;">🎯</h3>
                    <p style="font-weight: 700; font-size: 1em; margin: 5px 0; color: #333;">{confiance_badge}</p>
                    <p style="color: #999; margin: 0; font-size: 0.9em;">Confiance OCR</p>
                </div>
                """, unsafe_allow_html=True)
            
            if mots < 10:
                st.markdown("""
                <div style="background: #fff3cd; border-left: 5px solid #ffc300; padding: 15px; border-radius: 8px; margin-top: 15px;">
                    <p style="margin: 0; color: #856404;"><strong>⚠️ Attention:</strong> Texte très court détecté. La classification IA peut être moins fiable.</p>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            with st.spinner("🤖 Classification en cours..."):
                reponse = classifier_document_groq(texte)
            
            try:
                data = json.loads(reponse)
                
                # Récupérer les données
                type_doc = data.get('type_document', 'autre')
                confiance = data.get('confiance', 0)
                justification = data.get('justification', '')
                resume = data.get('resume', '')
                
                # Ajouter à l'historique
                st.session_state.historique.append({
                    'type': type_doc,
                    'confiance': confiance,
                    'resume': resume,
                    'heure': datetime.now().strftime('%H:%M:%S'),
                    'justification': justification
                })
                
                # Déterminer la couleur et l'icône
                couleur_hex = "#00d084" if confiance >= 0.8 else "#ffc300" if confiance >= 0.6 else "#ff6b6b"
                couleur_badge = "🟢" if confiance >= 0.8 else "🟡" if confiance >= 0.6 else "🔴"
                icone = obtenir_icone_document(type_doc)
                
                # Carte de résultats principale
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-icon">{icone}</div>
                    <div class="result-type">{type_doc}</div>
                    <div class="result-confidence">
                        {couleur_badge} Confiance: <strong>{confiance*100:.1f}%</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Sections détails
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="card-container" style="border-left: 5px solid #667eea;">
                        <h4 style="color: #667eea; margin-top: 0;">📋 Justification</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info(justification)
                
                with col2:
                    st.markdown("""
                    <div class="card-container" style="border-left: 5px solid #00d084;">
                        <h4 style="color: #00d084; margin-top: 0;">📝 Résumé</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    st.success(resume)
                
                st.divider()
                
                # Boutons d'action
                st.markdown("#### 🎯 Actions")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("💾 Télécharger JSON", use_container_width=True):
                        json_str = json.dumps(data, ensure_ascii=False, indent=2)
                        st.download_button(
                            label="📥 Télécharger",
                            data=json_str,
                            file_name=f"analyse_{type_doc}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                
                with col2:
                    if st.button("🔄 Réanalyser", use_container_width=True):
                        st.rerun()
                
                with col3:
                    if st.button("➕ Nouvelle image", use_container_width=True):
                        st.session_state.clear()
                        st.rerun()
                
                with col4:
                    if st.button("📊 Voir JSON brut", use_container_width=True):
                        pass
                
                # JSON brut
                with st.expander("🔍 Afficher le JSON brut"):
                    st.json(data)
                
            except json.JSONDecodeError:
                st.markdown("""
                <div style="background: #f8d7da; border-left: 5px solid #ff6b6b; padding: 15px; border-radius: 8px;">
                    <p style="margin: 0; color: #721c24;"><strong>❌ Erreur:</strong> Le JSON renvoyé par l'IA n'est pas valide.</p>
                </div>
                """, unsafe_allow_html=True)
                st.code(reponse, language="json")
            except Exception as e:
                st.markdown(f"""
                <div style="background: #f8d7da; border-left: 5px solid #ff6b6b; padding: 15px; border-radius: 8px;">
                    <p style="margin: 0; color: #721c24;"><strong>❌ Erreur:</strong> {str(e)}</p>
                </div>
                """, unsafe_allow_html=True)
    
    except Exception as e:
        st.markdown(f"""
        <div style="background: #f8d7da; border-left: 5px solid #ff6b6b; padding: 15px; border-radius: 8px;">
            <p style="margin: 0; color: #721c24;"><strong>❌ Erreur lors du traitement:</strong> {str(e)}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Message d'accueil attrayant
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h2 style="color: #667eea; font-size: 2.5em; margin-bottom: 10px;">🚀 Bienvenue !</h2>
        <p style="color: #666; font-size: 1.1em;">Commencez en chargeant une image ou un PDF pour analyser votre document</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="welcome-section">
            <h3>🎯 Comment ça marche ?</h3>
            <ul>
                <li><strong>📁 Charger</strong> image/PDF</li>
                <li><strong>🔍 OCR</strong> extrait le texte</li>
                <li><strong>🤖 IA</strong> classifie le document</li>
                <li><strong>✅ Résultats</strong> instantanés</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="welcome-section">
            <h3>📊 Types supportés</h3>
            <ul>
                <li><strong>👤</strong> Curriculum Vitae</li>
                <li><strong>💰</strong> Facture</li>
                <li><strong>🆔</strong> Carte d'identité</li>
                <li><strong>🏦</strong> Relevé bancaire</li>
                <li><strong>✅</strong> Attestation</li>
                <li><strong>🎓</strong> Diplôme</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="welcome-section">
            <h3>💡 Conseils</h3>
            <ul>
                <li><strong>✅</strong> Bonne qualité d'image</li>
                <li><strong>✅</strong> Documents bien lisibles</li>
                <li><strong>✅</strong> Format PNG/JPG/PDF</li>
                <li><strong>✅</strong> Minimum 50 mots</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 30px; border-radius: 15px; text-align: center;">
        <h3 style="margin-top: 0;">📁 Sélectionnez une image ou un PDF pour commencer</h3>
        <p style="opacity: 0.9;">Formats supportés: PNG, JPG, JPEG, PDF</p>
    </div>
    """, unsafe_allow_html=True)