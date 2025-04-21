import streamlit as st
import openai

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Fonction générale pour appeler GPT-3.5
def call_openai_chat(prompt: str, system_message: str = "Tu es un assistant pédagogique.") -> str:
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

# Reformulation du texte
def reformulate_text(text: str) -> str:
    if not text.strip():
        return "⚠️ Texte vide."
    prompt = (
        "Réécris le texte suivant pour qu’il soit facile à lire pour un élève dyslexique. "
        "Utilise des phrases courtes, un vocabulaire simple, et une structure claire :\n\n"
        f"{text}"
    )
    return call_openai_chat(prompt)

# Détection du thème principal du document
def detect_topic(text: str) -> str:
    prompt = (
        "Voici un extrait de document. Résume en une seule phrase courte et claire le thème principal de ce document :\n\n"
        f"{text[:1500]}"
    )
    return call_openai_chat(prompt, system_message="Tu es un assistant pédagogique.")

# Réponse à une question basée sur le thème
def ask_question(question: str, chunks: list[str], topic: str) -> str:
    if not question.strip():
        return ""
    context = "\n\n".join(chunks[:3])  # 3 chunks les plus pertinents
    prompt = (
        "Tu es un assistant pédagogique. Le document ci-dessous traite du thème suivant : "
        f"« {topic} ».\n\n"
        "Réponds à la question de l'utilisateur de façon claire et accessible, même si la réponse "
        "ne figure pas dans le texte, tant qu'elle reste dans le thème.\n\n"
        "Si la question n'a aucun lien avec ce thème, dis simplement : "
        "« Je ne peux pas répondre car ce n’est pas lié au sujet du document. »\n\n"
        f"=== Texte extrait ===\n{context}\n\n"
        f"=== Question ===\n{question}"
    )
    return call_openai_chat(prompt)
