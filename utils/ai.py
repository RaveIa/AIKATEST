import streamlit as st
import requests

# API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
}

# Fonction pour lire proprement la réponse
def extract_generated_text(response_json):
    if isinstance(response_json, list) and "generated_text" in response_json[0]:
        return response_json[0]["generated_text"]
    elif isinstance(response_json, dict) and "generated_text" in response_json:
        return response_json["generated_text"]
    elif isinstance(response_json, list) and "output" in response_json[0]:
        return response_json[0]["output"]
    else:
        return "Erreur : le modèle n'a pas renvoyé de réponse lisible."

# Reformulation
def reformulate_text(text):
    prompt = (
        "Réécris le texte suivant pour qu’il soit plus clair, avec des phrases simples, pour un élève dyslexique :\n\n"
        f"{text}"
    )
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return extract_generated_text(response.json())

# Chat IA basé uniquement sur le document
def ask_question(question, context):
    prompt = (
        "Tu es un assistant pédagogique. Réponds uniquement si la réponse se trouve dans ce texte :\n\n"
        f"{context}\n\n"
        f"Question : {question}\n\n"
        "Si la réponse ne s’y trouve pas, réponds : « Je ne peux répondre qu'à des questions sur ce document. »"
    )
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return extract_generated_text(response.json())
