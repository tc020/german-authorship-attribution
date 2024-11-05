import nltk
from nltk.corpus import gutenberg

nltk.download('punkt_tab')

################ Kapitel 2
print("############################# 2. Accessing Text Corpora and Lexical Resources #############################")

# Aufgabe 1

print(nltk.corpus.gutenberg.fileids())

emma_words = nltk.corpus.gutenberg.words('austen-emma.txt')
print("WORDS():",emma_words)
emma = nltk.Text(emma_words) # Wichtig!!!! Text muss erst als Corpus geladen und dann in Text umgewandelt werden, damit weitergearbeitet werden kann wie zB Konkordanz

print(len(emma))

print(emma.concordance("surprize"))

gutenberg.fileids()
emma = gutenberg.words('austen-emma.txt')

print("-------------------------------------------------------------------")


for fileid in gutenberg.fileids(): #Gibt die Durchschnittliche Wortlänge (sprachtypisch engl 3-4), Satzlänge und Textdiversität wieder. Rest Autorcharakteristisch
    num_chars = len(gutenberg.raw(fileid)) #raw gibt einfach nur den Text als einzelne Zeichen zurück in seiner "Rohform"
    num_words = len(gutenberg.words(fileid)) #words extrahiert alle Wörter aus dem Corpus
    num_sents = len(gutenberg.sents(fileid)) #sents extrahiert alle Sätze und speichert jeden Satz als Listeneintrag ab
    num_vocab = len(set(w.lower() for w in gutenberg.words(fileid)))
    print(round(num_chars/num_words), round(num_words/num_sents), round(num_words/num_vocab), fileid)

macbeth_sentences = gutenberg.sents('shakespeare-macbeth.txt') #Die Funktion sents() unterteilt den Text in seine Sätze, wobei jeder Satz eine Liste von Wörtern ist

print(macbeth_sentences)
print(macbeth_sentences[1116]) #Zeige zB Satz-Nr. 1116 in der Liste
longest_len = max(len(s) for s in macbeth_sentences)
print("Längster Satz:",[s for s in macbeth_sentences if len(s) == longest_len]) #Finde den längsten Satz im Korpus

# Aufgabe 1.2

