# -*- coding: utf-8 -*-
import spacy
import json
import ftfy
import srsly

# Build upon a blank German spaCy Model
nlp = spacy.blank("de")

# Read in subtitle_corpus from .jsonl file
with open("corpus\subtitle_corpus.jsonl", "r", encoding='UTF-8') as f:
    corpus = [json.loads(line) for line in f]

# Read in patterns from json file
with open("data\patterns.jsonl", "r", encoding='UTF-8') as f:
    patterns = [json.loads(line) for line in f]

#Create the EntityRuler
ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns(patterns)

TRAIN_DATA = []

# Iterate over the corpus and create training data
for chunk in corpus:
    chunk = ftfy.fix_text(chunk["text"])
    doc = nlp(chunk)
    # entities needs to be a dictionary in index 1 of the list, so it needs to be an empty list
    entities = []
    # extract entities
    for ent in doc.ents:
        # appending to entities in the correct format
        entities.append([ent.start_char, ent.end_char, ent.label_])
    if len(entities) > 0:
        TRAIN_DATA.append([chunk, {"entities": entities}])

# Save training data as .jsonl
file_name = 'train_data'
srsly.write_jsonl(f"./data/{file_name}.jsonl", TRAIN_DATA)

print("train .json for visual inspection created")

# Convert to spacy3 binary data structure
import srsly
import typer
import warnings
from pathlib import Path

import spacy
from spacy.tokens import DocBin

def convert(lang: str, TRAIN_DATA, output_path: Path):
    nlp = spacy.blank(lang)
    db = DocBin()
    for text, annot in TRAIN_DATA:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)

# Create a validation set from 20% of the training data
from sklearn.model_selection import train_test_split
train, valid = train_test_split(TRAIN_DATA, test_size=0.2)

# Save training and validation data
convert("de", train, "data\\init_train.spacy")
convert("de", valid, "data\\init_valid.spacy")

print("training data for spaCy 3.2.4 created")