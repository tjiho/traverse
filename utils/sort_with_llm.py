from transformers import pipeline

MODEL = "google/gemma-3-1b-it"

generator = pipeline("text-generation", model=MODEL, device_map="auto")

def sort_with_llm(tags):
    pass
