from dataclasses import dataclass, replace


@dataclass
class Candidate:
    tag: str                  # "amenity=restaurant"
    description_fr: str       # "Restaurant"
    description_natural: str  # "Lieu où l'on déguste des repas..." (Mistral)
    category: str             # "poi" | "attribute"
    usage_count: int          # 1534079
    score: float = 0.0        # rempli par search, puis écrasé par rerank
    visibility: str = ""      # "popular" | "niche" — rempli par rerank
