from viz import plot_multilegend
import os
from pprint import pprint
from es import ES

class Sentiment():
    
    def __init__(self, model):
        self.models = model
        self.es  = ES()
        

    def comparison_sentiment_embedders(self):
        docs = ["bello questo", "brutto questo", "non saprei","oggi è domenica",  "che noia di giorno.. c'è troppo rumore!", "adoro la notte e il suo silenzion, il suo colore, e il suo profumo", "non è bello questo quadro"]
        labels = ["w1", "w2", "w3", "w4", "w5", "w6", "w7"]
        colors = ["black", "lightgreen",  "red", "pink", "green", "purple", "grey", "cyan"]   

        models_preds = []
        for model_name, color in zip(self.models.list_pipelines(), colors):
            x, y, z = self.models.get_sentiment(docs, model_name)
            models_preds.append({"x": x, "y": y, "z": z, "labels": labels, "docs": docs, "legend": model_name, "color": color})
        return plot_multilegend(models_preds)
        
    
    def get_sent(self):
        words = ["ownership", "opinionated", "abandonware", "evangelismo"]
        persons = ["alva", "braggiotti", "cambieri", "chiarini", "dondi", "gamondi", "sgarro", "sperto"]
        colors = ["black", "lightgreen",  "red", "pink", "green", "purple", "grey", "cyan"]   
        
        
        models_preds_person_wise = []
        for person, color in zip(persons, colors):
            results = self.es.find_by_author(person, ["word", "meaning"], 1)
            labels = [res["word"] for res in results]
            docs = [res["meaning"] for res in results]
            x, y, z = self.models.get_sentiment(docs, "neuraly/bert-base-italian-cased-sentiment")
            models_preds_person_wise.append({"x": x, "y": y, "z": z, "labels": labels, "docs": docs, "legend": person, "color": color})
       
        
        version = 1
        models_preds_word_wise = []
        for word, color in zip(words, colors):
            labels, docs = [], []
            results = self.es.find_by_word(word, ["word", "meaning", "version", "author"])
            for res in results:
                if res["version"] == version:
                    labels.append(res["author"])
                    docs.append(res["meaning"])

            x, y, z = self.models.get_sentiment(docs, "neuraly/bert-base-italian-cased-sentiment")
            models_preds_word_wise.append({"x": x, "y": y, "z": z, "labels": labels, "docs": docs, "legend": word, "color": color})
        return plot_multilegend(models_preds_person_wise) , plot_multilegend(models_preds_word_wise)     
        
        
        
    # # se la prima versione di definizioni e quivale alla seconda
    # def get_coerenza():
    #     1
    #     # mostra tutti 
    #     # i colori caratterizzano un
        


def read_docs():
    persons = ["alva", "braggiotti", "cambieri", "chiarini", "dondi", "gamondi", "sgarro", "sperto"]
    corpus = dict()
    
    for person in persons:
        defs1, defs2 = dict(), dict()
        for file in os.listdir("data/" + person):
            with open("data/"+person+"/"+file, 'r') as f:
                doc = f.read()
                word = file[:file.index("_")]
                if doc:
                    if "_1" in file:
                        defs1[word] = doc
                    else:
                        defs2[word] = doc
                    
        corpus[person] = {"defs_1": defs1, "defs__2": defs2}
    return corpus                
        
                