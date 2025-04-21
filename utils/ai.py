
import requests
import os
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def reformulate_text(text):
    prompt = f"Réécris ce texte pour qu'il soit plus facile à lire pour un élève dyslexique : {text}"
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.json()[0]["generated_text"]

def ask_question(question, context):
    prompt = f"Réponds uniquement si la réponse se trouve dans ce texte : {context}\nQuestion : {question}"
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.json()[0]["generated_text"]
