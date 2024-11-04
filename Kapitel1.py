import matplotlib.pyplot as plt
from nltk.book import *
import nltk

################ Kapitel 1
print("############################# 1. Language Processing and Python #############################")

text2.concordance("monstrous") #Auflistung des entsprechenden Suchwortes

print("-------------------------------------")

text2.similar("monstrous") #Worte die Ähnlich verwendet werden wie der String

print("-------------------------------------")

text2.common_contexts(["monstrous", "very"]) #Kann die Kontexte untersuchen, die zwei oder mehr Wörter gemeinsam haben, wie z. B. monstrous und very.

print("-------------------------------------")

print("START")

#text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"]) #Stellt grafisch die Positionen im Text an denen die einzelnen Wörter vorkommen dar
#plt.show()

print("ENDE")

print(text3[:20])
print(sorted(set(text3))) #set erstellt eine Liste (Eselsbrücke: Ein Set!) an Elementen die in der ausgewählten Variable/Liste vorkommen. Jedoch ohne Häufigkeit
print("---------------------------------------")
print(len(set(text3)))
print(len(set(text3))/len(text3))

print("smote:",text3.count("smote"))
print("god:",text3.count("God"))
print(100 * text4.count('a') / len(text4))

test = "To be or not to be? Thats the question!"
print(test)
print(sorted(set(test)))
print("---------------------------------------")
print(len(set(test)))
print(len(set(test))/len(test))
print("a:",test.count("n"))

print("SENT")
print(sent2)

print("################ Aufgabe 3") ################ Aufgabe 3

### Aufgabe 3.1

fdist1 = FreqDist(text1) #Frequency Distribution (Frequenzverteilung); Wie oft befindet sich jedes einzelne Wort in text1 (Moby Dick)
print("fdist1:",fdist1) #Samples = Anzahl einzigartiger Wörter; Outcomes = Gesamtzahl aller Wörter, einschließlich Wiederholungen

print("fdist1 most common:",fdist1.most_common(50)) #Zeige die häufigsten 50 wörter an; Keine Zahl zeigt alle Wörter an

print("fsist1 'wahle':",fdist1['whale']) #Wie oft kommt STRING (zB wahle) im Text vor?

fdist1.plot(50, cumulative=True) #Plotted die Häufigkeit der ersten n (in unserem bsp 50) Wörter
#plt.show()

print("hapaxes:",fdist1.hapaxes()) #Hapax oder Hapax legomena (Einzahl: Hapax legomenon) Begriff aus der Sprachwissenschaft und bedeutet "einmal gesagte Wörter"

### Aufgabe 3.2

V = set(text1) #V für Vocabular 
long_words = [w for w in V if len(w) > 15] #Wörter mit mindestens einer Länge von 15 Buchstaben

print("Long Words:",sorted(long_words))

fdist5 = FreqDist(text5)
print(sorted(w for w in set(text5) if len(w) > 7 and fdist5[w] > 7)) #Finde Wörter die mind. 7 Buchstaben lang sind und min. 7 mal im Text vorkommen

### Aufgabe 3.3

print("bigrams:",list(bigrams(['more', 'is', 'said', 'than', 'done'])))
print("#############################################################################################")
print("text4 collocations:")
text4.collocations() # Erstellt eine Liste an Kollokationen

### Aufgabe 3.4

print("Länge:",[len(w) for w in text1]) #Länge der Wörter

fdist = FreqDist(len(w) for w in text1) #FreqDist zählt die Häufigkeit wie oft welche längen vorkommen
print(fdist)
print("-----------")
print("fdist most common:",fdist.most_common()) #Zeige die häufigsten wörter an
print("Max:",fdist.max()) #Zeige mit welche Wortlänge am häufigsten vorkommt
print("Wörter mit 3 Zeichen:",fdist[3]) #Wie oft kommt das Wort, welches vorher mit max ermittelt wurde im Text vor? Hier: Über 50.000 mal
print("Frequenz:",fdist.freq(3)) #Wie hoch ist die Häufigkeitsfrequenz? In dem Fall 19,3 %

print("################ Aufgabe 5") ################ Aufgabe 5

#nltk.chat.chatbots()
