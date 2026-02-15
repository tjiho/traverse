"""
Génère des descriptions naturelles en français à partir des descriptions wiki EN/FR
en utilisant l'API Mistral. Sauvegarde dans data/osm_wiki_tags_natural_desc.json
"""

import json
import time
import os
from mistralai import Mistral

API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-large-latest"
INPUT_FILE = "data/data_tmp/osm_tags_complete.json"
OUTPUT_FILE = "data/osm_wiki_tags_natural_desc.json"
BATCH_SIZE = 20  # tags par requête pour réduire le nombre d'appels

client = Mistral(api_key=API_KEY)


def format_tag_descriptions(item: dict) -> str:
    """Formate les descriptions EN/FR d'un tag pour le prompt."""
    tag = item["tag"]
    desc_en = item.get("description_en", "")
    desc_fr = item.get("description_fr", "")

    parts = [f"- {tag}"]
    if desc_en:
        parts.append(f" [EN]: {desc_en}")
    if desc_fr:
        parts.append(f" [FR]: {desc_fr}")
    if not desc_en and not desc_fr:
        parts.append(f" (pas de description)")

    return "".join(parts)


def build_batch_prompt(tags_batch: list[dict]) -> str:
    """Construit un prompt pour générer des descriptions naturelles à partir des descriptions wiki."""
    lines = [format_tag_descriptions(item) for item in tags_batch]

    return f"""Voici des tags OpenStreetMap avec leurs descriptions wiki en anglais et/ou français.
Pour chaque tag, produis UNE phrase descriptive naturelle en français (max 20 mots).
La phrase doit décrire ce qu'est le lieu ou l'attribut pour que quelqu'un qui cherche en français puisse le trouver.
Ne mets pas le nom du tag dans la phrase. Si aucune description n'est fournie, déduis du nom du tag.

{chr(10).join(lines)}

Réponds UNIQUEMENT au format JSON (un objet avec les tags comme clés et les phrases comme valeurs), sans markdown ni commentaire.
Exemple de format: {{"shop=bakery": "Magasin où l'on achète du pain, des baguettes, des croissants et des viennoiseries"}}"""


def process_batch(tags_batch: list[dict]) -> dict:
    """Envoie un batch à Mistral et parse la réponse JSON."""
    prompt = build_batch_prompt(tags_batch)
    response = client.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    text = response.choices[0].message.content.strip()
    # Nettoyer si le modèle entoure de ```json ... ```
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]
    return json.loads(text)


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Charger les résultats existants si reprise
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
        print(f"Reprise: {len(results)} tags déjà traités")
    else:
        results = {}

    # Collecter tous les tags à traiter
    all_tags = []
    for category, info in data.items():
        if "values" not in info:
            continue
        for tag_val, tag_info in info["values"].items():
            full_tag = f"{category}={tag_val}"
            if full_tag in results:
                continue
            desc_en = tag_info.get("description_en", "")
            desc_fr = tag_info.get("description_fr", "")
            all_tags.append({
                "tag": full_tag,
                "description_en": desc_en,
                "description_fr": desc_fr,
            })

    print(f"{len(all_tags)} tags à traiter ({len(results)} déjà faits)")

    # Traiter par batch
    for i in range(0, len(all_tags), BATCH_SIZE):
        batch = all_tags[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (len(all_tags) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"Batch {batch_num}/{total_batches} ({len(batch)} tags)...", end=" ", flush=True)

        try:
            batch_results = process_batch(batch)
            results.update(batch_results)
            print(f"OK ({len(batch_results)} résultats)")
        except Exception as e:
            print(f"ERREUR: {e}")
            # Sauvegarder ce qu'on a avant de continuer
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            time.sleep(2)
            continue

        # Sauvegarder régulièrement
        if batch_num % 5 == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

        time.sleep(0.3)  # rate limiting

    # Sauvegarde finale
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nTerminé ! {len(results)} descriptions sauvegardées dans {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
