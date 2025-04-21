import streamlit as st
import openai

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def call_openai_chat(prompt: str, system_message: str = "Tu es un assistant pédagogique spécialisé pour les élèves dyslexiques.") -> str:
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur OpenAI : {str(e)}"

def reformulate_text(text: str) -> str:
    if not text.strip():
        return "⚠️ Texte vide."
    prompt = (
        "Réécris le texte suivant pour qu’il soit plus facile à lire pour un élève dyslexique. "
        "Utilise des phrases courtes, un vocabulaire simple, et une structure claire :\n\n"
        f"{text}"
    )
    return call_openai_chat(prompt)

def ask_question(question: str, context: str) -> str:
    if not question.strip():
        return ""
    prompt = (
        "Voici un texte :\n\n"
        f"{context}\n\n"
        "Tu dois répondre à la question suivante **en te basant uniquement sur ce texte**. "
        "Si tu ne trouves pas la réponse dans le texte, dis : « Je ne peux pas répondre car ce n’est pas dans le document. »\n\n"
        f"Question : {question}"
    )
    return call_openai_chat(prompt)
