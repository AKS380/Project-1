import spacy
from spacy.training import Example
from app.utils.tokenizer import custom_tokenizer_factory

TRAIN_DATA = [
    ("Login attempt by user: Shailesh Saple, ID: 12345", {"entities": [(23, 37, "PERSON")]}),
    ("Transaction from account: AM00413885 for $100.", {"entities": [(25, 37, "ACCOUNT_NBR")]}),
    ('{"bankerName": "Shailesh Saple"}', {"entities": [(16, 30, "PERSON")]}),
    ('customerName: Vaibhav Patel, accountKey: 10300000945630', {
        "entities": [(14, 27, "PERSON"), (40, 54, "ACCOUNT_KEY")]
    })
]

def train_model():
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")

    for _, annotations in TRAIN_DATA:
        for ent in annotations["entities"]:
            ner.add_label(ent[2])

    nlp.tokenizer = custom_tokenizer_factory(nlp)
    optimizer = nlp.begin_training()

    for itn in range(10):
        losses = {}
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.3, losses=losses)
        print(f"Losses at iteration {itn}: {losses}")

    nlp.to_disk("pii_redaction_model")

if __name__ == "__main__":
    train_model()
