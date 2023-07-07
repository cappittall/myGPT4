tests = open("seks.txt", "r").read().splitlines()
item = tests[0]
item
import io
import random

sonuc = []
for item in tests:
    if item.startswith('Soru:'):
        sonuc.append(item)
        new_item = item.replace('Soru:', '')
        new_item = new_item.split()
        random.shuffle(new_item)
        new_item = " ".join(new_item)
        new_item = "Cevap: Çok severim, "+ new_item 
        sonuc.append(new_item)
    
with io.open("seks3.txt", "w") as f:
    for s in sonuc:
        f.write(s + "\n") 