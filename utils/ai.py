import streamlit as st
import requests

# URL du modèle léger et compatible Inference API
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
}

def call_huggingface_api(prompt: str, max_new_tokens: int = 250):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": 0.7,
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": response.text}

def extract_generated_text(response_json):
    # Gestion d'erreur
    if isinstance(response_json, dict) and response_json.get("error"):
        return f"❌ Erreur HF : {response_json['error']}"
    # Si liste de dicts
    if isinstance(response_json, list):
        for item in response_json:
            if "generated_text" in item:
                return item["generated_text"].strip()
            if "output" in item:
                return item["output"].strip()
        return "❌ Aucune génération trouvée."
    # Cas dict simple
    if isinstance(response_json, dict) and "generated_text" in response_json:
        return response_json["generated_text"].strip()
    return "❌ Réponse inattendue."

def reformulate_text(text: str) -> str:
    if not text.strip():
        return "⚠️ Texte original vide, impossible de reformuler."
    prompt = (
        "Réécris le texte suivant pour qu'il soit clair et facile à lire "
        "pour un élève dyslexique. Utilise des phrases courtes et un vocabulaire simple :\n\n"
        f"{text}"
    )
    result = call_huggingface_api(prompt, max_new_tokens=250)
    return extract_generated_text(result)

def ask_question(question: str, context: str) -> str:
    if not question.strip():
        return ""
    prompt = (
        "Tu es un assistant pédagogique. Réponds **uniquement** si la réponse "
        "se trouve dans le texte ci‑dessous. Sinon, réponds : "
        "« Je ne peux répondre qu'à des questions sur ce document. »\n\n"
        "=== Texte de référence ===\n"
        f"{context}\n\n"
        "=== Question ===\n"
        f"{question}\n\n"
        "=== Fin du contexte ==="
    )
    result = call_huggingface_api(prompt, max_new_tokens=150)
    return extract_generated_text(result)
