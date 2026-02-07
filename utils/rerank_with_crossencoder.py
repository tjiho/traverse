from sentence_transformers import CrossEncoder
from .types import TagItem
# === CONFIG ===
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # ou nli-deberta-v3-small

# === CHARGEMENT ===
reranker = CrossEncoder(CROSS_ENCODER_MODEL, device="cuda")

def rerank(query: str, candidates: list[TagItem], top_k: int = 5) -> list[TagItem]:
    """Re-rank avec cross-encoder - pas de génération, juste des scores"""
    pairs = [(query, f"{item['tag']}: {item['description']}") for item in candidates]
    scores = reranker.predict(pairs)
    
    # Trier par score
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [{"tag": item['tag'], "description": item['description'] ,"score": float(score), "category": "poi"} for item, score in ranked[:top_k]]