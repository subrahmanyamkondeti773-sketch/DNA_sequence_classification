import os, warnings
warnings.filterwarnings('ignore')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dna_classification_project.settings'
import django; django.setup()
import joblib
import numpy as np
from pathlib import Path

models_dir = Path('models')
vectorizer = joblib.load(models_dir / 'vectorizer.pkl')
classifier = joblib.load(models_dir / 'dna_classifier.pkl')
label_encoder = joblib.load(models_dir / 'label_encoder.pkl')

sample_key = next(iter(vectorizer.vocabulary_.keys()))
k = len(sample_key)
print(f"K-mer size: {k}, Classes: {label_encoder.classes_}")

def kmers(seq, k):
    seq = seq.lower()
    return ' '.join(seq[i:i+k] for i in range(len(seq)-k+1))

def predict(seq, label=''):
    f = vectorizer.transform([kmers(seq, k)])
    p = classifier.predict(f)
    lbl = label_encoder.inverse_transform(p)[0]
    if hasattr(classifier, 'predict_proba'):
        pr = classifier.predict_proba(f)[0]
        cls = label_encoder.classes_
        probs = {c: round(v,3) for c,v in zip(cls, pr)}
        print(f"  {label:30s} -> {lbl:15s} probs={probs}")
    else:
        print(f"  {label:30s} -> {lbl}")

# Try real genomic sequences - longer ones from known databases
# Human TP53 (tumor suppressor) fragment
human_tp53 = "ATGTTTTGCCAACTGGCCAAGACCTGCCCTGTGCAGCTGTGGGTTGATTCCACACCCCCGCCCGGCACCCGCGTCCGCGCCATGGCCATCTACAAGCAGTCACAGCACATGACGGAGGTTGTGAGGCGCTGCCCCCACCATGAGCGCTGCTCAGATAGCGATGGTCTGGCCCCTCCTCAGCATCTTATCCGAGTGGAAGGAAATTTGCGTGTGGAGTATTTGGATGACAGAAACACTTTTCGACATAGTGTGGTGGTGCCCTATGAGCCGCCTGAGGTTGGCTCTGACTGTACCACCATCCACTACAACTACATGTGTAACAGTTCCTGCATGGGCGGCATGAACCGGAGGCCCATCCTCACCATCATCACACTGGAAGACTCCAGTGGTAATCTACTGGGACGGAACAGCTTTGAGGTGCGTGTTTGTGCCTGTCCTGGGAGAGACCGGCGCACAGAGGAAGAGAATCTCCGCAAGAAAGGGGAGCCTCACCACGAGCTGCCCCCAGGGAGCACTAAGCGAGCACTGCCCAACAACACCAGCTCCTCTCCCCAGCCAAAGAAGAAACCACTGGATGGAGAATATTTCACCCTTCAGATCCGTGGGCGTGAGCGCTTCGAGATGTTCCGAGAGCTGAATGAGGCCTTGGAACTCAAGCCGTACTCCCCGGACGAT"

# Chimpanzee FOXP2 fragment
chimp_foxp2 = "ATGCAGCAGCCCCGGCAGCAGCAGCAGCAGCAAAGCAAGATCAGCAGCAACAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAG"

# Dog IGF1 fragment
dog_igf1 = "ATGGGAATCCCAGAAGGAAAGTCAGCTTGCAAATGGAATGGATTTCCAGCAGTAGCAGCCCAGCCCCCGGAGCCACAGCCCCCAGCCCCAGCCCCAGCACCCAGCACCCGGCCGCAGCACCCGGAGAGCAGCAGAGCCCAGCAAGGCAGCAGCAGCAGCAGCAGATCAAGAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAG"

sequences = [
    (human_tp53, "Human TP53"),
    (chimp_foxp2, "Chimp FOXP2"),
    (dog_igf1, "Dog IGF1"),
    # Shorter ones
    (human_tp53[:200], "Human TP53 (200bp)"),
    (human_tp53[:100], "Human TP53 (100bp)"),
    (human_tp53[:60], "Human TP53 (60bp)"),
]

for seq, label in sequences:
    predict(seq.upper(), label)
