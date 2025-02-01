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

from nltk.corpus import inaugural #collection of 55 texts, one for each presidential address

print(inaugural.fileids()) #Zeige alle Files
print([fileid[:4] for fileid in inaugural.fileids()]) #Zeige nur die Jahre

#In welcher Frequenz kamen die Wörter "america" und "citizen" in den Reden vor?
cfd = nltk.ConditionalFreqDist(
    (target, fileid[:4])
    for fileid in inaugural.fileids()
    for w in inaugural.words(fileid)
    for target in ['america', 'citizen']
    if w.lower().startswith(target))

cfd.plot()

# Aufgabe 1.7 Corpora in Other Languages

#Encoding Beispiele
# print(nltk.corpus.cess_esp.words())
# print(nltk.corpus.floresta.words())
# print(nltk.corpus.indian.words('hindi.pos'))
# print(nltk.corpus.udhr.fileids())
# print(nltk.corpus.udhr.words('Javanese-Latin1')[11:])

# Aufgabe 1.8 Text Corpus Structure


# Aufgabe 1.9 Loading your own Corpus

# PlaintextCorpusReader:
# Wird verwendet, um einfache, unstrukturierte Textdateien zu lesen.
# Eignet sich für normale Texte ohne syntaktische Annotationen, z.B. Romane oder Artikel.
# Ermöglicht den Zugriff auf Wörter, Sätze oder rohen Text.

# Beispiel:
"""
from nltk.corpus import PlaintextCorpusReader
corpus_root = 'path/to/textfiles'  # Verzeichnis mit den Textdateien
corpus = PlaintextCorpusReader(corpus_root, '.*\.txt')
print(corpus.words())  # Gibt eine Liste aller Wörter im Korpus zurück
"""

# BracketParseCorpusReader:
# Wird für geparste Korpora mit syntaktischer Baumstruktur in Klammernotation verwendet.
# Die Klammernotation zeigt die hierarchische Struktur eines Satzes an (z.B. Subjekte, Prädikate, Objekte).
# Geeignet für Korpora wie den Penn Treebank, die syntaktische Analysen in Klammernotation verwenden.

# Beispiel:
"""
from nltk.corpus import BracketParseCorpusReader
corpus_root = 'path/to/bracketed/files'  # Verzeichnis mit den geparsten Dateien
corpus = BracketParseCorpusReader(corpus_root, '.*\.txt')
print(corpus.parsed_sents())  # Gibt eine Liste von Syntaxbäumen zurück
"""

# Aufgabe 2 Conditional Frequency Distributions

# Aufgabe 2.1 Conditions and Events

# Aufgabe 2.2 Countin Words by Genre

print("Aufgabe 2.2")

from nltk.corpus import brown
cfd = nltk.ConditionalFreqDist(
    (genre, word)
    for genre in brown.categories()
    for word in brown.words(categories=genre))

genre_word = [(genre, word)
    for genre in ['news', 'romance']
    for word in brown.words(categories=genre)]

print("LÄNGE:",len(genre_word))

cfd = nltk.ConditionalFreqDist(genre_word)
print("cfd:",cfd)
print("Conditions:",cfd.conditions())

print("cfd[news]:",cfd['news'])
print("cfd[romance]:",cfd['romance'])
print("cfd['romance'].most_common(20):",cfd['romance'].most_common(20))
print("cfd['romance']['could']:",cfd['romance']['could'])

# Aufgabe 2.3 Plotting and Tabulating Distributions
print("Aufgabe 2.3")

from nltk.corpus import udhr
languages = ['Chickasaw', 'English', 'German_Deutsch',
     'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik']
cfd = nltk.ConditionalFreqDist(
           (lang, len(word))
           for lang in languages
           for word in udhr.words(lang + '-Latin1'))

print(cfd.tabulate(samples=range(10), cumulative=True)) #Mit (conditions=['English', 'German_Deutsch'] würde es sich auf die zwei Conditions limitieren lassen
#range is for words less than 10 characters long, last column says there are words with 9 or fewer letters

# Aufgabe 2.4 Generating Random Text with Bigrams

# Aufgabe 3 More Python: Reusing Code

# Aufgabe 3.1-3.3 Python Grundlagen

"""
Gute Definition: Eine Sammlung von Variablen- und Funktionsdefinitionen in einer Datei wird als Python-**Modul** bezeichnet. Eine Sammlung von verwandten Modulen 
wird als **Paket/Package** bezeichnet. Der Code von NLTK für die Verarbeitung des Brown Corpus ist ein Beispiel für ein Modul, und die Sammlung von Code für die Verarbeitung 
aller verschiedenen Korpora ist ein Beispiel für ein Paket. NLTK selbst ist eine Sammlung von Paketen, manchmal auch **Bibliothek/Library** genannt.
"""

# Aufgabe 4 Lexical Resources

# Aufgabe 4.1 Wordlist Corpora

#Kann genutzt werden um z.B. Rechtschriebprüfung zu erstellen.
#Oder Liste mit Stopp-Wörtern um diese aus normalen Texten herausfiltern zu können, bevor man sie weiterverarbeitet

from nltk.corpus import stopwords
print("Stopwords:",stopwords.words('english'))

#Let's define a function to compute what fraction of words in a text are not in the stopwords list:

def content_fraction(text):
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in text if w.lower() not in stopwords]
    return len(content) / len(text)

print("Fraction Reuters Words:",content_fraction(nltk.corpus.reuters.words())) #Über 25 % der des Textes wird dadurch gekürzt


# Aufgabe 4.2 A Pronouncing Dictionary

# Aufgabe 4.3 Comparative Wordlists

#Kann genutzt werden um Übersetzer / Translator zu bauen

# Aufgabe 4.4 Shoebox and Toolbox Lexicons

# Aufgabe 5 WordNet

# Aufgabe 5.1 Senses and Synonyms

from nltk.corpus import wordnet as wn

print(wn.synsets('motorcar')) #synsets = Synonym Set = Collection of synonymous words ("lemmas")
print(wn.synset('car.n.01').lemma_names())
print(wn.synset('car.n.01').definition())
print(wn.synset('car.n.01').examples())

print(wn.synset('car.n.01').lemmas()) #We can get all the lemmas for a given synset
print( wn.lemma('car.n.01.automobile')) #look up a particular lemma
print(wn.lemma('car.n.01.automobile').synset()) #get the synset corresponding to a lemma
print(wn.lemma('car.n.01.automobile').name()) #and get the "name" of a lemma.

print(wn.lemmas('car')) #we can access all the lemmas involving the word car

# Aufgabe 5.2 The WorldNet Hierarchy
##################################### LETZTER STAND #########################################

print("############# Aufgabe 5.2")
print(motorcar = wn.synset('car.n.01'))
print(types_of_motorcar = motorcar.hyponyms())
print(types_of_motorcar[0])
print(sorted(lemma.name() for synset in types_of_motorcar for lemma in synset.lemmas()))

# Aufgabe 5.3 More Lexical Relations

print("############# Aufgabe 5.3")
print(wn.synset('tree.n.01').part_meronyms())

# Aufgabe 5.4 Semantic Similarity

print("############# Aufgabe 5.4")
right = wn.synset('right_whale.n.01')
orca = wn.synset('orca.n.01')
minke = wn.synset('minke_whale.n.01')
tortoise = wn.synset('tortoise.n.01')
novel = wn.synset('novel.n.01')
print(right.lowest_common_hypernyms(minke))
print(right.lowest_common_hypernyms(orca))
print(right.lowest_common_hypernyms(tortoise))
print(right.lowest_common_hypernyms(novel))

print(wn.synset('baleen_whale.n.01').min_depth())
print(wn.synset('whale.n.02').min_depth())
print(wn.synset('vertebrate.n.01').min_depth())
print(wn.synset('entity.n.01').min_depth())

print(right.path_similarity(minke))
print(right.path_similarity(orca))
print(right.path_similarity(tortoise))
print(right.path_similarity(novel))

############# KAPITEL ENDE #############