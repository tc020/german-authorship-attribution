import nltk
from nltk.corpus import gutenberg

nltk.download('punkt_tab')

################ Kapitel 2
print("############################# 2. Accessing Text Corpora and Lexical Resources #############################")

# Aufgabe 1 Accessing Text Corpora

# Aufgabe 1.1 Gutenberg Corpus

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

# Aufgabe 1.2 Web and Chat Text

from nltk.corpus import webtext #Zugriff auf etwas unkonventionellere Texte 

for fileid in webtext.fileids():
    print(fileid, webtext.raw(fileid)[:65], '...') 

from nltk.corpus import nps_chat #Zugriff auf Chat-Logs

chatroom = nps_chat.posts('10-19-20s_706posts.xml')
print(chatroom[123])

# Aufgabe 1.3 Umgant mit dem Brown Corpus

from nltk.corpus import brown #Zugriff auf den Brown Corpus (Erste große digitale Textsammlung aus 1961 von der Brown University) mit über 500 Quellen

print(brown.categories())
print(brown.words(categories='news'))
print(brown.words(fileids=['cg22']))
print(brown.sents(categories=['news', 'editorial', 'reviews']))

print("Modalverben") #Beispiel: Untersuchung auf Modalverben
news_text = brown.words(categories='news') 
fdist = nltk.FreqDist(w.lower() for w in news_text)
modals = ['can', 'could', 'may', 'might', 'must', 'will']
for m in modals:
    print(m + ':', fdist[m], end=' ') #end, damit die Auflistung in einer Zeile stattfindet. Sonst wäre es ein Modalverb pro Zeile
print(" ") #Leeres print um einen Zeilenumbruch zu erzeugen, da sonst die nächste Ausgabe zerschossen wird.


print("Modalverben je Genre") #Beispiel: Untersuchung der Modalverben pro Genre
cfd = nltk.ConditionalFreqDist(
    (genre, word)
    for genre in brown.categories()
    for word in brown.words(categories=genre))
genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
modals = ['can', 'could', 'may', 'might', 'must', 'will']
print(cfd.tabulate(conditions=genres, samples=modals))

# Aufgabe 1.4 Umgang mit dem Reuters Corpus

#Reuters Corpus contains 10,788 news documents totaling 1.3 million words; classified into 90 topics; grouped in "training" and "test"
from nltk.corpus import reuters #Zugriff auf den Reuters Corpus
print("Files and ID:",reuters.fileids())
print("Categeories:",reuters.categories())

print("Categories of Trainings ID 9865:",reuters.categories('training/9865'))
print("Categories of Trainings ID 9865 & 9880:",reuters.categories(['training/9865', 'training/9880']))
print("Files contain 'barley':",reuters.fileids('barley'))
print("Files contain 'barley & 'corn':",reuters.fileids(['barley', 'corn']))

print("Reuter Words:",reuters.words('training/9865')[:14]) #Erst5en 14 Wörter. Die Wörter in Capslock sind der Titel

# Aufgabe 1.5 Inaugural Address Corpus