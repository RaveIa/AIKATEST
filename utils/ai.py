import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
}

def call_huggingface_api(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": response.text}

def extract_generated_text(response_json):
    if "error" in response_json:
        return f"❌ Erreur Hugging Face : {response_json['error']}"
    if isinstance(response_json, list) and "generated_text" in response_json[0]:
        return response_json[0]["generated_text"]
    return "❌ Réponse inattendue du modèle."

def reformulate_text(text):
    prompt = (
        "Réécris le texte suivant pour qu'il soit clair, simple et facile à lire pour un élève dyslexique :\n\n"
    f"{text}"
    )
    result = call_huggingface_api(prompt)
    return extract_generated_text(result)

def ask_question(question, context):
    prompt = f"""
Tu es un assistant pédagogique. Réponds uniquement si la réponse se trouve dans ce texte :

{context}

Question : {question}

Si la réponse ne s’y trouve pas, réponds : « Je ne peux répondre qu'à des questions sur ce document. »
"""
    result = call_huggingface_api(prompt)
    return extract_generated_text(result)
