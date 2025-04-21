import streamlit as st
from utils.extract import extract_text_from_pdf, extract_text_from_docx
from utils.export import export_to_pdf
from utils.tts import text_to_speech
from utils.rag import build_index, is_question_relevant
from utils.ai import reformulate_text, ask_question, detect_topic

st.set_page_config(page_title="Assistant IA - Dyslexie", layout="wide")
st.title("🧠 Assistant IA pour élèves dyslexiques")

if "reformulated_text" not in st.session_state:
    st.session_state.reformulated_text = ""
if "rag_chunks" not in st.session_state:
    st.session_state.rag_chunks = []
if "rag_embeddings" not in st.session_state:
    st.session_state.rag_embeddings = []
if "document_topic" not in st.session_state:
    st.session_state.document_topic = ""

uploaded_file = st.file_uploader("📂 Charge un fichier PDF ou Word", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        raw_text = extract_text_from_pdf(uploaded_file)
    else:
        raw_text = extract_text_from_docx(uploaded_file)

    # Analyse du thème
    if not st.session_state.document_topic:
        with st.spinner("🔎 Analyse du thème du document..."):
            st.session_state.document_topic = detect_topic(raw_text)
    st.info(f"📚 Thème détecté : *{st.session_state.document_topic}*")

    # Indexation pour le chat
    if not st.session_state.rag_chunks:
        _, chunks, embeddings = build_index(raw_text)
        st.session_state.rag_chunks = chunks
        st.session_state.rag_embeddings = embeddings

    # Reformulation
    if st.button("✨ Reformuler pour dyslexie"):
        with st.spinner("Reformulation en cours..."):
            st.session_state.reformulated_text = reformulate_text(raw_text)

    if st.session_state.reformulated_text:
        st.success("Texte reformulé avec succès !")
        if st.button("📄 Télécharger version PDF adaptée"):
            path = export_to_pdf(st.session_state.reformulated_text)
            with open(path, "rb") as f:
                st.download_button("📥 Télécharger", f, file_name="cours_dyslexique.pdf")

    # Chat IA avec contexte élargi par thème
    st.subheader("💬 Pose une question liée au document")
    question = st.text_input("Ta question ici")
    if question:
        response = ask_question(question, st.session_state.rag_chunks, topic=st.session_state.document_topic)
        st.markdown(f"**Réponse :** {response}")
