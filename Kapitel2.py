import nltk
from nltk.corpus import gutenberg

################ Kapitel 2
print("############################# 2. Accessing Text Corpora and Lexical Resources #############################")

# Aufgabe 1

print(nltk.corpus.gutenberg.fileids())

emma_words = nltk.corpus.gutenberg.words('austen-emma.txt')
emma = nltk.Text(emma_words) # Wichtig!!!! Text muss erst al Corpus geladen und dann in Text umgewandelt werden, damit weitergearbeitet werden kann wie zB Konkordanz

print(len(emma))

print(emma.concordance("surprize"))

gutenberg.fileids()
emma = gutenberg.words('austen-emma.txt')

print("-------------------------------------------------------------------")

for fileid in gutenberg.fileids():
    num_chars = len(gutenberg.raw(fileid))
    num_words = len(gutenberg.words(fileid))
    num_sents = len(gutenberg.sents(fileid))
    num_vocab = len(set(w.lower() for w in gutenberg.words(fileid)))
    print(round(num_chars/num_words), round(num_words/num_sents), round(num_words/num_vocab), fileid)