import streamlit as st
from utils.extract import extract_text_from_pdf, extract_text_from_docx
from utils.ai import reformulate_text, ask_question
from utils.export import export_to_pdf
from utils.tts import text_to_speech
from utils.rag import build_index, is_question_relevant
import tempfile

st.set_page_config(page_title="Assistant Dyslexie", layout="wide")
st.title("Assistant IA pour élèves dyslexiques")

# Session states pour conserver les résultats
if "reformulated_text" not in st.session_state:
    st.session_state.reformulated_text = ""
if "rag_chunks" not in st.session_state:
    st.session_state.rag_chunks = []
if "rag_embeddings" not in st.session_state:
    st.session_state.rag_embeddings = []

# Upload du fichier
uploaded_file = st.file_uploader("Charge un fichier PDF ou Word", type=["pdf", "docx"])

if uploaded_file:
    # Extraction du texte
    if uploaded_file.type == "application/pdf":
        raw_text = extract_text_from_pdf(uploaded_file)
    else:
        raw_text = extract_text_from_docx(uploaded_file)

    st.subheader("Texte extrait")
    st.text_area("Contenu du document", raw_text, height=250)

    # Indexation pour le chat IA
    if not st.session_state.rag_chunks:
        index, chunks, embeddings = build_index(raw_text)
        st.session_state.rag_chunks = chunks
        st.session_state.rag_embeddings = embeddings

    # Bouton Reformuler
    if st.button("Reformuler pour dyslexie"):
        with st.spinner("Reformulation en cours..."):
            st.session_state.reformulated_text = reformulate_text(raw_text)

    # Affichage du texte reformulé
    if st.session_state.reformulated_text:
        st.subheader("Texte reformulé")
        st.text_area("Texte adapté", st.session_state.reformulated_text, height=250)

        # Téléchargement PDF
        if st.button("Télécharger en PDF"):
            path = export_to_pdf(st.session_state.reformulated_text)
            with open(path, "rb") as f:
                st.download_button("Télécharger le PDF", f, file_name="cours_dyslexique.pdf")

        # Lecture audio
        if st.button("Lire à haute voix"):
            audio_path = text_to_speech(st.session_state.reformulated_text)
            st.audio(audio_path)

    # Chat IA
    st.subheader("Pose une question sur ce document")
    question = st.text_input("Ta question")
    if question:
        if is_question_relevant(question, st.session_state.rag_embeddings):
            response = ask_question(question, raw_text)
            st.markdown(f"**Réponse :** {response}")
        else:
            st.warning("Ta question semble hors sujet par rapport au document.")
