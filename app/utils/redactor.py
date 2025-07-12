import re
import spacy
from spacy.pipeline import EntityRuler

# Load blank English model
nlp = spacy.load("en_core_web_sm")  # Or your custom trained model

# Add rule-based patterns
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "EMAIL", "pattern": [{"LIKE_EMAIL": True}]},
    {"label": "PHONE_NUMBER", "pattern": [{"SHAPE": "ddd"}, {"ORTH": "-", "OP": "?"}, {"SHAPE": "ddd"}, {"ORTH": "-", "OP": "?"}, {"SHAPE": "dddd"}]},
    {"label": "ACCOUNT_KEY", "pattern": [{"LOWER": "accountkey"}, {"ORTH": ":"}, {"IS_DIGIT": True}]},
    {"label": "ACCOUNT_NUMBER", "pattern": [{"LOWER": "account"}, {"ORTH": ":"}, {"TEXT": {"REGEX": r"AM\d+"}}]},
    {"label": "AADHAAR", "pattern": [{"TEXT": {"REGEX": r"\d{4}\s\d{4}\s\d{4}"}}]},
    {"label": "PAN", "pattern": [{"TEXT": {"REGEX": r"[A-Z]{5}[0-9]{4}[A-Z]{1}"}}]}
]
ruler.add_patterns(patterns)

# Redaction function
def redact_text(text: str) -> str:
    doc = nlp(text)
    redacted_text = text

    # Replace detected entities with <LABEL>
    for ent in doc.ents:
        redacted_text = redacted_text.replace(ent.text, f"<{ent.label_}>", 1)

    # Extra regex fallback (optional if EntityRuler doesn't catch something)
    redacted_text = re.sub(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', '<PHONE_NUMBER>', redacted_text)

    return redacted_text


