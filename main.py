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

