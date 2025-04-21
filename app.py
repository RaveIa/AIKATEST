
import streamlit as st
from utils.extract import extract_text_from_pdf, extract_text_from_docx
from utils.ai import reformulate_text, ask_question
from utils.export import export_to_pdf
from utils.tts import text_to_speech
from utils.rag import build_index, is_question_relevant
import tempfile

st.set_page_config(page_title="Assistant Dyslexie", layout="wide")
st.title("Assistant IA pour élèves dyslexiques")

uploaded_file = st.file_uploader("Charge un fichier PDF ou Word", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        raw_text = extract_text_from_pdf(uploaded_file)
    else:
        raw_text = extract_text_from_docx(uploaded_file)

    st.subheader("Texte extrait")
    st.text_area("Contenu du document", raw_text, height=250)

    if st.button("Reformuler pour dyslexie"):
        with st.spinner("Reformulation en cours..."):
            reformulated_text = reformulate_text(raw_text)
        st.subheader("Texte reformulé")
        st.text_area("Texte adapté", reformulated_text, height=250)

        if st.button("Télécharger en PDF"):
            path = export_to_pdf(reformulated_text)
            with open(path, "rb") as f:
                st.download_button("Télécharger le PDF", f, file_name="cours_dyslexique.pdf")

        if st.button("Lire à haute voix"):
            audio_path = text_to_speech(reformulated_text)
            st.audio(audio_path)

        st.subheader("Pose une question sur ce document")
        question = st.text_input("Ta question")
        if question:
            index, chunks, embeddings = build_index(raw_text)
            if is_question_relevant(question, embeddings):
                response = ask_question(question, raw_text)
                st.markdown(f"**Réponse :** {response}")
            else:
                st.warning("Ta question semble hors sujet par rapport au document.")
