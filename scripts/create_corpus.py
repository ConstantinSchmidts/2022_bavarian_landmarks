# Reading in all subtitle files from the train folder and creating a corpus.
# -*- coding: utf-8 -*-
import spacy
import srsly
import re

from torch import chunk

#Build upon the spaCy large German Model
nlp = spacy.load("de_core_news_lg")

#Create a blank list for appending later.
corpus = []

# ftfy can fix mojibake (encoding mix-ups), 
# by detecting patterns of characters that were clearly meant to be UTF-8
# but were decoded as something else
import ftfy

# Read in all subtitle text file from train folder to create corpus
import glob
import textract
path = './data/train_subtitles/*.txt' 
files=glob.glob(path) 
txt = ''

# Create regular expression that catches all lines that start with ♪ (Singing)
# and lines that are surroundes by * *, e.g. * Pfeifen *   
# and all lines that do not have any letters in them in order to remove timecodes
regex_tc = r"^\*.*\*$|^♪.*\.$|(?!^.*[a-zA-Z].*$)^.+"

# Taking the text from the subtitle files, preprocess it and split it into chunks of four sentences.
for file in files:
    text = textract.process(file)
    txt = text.decode("utf-8")
    # fix encoding errors
    txt = ftfy.fix_text(txt)
    # remove separators
    txt = txt.replace(" / ", " ")
    # remove timecodes and special character lines 
    txt_c1 = re.sub(regex_tc, " ", txt, 0, re.MULTILINE)
    # remove all whitespace characters (space, tab, newline, return, formfeed)
    txt_c2 = " ".join(txt_c1.split())
    doc = nlp(txt_c2)
    # use the spacy tokenizer to get sentences
    # Take four sentences and append them to corpus
    chunk_nr = 0
    chunk_text = "" 
    for sent in doc.sents:
        chunk_text += (" " + sent.text)
        chunk_nr += 1
        if chunk_nr % 4 == 0:
            corpus.append({"text": chunk_text})
            chunk_text = ""
            chunk_nr = 0
            

# Save corpus as .jsonl file to corpus folder
file_name = 'subtitles_corpus'
srsly.write_jsonl(f"./corpus/{file_name}.jsonl", corpus)

print("Corpus created")