from viz import plot_multilegend, plot
import os
from pprint import pprint
from sentiment_analysis import read_docs
from reductor import reductor_fit_transform
from es import ES
import random 
import pandas as pd
import numpy as np

class Sematics():
     
    def __init__(self, model):
        self.models = model   
        self.es  = ES()
    
    
    def concept(self):
        persons = ["alva", "braggiotti", "cambieri", "chiarini", "dondi", "gamondi", "sgarro", "sperto"]
        colors = ["black", "lightgreen",  "red", "pink", "green", "purple", "grey", "cyan"]   
        
        models_preds_person_wise = []
        for person, color in zip(persons, colors):
            x, y, z, labels, defs  =  [], [], [], [], []
            results = self.es.find_by_author(person, ["word", "meaning", "sbert_ita_3d"], 1)
            for res in results:
                x.append(res["sbert_ita_3d"][0])
                y.append(res["sbert_ita_3d"][1])
                z.append(res["sbert_ita_3d"][2])
                labels.append(res["word"])
                defs.append(res["id"])
            models_preds_person_wise.append({"x": x, "y": y, "z": z, "labels": labels, "docs": defs, "legend": person, "color": color})

        
        words = ["ownership", "opinionated", "abandonware", "evangelismo"]
        colors = ["black", "lightgreen",  "red", "pink", "green", "purple", "grey", "cyan"]   
        version = 1
        models_preds_word_wise = []
        for word, color in zip(words, colors):
            x, y, z, labels, defs  =  [], [], [], [], []
            results = self.es.find_by_word(word, ["word", "meaning", "sbert_ita_3d", "version"])
            for res in results:
                if res["version"] == version:
                    x.append(res["sbert_ita_3d"][0])
                    y.append(res["sbert_ita_3d"][1])
                    z.append(res["sbert_ita_3d"][2])
                    id =res["id"]
                    labels.append(id[id.find("_")+1: id.rfind("_")])
                    defs.append(res["id"])
            models_preds_word_wise.append({"x": x, "y": y, "z": z, "labels": labels, "docs": defs, "legend": word, "color": color})

        return plot_multilegend(models_preds_person_wise), plot_multilegend(models_preds_word_wise)

    # ALL CONCEPTS
    def mod_1(self, n_samples):
        results = self.es.get_all_docs(["sbert_ita_3d"], None, ["sbert_ita_3d"])
        results = random.sample(results, n_samples)  
        ids = [res["id"] for res in results]
        x = [res["sbert_ita_3d"][0] for res in results]
        y = [res["sbert_ita_3d"][1] for res in results]
        z = [res["sbert_ita_3d"][2] for res in results]

        return plot({"x": x, "y":y, "z":z, "labels": ids, "docs": ids, "legend": "tmp", "color":"blue"})
    
    
    # given a word returns  dataframe and a figures with the knn words
    def mod_2(self, id, scope):
        is_custom = None
        if scope == "custom definitions":
            is_custom = True
        elif scope == "Treccani definitions":
            is_custom = False
            
        results = self.es.knn_by_id(id, fields=["word", "meaning", "sbert_ita_3d"], is_custom=is_custom)
        
        x, y, z, ids = [], [], [], []
        for res in results:
            pprint(res)
        for res in results:
            if res["id"] !=id:                   # to remove the q from the results
                x.append(res["sbert_ita_3d"][0])
                y.append(res["sbert_ita_3d"][1])
                z.append(res["sbert_ita_3d"][2])
                ids.append(res["id"])
                
        df = pd.DataFrame(results)
        df = df[["score", "id", "word", "meaning"]]
        
        doc = self.es.find_by_id(id, ["word", "meaning", "sbert_ita_3d"])

    
        q = {"x": [doc["sbert_ita_3d"][0]], "y": [doc["sbert_ita_3d"][1]], "z":[doc["sbert_ita_3d"][2]], "labels": [id], "docs": [id], "legend": "query", "color":"orange"}
        dots_2 = {"x": x, "y":y, "z":z, "labels": ids, "docs": ids, "legend": "knn", "color":"blue"}
        fig = plot_multilegend([q, dots_2])
        return df, fig
    
    
    def mod_3(self, ids, scope):
        is_custom = None
        if scope == "custom definitions":
            is_custom = True
        elif scope == "Treccani definitions":
            is_custom = False
        
        dfs = list()
        docs = []
        x, y, z, identifiers = [], [], [], []
        for id in ids:  
            docs.append(self.es.find_by_id(id, ["meaning"])["meaning"])
            results = self.es.knn_by_id(id, fields=["word", "meaning", "sbert_ita_3d"], is_custom=is_custom)
            df = pd.DataFrame(results)
            df = df[["score", "id", "word", "meaning"]]
            dfs.append(df)
        
            for res in results:
                if res["id"] not in ids:
                    x.append(res["sbert_ita_3d"][0])
                    y.append(res["sbert_ita_3d"][1])
                    z.append(res["sbert_ita_3d"][2])
                    identifiers.append(res["id"])
            
            
        q_x, q_y, q_z  = [], [], []
        for id in ids:
            doc = self.es.find_by_id(id, ["word", "meaning", "sbert_ita_3d"])
            q_x.append(doc["sbert_ita_3d"][0])
            q_y.append(doc["sbert_ita_3d"][1])
            q_z.append(doc["sbert_ita_3d"][2])

    
        qs = {"x": q_x, "y": q_y, "z":q_z, "labels": ids, "docs": ids, "legend": "query", "color":"orange"}
        dots_2 = {"x": x, "y":y, "z":z, "labels": identifiers, "docs": identifiers, "legend": "knn", "color":"blue"}
        fig = plot_multilegend([qs, dots_2])
        return docs, dfs, fig
    
    
    
    def mod_4(self, input_def, scope):
        is_custom = None
        if scope == "custom definitions":
            is_custom = True
        elif scope == "Treccani definitions":
            is_custom = False
            
        model_hf = "nickprock/sentence-bert-base-italian-uncased"
        input_def_emb = self.models.get_embeddings([input_def], model_hf).squeeze().tolist()

        results = self.es.knn_by_embedding(input_def_emb, fields=["word", "meaning", "sbert_ita"], is_custom=is_custom)
        df = pd.DataFrame(results)
        df = df[["score", "id", "word", "meaning"]]
        return df
    
    
    def employee_coherence(self, employee):
        results = self.es.find_by_author(employee, ["word", "meaning"])
        ids = [res["id"] for res in results]
        labels = [ id[:id.find("_"):] +  id[id.rfind("_"):] for id in ids]
        words = [res["word"] for res in results]
        
        dfs = {"abandonware":[], "opinionated":[], "ownership":[], "evangelismo":[]}
        x, y, z, identifiers = [], [], [], []
        for id, word in zip(ids, words):  
            results = self.es.knn_by_id(id, fields=["word", "meaning", "sbert_ita_3d"], is_custom=False)
            df = pd.DataFrame(results)
            df = df[["score", "id", "word", "meaning"]]

            dfs[word].append({"doc": self.es.find_by_id(id, ["meaning"])["meaning"], "df": df})
        
            for res in results:
                if res["id"] not in ids:
                    x.append(res["sbert_ita_3d"][0])
                    y.append(res["sbert_ita_3d"][1])
                    z.append(res["sbert_ita_3d"][2])
                    identifiers.append(res["id"])
            
            
        q_x, q_y, q_z  = [], [], []
        for id in ids:
            doc = self.es.find_by_id(id, ["word", "meaning", "sbert_ita_3d"])
            q_x.append(doc["sbert_ita_3d"][0])
            q_y.append(doc["sbert_ita_3d"][1])
            q_z.append(doc["sbert_ita_3d"][2])

    
        qs = {"x": q_x, "y": q_y, "z":q_z, "labels": labels, "docs": ids, "legend": "query", "color":"orange"}
        dots_2 = {"x": x, "y":y, "z":z, "labels": identifiers, "docs": identifiers, "legend": "knn", "color":"blue"}
        fig = plot_multilegend([qs, dots_2])
        return dfs, fig
    
    