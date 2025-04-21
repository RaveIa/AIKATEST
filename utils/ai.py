import streamlit as st
import openai

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Appelle GPT-3.5-Turbo pour une tâche donnée
def call_openai_chat(prompt: str, system_message: str = "Tu es un assistant pédagogique spécialisé pour les élèves dyslexiques.") -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur OpenAI : {str(e)}"

# Reformulation du texte pour un public dyslexique
def reformulate_text(text: str) -> str:
    if not text.strip():
        return "⚠️ Texte vide."
    prompt = (
        "Réécris le texte suivant pour qu’il soit facile à lire pour un élève dyslexique. "
        "Utilise des phrases courtes, un vocabulaire simple, et une structure claire :\n\n"
        f"{text}"
    )
    return call_openai_chat(prompt)

# Pose une question sur le document (avec contexte RAG)
def ask_question(question: str, chunks: list[str]) -> str:
    if not question.strip():
        return ""
    context = "\n\n".join(chunks[:3])  # prend les 3 chunks les plus pertinents déjà triés
    prompt = (
        "Voici un extrait de document :\n\n"
        f"{context}\n\n"
        "Tu dois répondre à la question suivante **uniquement** si la réponse est dans le texte ci-dessus.\n"
        "Si la réponse ne s'y trouve pas, dis : « Je ne peux pas répondre car ce n’est pas dans le document. »\n\n"
        f"Question : {question}"
    )
    return call_openai_chat(prompt)
