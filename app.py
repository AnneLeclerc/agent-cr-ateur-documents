import streamlit as st
import ollama
from docx import Document
from pptx import Presentation
from pptx.util import Inches, Pt
from fpdf import FPDF
import pandas as pd
import io

# === CONFIGURATION DE LA PAGE ===
st.set_page_config(page_title="Agent Créateur de Documents", layout="wide")
st.title("🤖 Agent Créateur de Documents IA")
st.caption("Décris ton sujet, choisis le format, et l'IA génère le fichier pour toi.")

# === CONFIGURATION OLLAMA ===
# On utilise le modèle que tu as déjà
MODEL_NAME = "qwen3.8:27b"

# === INTERFACE UTILISATEUR ===
col1, col2 = st.columns(2)
with col1:
    sujet = st.text_area("📝 Sur quel sujet veux-tu un document ?", height=100,
                         placeholder="Ex: Les avantages de l'énergie solaire pour les entreprises...")
with col2:
    format_fichier = st.selectbox("📂 Quel format de fichier ?",
                                  ["Word (.docx)", "PDF (.pdf)", "PowerPoint (.pptx)", "Excel (.xlsx)"])

bouton_generer = st.button("✨ Générer le document", type="primary")

# === LOGIQUE DE GÉNÉRATION ===
if bouton_generer and sujet:
    with st.spinner(" L'IA rédige le contenu... (cela peut prendre 1 à 2 minutes)"):
        try:
            # 1. Demander à l'IA de générer le contenu structuré
            # On lui demande du Markdown car c'est facile à convertir
            prompt = f"""Rédige un document complet et structuré sur le sujet suivant : "{sujet}".
            Utilise le format Markdown avec des titres (#), des sous-titres (##) et des listes à puces (-).
            Ne mets pas de code, juste le texte du document."""

            response = ollama.chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt}])
            contenu_ia = response['message']['content']

            st.success("✅ Contenu généré ! Création du fichier...")

            # 2. Créer le fichier selon le format choisi
            buffer = io.BytesIO()

            if format_fichier == "Word (.docx)":
                doc = Document()
                for ligne in contenu_ia.split('\n'):
                    if ligne.startswith('# '):
                        doc.add_heading(ligne.replace('# ', ''), level=1)
                    elif ligne.startswith('## '):
                        doc.add_heading(ligne.replace('## ', ''), level=2)
                    elif ligne.startswith('- '):
                        doc.add_paragraph(ligne.replace('- ', ''), style='List Bullet')
                    else:
                        doc.add_paragraph(ligne)
                doc.save(buffer)
                buffer.seek(0)
                st.download_button("⬇️ Télécharger le Word", buffer, file_name="document_ia.docx",
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

            elif format_fichier == "PDF (.pdf)":
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_font('DejaVu', '', 'C:/Windows/Fonts/arial.ttf', uni=True)  # Police standard Windows
                pdf.set_font('DejaVu', size=12)
                for ligne in contenu_ia.split('\n'):
                    if ligne.startswith('# '):
                        pdf.set_font('DejaVu', size=16, style='B')
                        pdf.cell(0, 10, ligne.replace('# ', ''), new_x="LMARGIN", new_y="NEXT")
                    elif ligne.startswith('## '):
                        pdf.set_font('DejaVu', size=14, style='B')
                        pdf.cell(0, 8, ligne.replace('## ', ''), new_x="LMARGIN", new_y="NEXT")
                    else:
                        pdf.set_font('DejaVu', size=12)
                        pdf.multi_cell(0, 5, ligne)
                    pdf.ln(2)
                pdf.output(dest='S').encode('latin-1')  # Astuce pour fpdf2
                # Version simplifiée pour éviter les erreurs d'encodage complexes
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font('DejaVu', '', 'C:/Windows/Fonts/arial.ttf', uni=True)
                pdf.set_font('DejaVu', size=12)
                # Nettoyage basique pour le PDF
                texte_propre = contenu_ia.replace('#', '').replace('*', '')
                pdf.multi_cell(0, 5, texte_propre)
                pdf_bytes = pdf.output()
                st.download_button("⬇️ Télécharger le PDF", pdf_bytes, file_name="document_ia.pdf",
                                   mime="application/pdf")

            elif format_fichier == "PowerPoint (.pptx)":
                prs = Presentation()
                slides = contenu_ia.split('\n\n')  # Séparer par blocs
                for bloc in slides:
                    if bloc.strip():
                        slide = prs.slides.add_slide(prs.slide_layouts[1])  # Layout Titre + Contenu
                        titre = slide.shapes.title
                        corps = slide.placeholders[1]
                        # Découpage simple titre/corps
                        lignes = bloc.split('\n')
                        titre.text = lignes[0].replace('# ', '') if lignes[0].startswith('#') else "Section"
                        corps.text = '\n'.join(lignes[1:]) if len(lignes) > 1 else ""
                prs.save(buffer)
                buffer.seek(0)
                st.download_button("️ Télécharger le PowerPoint", buffer, file_name="presentation_ia.pptx",
                                   mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")

            elif format_fichier == "Excel (.xlsx)":
                # Pour Excel, on demande à l'IA de faire un tableau
                prompt_excel = f"Transforme les informations sur '{sujet}' en un tableau structuré. Réponds UNIQUEMENT avec des lignes CSV (séparées par des points-virgules), sans titre, sans explication."
                response_excel = ollama.chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt_excel}])
                csv_text = response_excel['message']['content']

                # Conversion CSV -> Excel
                df = pd.read_csv(io.StringIO(csv_text), sep=';', header=None)
                df.to_excel(buffer, index=False, header=False)
                buffer.seek(0)
                st.download_button("⬇️ Télécharger l'Excel", buffer, file_name="donnees_ia.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")

elif bouton_generer and not sujet:
    st.warning("⚠️ Veuillez d'abord décrire le sujet de votre document.")
