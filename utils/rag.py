
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(text):
    chunks = [text[i:i+512] for i in range(0, len(text), 512)]
    embeddings = model.encode(chunks)
    return None, chunks, np.array(embeddings)

def is_question_relevant(question, embeddings, threshold=0.45):
    q_vec = model.encode([question])
    sims = (q_vec @ embeddings.T)[0]
    return max(sims) > threshold
