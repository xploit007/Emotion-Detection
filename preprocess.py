import re
import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    doc = nlp(text)
    tokens = [
        token.lemma_ for token in doc if not token.is_stop and token.lemma_.isalnum()
    ]
    return " ".join(tokens)
