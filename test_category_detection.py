"""
Test différentes approches pour détecter la catégorie de recherche (POI vs Attribut)
"""

import time
import torch

# === CAS DE TEST ===
TEST_CASES = [
    # POI seulement
    {"query": "restaurant", "expected": ["poi"]},
    {"query": "boulangerie", "expected": ["poi"]},
    {"query": "où manger", "expected": ["poi"]},
    {"query": "pharmacie", "expected": ["poi"]},
    {"query": "hôpital", "expected": ["poi"]},
    {"query": "banque", "expected": ["poi"]},
    {"query": "supermarché", "expected": ["poi"]},
    {"query": "parking", "expected": ["poi"]},
    {"query": "station essence", "expected": ["poi"]},
    {"query": "coiffeur", "expected": ["poi"]},

    # Attribut seulement
    {"query": "cuisine indienne", "expected": ["attribute"]},
    {"query": "accessible fauteuil roulant", "expected": ["attribute"]},
    {"query": "ouvert le dimanche", "expected": ["attribute"]},
    {"query": "wifi gratuit", "expected": ["attribute"]},
    {"query": "terrasse", "expected": ["attribute"]},
    {"query": "végétarien", "expected": ["attribute"]},
    {"query": "halal", "expected": ["attribute"]},
    {"query": "pizza", "expected": ["attribute"]},
    {"query": "paiement carte", "expected": ["attribute"]},
    {"query": "livraison", "expected": ["attribute"]},

    # Les deux
    {"query": "restaurant indien", "expected": ["poi", "attribute"]},
    {"query": "café avec wifi", "expected": ["poi", "attribute"]},
    {"query": "boulangerie ouverte dimanche", "expected": ["poi", "attribute"]},
    {"query": "pizzeria", "expected": ["poi", "attribute"]},
    {"query": "bar avec terrasse", "expected": ["poi", "attribute"]},
    {"query": "restaurant végétarien", "expected": ["poi", "attribute"]},
    {"query": "hôtel avec parking", "expected": ["poi", "attribute"]},
    {"query": "piscine accessible handicapé", "expected": ["poi", "attribute"]},
    {"query": "supermarché ouvert tard", "expected": ["poi", "attribute"]},
    {"query": "kebab halal", "expected": ["poi", "attribute"]},
]

LABELS_POI = ["lieu", "endroit", "établissement", "point d'intérêt"]
LABELS_ATTR = ["caractéristique", "attribut", "propriété", "type de cuisine", "accessibilité"]


def evaluate_method(name: str, predict_fn, test_cases: list) -> dict:
    """Évalue une méthode de détection"""
    correct = 0
    total = len(test_cases)
    errors = []

    start = time.time()
    for case in test_cases:
        predicted = predict_fn(case["query"])
        expected = set(case["expected"])

        if set(predicted) == expected:
            correct += 1
        else:
            errors.append({
                "query": case["query"],
                "expected": case["expected"],
                "predicted": predicted
            })

    elapsed = time.time() - start
    accuracy = correct / total

    print(f"\n{'='*60}")
    print(f"{name}")
    print(f"{'='*60}")
    print(f"Accuracy: {accuracy:.1%} ({correct}/{total})")
    print(f"Temps: {elapsed:.2f}s ({elapsed/total*1000:.1f}ms/query)")

    if errors[:5]:
        print(f"\nErreurs (max 5):")
        for e in errors[:5]:
            print(f"  '{e['query']}' → {e['predicted']} (attendu: {e['expected']})")

    return {"accuracy": accuracy, "time": elapsed, "errors": errors}


# === MÉTHODE 1: Règles heuristiques (baseline) ===
def detect_heuristic(query: str) -> list[str]:
    """Détection par règles simples"""
    query_lower = query.lower()
    words = query_lower.split()

    poi_keywords = {
        "restaurant", "café", "cafe", "bar", "boulangerie", "pharmacie",
        "hôpital", "hopital", "banque", "supermarché", "supermarche",
        "parking", "station", "coiffeur", "hôtel", "hotel", "magasin",
        "boutique", "où", "ou", "trouver", "cherche", "piscine"
    }

    attr_keywords = {
        "indien", "chinois", "japonais", "italien", "mexicain", "pizza",
        "burger", "kebab", "sushi", "végétarien", "vegetarien", "vegan",
        "halal", "casher", "accessible", "fauteuil", "handicapé", "handicape",
        "ouvert", "dimanche", "nuit", "24h", "wifi", "terrasse", "parking",
        "livraison", "carte", "paiement", "gratuit"
    }

    has_poi = any(w in poi_keywords for w in words)
    has_attr = any(w in attr_keywords for w in words)

    if has_poi and has_attr:
        return ["poi", "attribute"]
    elif has_attr:
        return ["attribute"]
    elif has_poi:
        return ["poi"]
    else:
        return ["poi"]  # défaut


# === MÉTHODE 2: Zero-shot classification ===
def load_zeroshot_classifier():
    from transformers import pipeline
    print("Chargement du modèle zero-shot...")
    classifier = pipeline(
        "zero-shot-classification",
        model="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7",
        device="cuda" if torch.cuda.is_available() else "cpu"
    )
    return classifier

def make_zeroshot_detector(classifier):
    def detect(query: str) -> list[str]:
        result = classifier(
            query,
            candidate_labels=["recherche d'un lieu ou établissement", "caractéristique ou attribut spécifique"],
            hypothesis_template="Cette recherche concerne {}.",
            multi_label=True
        )

        categories = []
        for label, score in zip(result["labels"], result["scores"]):
            if score > 0.5:
                if "lieu" in label:
                    categories.append("poi")
                else:
                    categories.append("attribute")

        return categories if categories else ["poi"]

    return detect


# === MÉTHODE 3: Embedding similarity ===
def load_embedding_model():
    from sentence_transformers import SentenceTransformer
    print("Chargement du modèle d'embedding...")
    model = SentenceTransformer("google/embeddinggemma-300m")
    return model

def make_embedding_detector(model):
    import numpy as np

    # Prototypes pour chaque catégorie
    poi_examples = [
        "restaurant", "boulangerie", "pharmacie", "hôpital", "banque",
        "supermarché", "parking", "station essence", "hôtel", "magasin",
        "où trouver un lieu", "chercher un endroit", "établissement"
    ]
    attr_examples = [
        "cuisine indienne", "accessible handicapé", "ouvert dimanche",
        "wifi gratuit", "terrasse", "végétarien", "halal", "pizza",
        "paiement carte", "livraison", "caractéristique", "attribut"
    ]

    poi_embeddings = model.encode(poi_examples, normalize_embeddings=True)
    attr_embeddings = model.encode(attr_examples, normalize_embeddings=True)

    poi_centroid = np.mean(poi_embeddings, axis=0)
    attr_centroid = np.mean(attr_embeddings, axis=0)

    # Normaliser les centroïdes
    poi_centroid = poi_centroid / np.linalg.norm(poi_centroid)
    attr_centroid = attr_centroid / np.linalg.norm(attr_centroid)

    def detect(query: str) -> list[str]:
        query_emb = model.encode([query], normalize_embeddings=True)[0]

        poi_sim = float(np.dot(query_emb, poi_centroid))
        attr_sim = float(np.dot(query_emb, attr_centroid))

        categories = []
        threshold = 0.3
        diff_threshold = 0.05

        if abs(poi_sim - attr_sim) < diff_threshold:
            return ["poi", "attribute"]
        elif poi_sim > attr_sim:
            return ["poi"]
        else:
            return ["attribute"]

    return detect


# === MÉTHODE 4: Petit LLM (Gemma) ===
def load_llm():
    from transformers import pipeline
    print("Chargement du LLM...")
    generator = pipeline(
        "text-generation",
        model="google/gemma-3-1b-it",
        device_map="auto",
        torch_dtype=torch.bfloat16
    )
    return generator

def make_llm_detector(generator):
    def detect(query: str) -> list[str]:
        prompt = f"""Classifie cette recherche en catégories. Réponds UNIQUEMENT par: POI, ATTRIBUT, ou LES_DEUX

- POI = recherche d'un lieu/établissement (restaurant, pharmacie, etc.)
- ATTRIBUT = recherche d'une caractéristique (cuisine indienne, accessible, wifi, etc.)
- LES_DEUX = les deux à la fois (restaurant indien, café avec wifi, etc.)

Recherche: "{query}"
Catégorie:"""

        result = generator(
            prompt,
            max_new_tokens=10,
            do_sample=False,
            pad_token_id=generator.tokenizer.eos_token_id
        )

        response = result[0]["generated_text"][len(prompt):].strip().upper()

        if "LES_DEUX" in response or ("POI" in response and "ATTR" in response):
            return ["poi", "attribute"]
        elif "ATTR" in response:
            return ["attribute"]
        else:
            return ["poi"]

    return detect


# === MAIN ===
if __name__ == "__main__":
    results = {}

    # 1. Heuristiques (baseline)
    results["heuristic"] = evaluate_method("1. Règles heuristiques (baseline)", detect_heuristic, TEST_CASES)

    # 2. Zero-shot
    try:
        classifier = load_zeroshot_classifier()
        detect_zeroshot = make_zeroshot_detector(classifier)
        results["zeroshot"] = evaluate_method("2. Zero-shot (mDeBERTa)", detect_zeroshot, TEST_CASES)
        del classifier
        torch.cuda.empty_cache()
    except Exception as e:
        print(f"Erreur zero-shot: {e}")

    # 3. Embedding similarity
    try:
        emb_model = load_embedding_model()
        detect_embedding = make_embedding_detector(emb_model)
        results["embedding"] = evaluate_method("3. Embedding similarity", detect_embedding, TEST_CASES)
        del emb_model
        torch.cuda.empty_cache()
    except Exception as e:
        print(f"Erreur embedding: {e}")

    # 4. LLM
    try:
        llm = load_llm()
        detect_llm = make_llm_detector(llm)
        results["llm"] = evaluate_method("4. LLM (Gemma 3 1B)", detect_llm, TEST_CASES)
        del llm
        torch.cuda.empty_cache()
    except Exception as e:
        print(f"Erreur LLM: {e}")

    # Résumé
    print(f"\n{'='*60}")
    print("RÉSUMÉ")
    print(f"{'='*60}")
    print(f"{'Méthode':<30} {'Accuracy':>10} {'Temps':>15}")
    print("-" * 60)
    for name, r in results.items():
        print(f"{name:<30} {r['accuracy']:>10.1%} {r['time']:>12.2f}s")
