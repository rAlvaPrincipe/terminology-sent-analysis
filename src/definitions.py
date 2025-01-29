import requests
from bs4 import BeautifulSoup
import time
from es import ES
import os
import pprint
from pprint import pprint


base_URL = "https://www.treccani.it/vocabolario/"
es = ES()

def get_meanings(word, delay=4):
    page = requests.get(base_URL  + word +"/")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("p", class_="MuiTypography-root MuiTypography-bodyL css-d8t48w")
    
    meanings_all = []
    if  len(results)==0:    # se word non ha associata una pagina
        print(word + " --> not found")
        if word[-1].isdigit()== False:   # per evitare di fare chiamate ricorsive infinite
            for i in range(1,5):
                time.sleep(delay)
                meanings = get_meanings(word+str(i))   # chiamata ricorsiva aggiungendo un digito alla word
                if meanings:                                 # se ha trova qualcosa aggiuni ai menaings
                    meanings_all.extend(meanings)
                else:
                    break
        else:
            return None
    else:                  #caso in cui trovi dei meanings
        out = process_treccani_results(word, results)
        if out:
            meanings_all.extend(out)
        else:                          # se in realtà si tratta di una pag del tesauro e non del vocab.
            for i in range(1,5):
                time.sleep(delay)
                meanings = get_meanings(word+str(i))   # chiamata ricorsiva aggiungendo un digito alla word
                if meanings:                                 # se ha trova qualcosa aggiuni ai menaings
                    meanings_all.extend(meanings)
                else:
                    break
    
    return meanings_all
        

def process_treccani_results(word, results):
    if len(results) == 1:
        soup = BeautifulSoup(str(results[0]), 'html.parser')
    else:  
        soup = BeautifulSoup(str(results[1]), 'html.parser')
    
    text = soup.get_text(separator=" ", strip=True)
    text = text[:text.find("◆ ")]
    if text == "":
        print(word + " --> not found")
        return None
    else:
        meanings = []
        if "1. " in text:
            text = text[text.find("1. "): ]

            for i in range(2, 20):
                index = text.find(str(i)+". ")
                meaning = text[3:index]
                meaning = meaning.replace(" , ", ", ")
                meaning = meaning.replace(" ; ", "; ")
                meaning = meaning.replace(" . ", ". ")
                meanings.append(meaning)
                if index == -1:
                    break
                text = text[index:]
        else:
            meanings.append(text)
            
        print(word + " --> done")   
        return meanings
    
     

def get_meanings_old(word):
    page = requests.get(base_URL  + word +"/")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("p", class_="MuiTypography-root MuiTypography-bodyL css-d8t48w")
    if len(results)==0:
        print(word + " --> not found")
        return None
    elif len(results) == 1:
        soup = BeautifulSoup(str(results[0]), 'html.parser')
    else:  
        soup = BeautifulSoup(str(results[1]), 'html.parser')
    
    text = soup.get_text(separator=" ", strip=True)
    text = text[:text.find("◆ ")]
    if text == "":
        print(word + " --> not found")
        return None
    else:
        meanings = []
        if "1. " in text:
            text = text[text.find("1. "): ]

            for i in range(2, 20):
                index = text.find(str(i)+". ")
                meaning = text[3:index]
                meaning = meaning.replace(" , ", ", ")
                meaning = meaning.replace(" ; ", "; ")
                meaning = meaning.replace(" . ", ". ")
                meanings.append(meaning)
                if index == -1:
                    break
                text = text[index:]
        else:
            meanings.append(text)
            
        print(word + " --> done")   
        return meanings


def scrape_vocabulary(vocab_path):
    with open(vocab_path, 'r') as file:
        words = file.read().splitlines()
        for count, word in enumerate(words):
            if es.exist_word(word):
                print(word + " --> skipped")
            else:
                time.sleep(4)
                meanings = get_meanings(word)
                es.insert(word, meanings, False)
            
            if count%100==0:
                print(count)
    
    
  
def load_custom_defs():
    persons = ["alva", "braggiotti", "cambieri", "chiarini", "dondi", "gamondi", "sgarro", "sperto"]
    
    for person in persons:        
        defs = dict()
        for file in os.listdir("data/" + person):
            with open("data/"+person+"/"+file, 'r') as f:
                word = file[:file.index("_")]
                doc = f.read()
                if doc:
                    if word in defs.keys():
                        tmp = defs[word]
                        tmp.append(doc)
                        defs[word] = tmp
                    else:
                        defs[word] = [doc]
            
        for key in defs.keys():
            es.insert(key, defs[key], True, person)  
            


# out = get_meanings("cane",1)
# for el in out:
#     pprint(el)
# print(len(out))
# # out = get_meanings_super("caro2")
# # print(out)