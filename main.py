import matplotlib.pyplot as plt
from nltk.book import *


print("-------------------------------------")

text2.concordance("monstrous")

print("-------------------------------------")

text2.similar("monstrous")

print("-------------------------------------")

text2.common_contexts(["monstrous", "very"])

print("-------------------------------------")

print("START")

text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])
#plt.show()

print("ENDE")

print(text3[:20])
print(sorted(set(text3)))
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