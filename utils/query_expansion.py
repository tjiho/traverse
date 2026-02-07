"""
Query expansion avec LLM pour enrichir les requêtes de recherche
"""

from transformers import pipeline
import torch

MODEL_NAME = "google/gemma-3-1b-it"

# Chargement lazy du modèle
_generator = None

def _get_generator():
    global _generator
    if _generator is None:
        _generator = pipeline(
            "text-generation",
            model=MODEL_NAME,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
    return _generator


def expand_query(query: str, max_terms: int = 10) -> str:
    """
    Enrichit une requête avec des termes liés/synonymes.

    Args:
        query: La requête originale (ex: "où manger")
        max_terms: Nombre max de termes à ajouter

    Returns:
        Requête enrichie (ex: "où manger restaurant restauration fast-food café")
    """
    generator = _get_generator()

    prompt = f"""Tu enrichis des requêtes pour chercher des lieux sur une carte.
Donne des synonymes et types de lieux liés, séparés par des virgules.
Maximum {max_terms} termes uniques, pas de répétition.

Exemples:
- "café" → espresso, terrasse, salon de thé, coffee shop, bar
- "faire du sport" → gymnase, stade, piscine, terrain, salle de sport
- "essence" → station-service, carburant, diesel, pompe

Requête: "{query}"
Termes liés:"""

    result = generator(
        prompt,
        max_new_tokens=50,
        do_sample=False,
        pad_token_id=generator.tokenizer.eos_token_id,
    )

    # Extraire la réponse
    response = result[0]["generated_text"][len(prompt):].strip()

    # Nettoyer: prendre la première ligne, split par virgule ou espace
    first_line = response.split("\n")[0].replace("-", "").strip()

    # Split par virgule ou espace
    if "," in first_line:
        terms = [t.strip().lower() for t in first_line.split(",")]
    else:
        terms = [t.strip().lower() for t in first_line.split()]

    # Enlever doublons, mots trop courts, et mots déjà dans la requête
    query_words = set(query.lower().split())
    seen = set()
    unique_terms = []
    for t in terms:
        if t and len(t) > 2 and t not in seen and t not in query_words:
            seen.add(t)
            unique_terms.append(t)

    terms = unique_terms[:max_terms]

    # Combiner requête originale + termes
    expanded = query + " " + " ".join(terms)
    return expanded


# Cache simple pour éviter de recalculer
_cache = {}

def expand_query_cached(query: str, max_terms: int = 10) -> str:
    """Version avec cache pour éviter les appels répétés"""
    cache_key = (query.lower().strip(), max_terms)
    if cache_key not in _cache:
        _cache[cache_key] = expand_query(query, max_terms)
    return _cache[cache_key]


if __name__ == "__main__":
    # Test
    test_queries = [
        "où manger",
        "restaurant",
        "faire les courses",
        "accessible fauteuil roulant",
    ]

    for q in test_queries:
        expanded = expand_query(q)
        print(f"'{q}' → '{expanded}'")
        print()
