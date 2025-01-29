from elasticsearch import Elasticsearch
from datetime import datetime
from pprint import pprint
import pandas as pd
from elasticsearch.helpers import scan
class ES:
    
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")
        self.INDEX = "words_ok"
        
        if not self.es.indices.exists(index=self.INDEX):
            mappings = {
                "properties": {
                    "id": {"type": "text", "analyzer": "standard"},
                    "word": {"type": "completion", "analyzer": "standard"},
                    "meaning": {"type": "text", "analyzer": "italian"},
                    "umberto": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "cosine"},
                    "umberto_3d": {"type": "dense_vector", "dims": 3},
                    "sbert_ita": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "cosine"},
                    "sbert_ita_3d": {"type": "dense_vector", "dims": 3},
                    "is_custom": {"type": "boolean", "index": True},
                    "author": {"type": "text", "index": True},
                    "version": {"type": "integer"}
                    }
                }
            self.create_index(mappings, self.INDEX)


    ################ WRITE #################################

    def create_index(self, mappings, index_name):
        self.es.indices.create(index=index_name, mappings=mappings)
            

    def reindex_docs(self, source_index_name, dest_index_name):
        reindex_query = {
            "source": {
                "index": source_index_name,
                "_source": {
                    "excludes": ["sbert_ita", "sbert_ita_3d"]
                }
            },
            "dest": {
                "index": dest_index_name
            }
        }
        response = self.es.reindex(**reindex_query, request_timeout=60)
        pprint(response)
           

    def insert(self, word, meanings, is_custom, author = None):  
        if meanings:
            for count, meaning in enumerate(meanings):   
                id = word+"_"+str(count+1) 
                doc = dict()
                if is_custom:
                    id = word+"_" + author + "_" +str(count+1) 
                    doc["word"] = word
                    doc["meaning"] = meaning
                    doc["is_custom"] = is_custom
                    doc["author"] = author
                    doc["version"] = count+1
                else:
                    id = word+"_"+str(count+1) 
                    doc["word"] = word
                    doc["meaning"] = meaning
                    doc["is_custom"] = is_custom
                
                resp = self.es.index(index=self.INDEX, id=id, document=doc)
        
    
    def update_embedding(self, id, embedding_field, embedding):
        update_query = {
            "doc": { embedding_field: embedding }
        }
        self.es.update(index=self.INDEX, id=id, body=update_query)


    def update_is_custom(self, id, is_custom):
        update_query = {
            "doc": { "is_custom": is_custom }
        }
        self.es.update(index=self.INDEX, id=id, body=update_query)

        
        
        
    def delete_field_from_all_docs(self, field):
        all_documents = scan(self.es, index=self.INDEX)
        for document in all_documents:
            doc_id = document["_id"]
            doc_source = document["_source"]

            # Remove the specified field
            if field in doc_source:
                print(doc_id)
                del doc_source[field]

                # Update the document
                self.es.update(index=self.INDEX, id=doc_id, body={"doc": doc_source})


    ######################## READ ######################################à

    # filter contiene una dupla (chiave, valore) che serve per tenere solo i documenti che posseggono la chiave con quello specifico valore
    # se il valore in filter è None allora un documento per essere incluso non deve contenere tale key
    # la key coinvolta nel filter deve essere  presente in pre_filter_fields
    # output_fields sono i campi che i documenti finali conterranno.
    def get_all_docs(self, pre_filter_fields=None, filter=None, output_fields=None):
        results  = []
        res = scan(self.es, index=self.INDEX, _source=pre_filter_fields)
        for el in res:
            
            if filter:
                if filter[1]== None and filter[0] in el["_source"].keys():
                    continue
                if filter[1]!= None and filter[0] not in el["_source"].keys():
                    continue
                if filter[1]!= None  and  filter[1] != el["_source"][filter[0]]:
                    continue
            
            doc = {"id": el["_id"]}
            for field in output_fields:
                if field in el["_source"].keys():
                    doc[field] = el["_source"][field]
            results.append(doc)
        return results


    def find_by_word(self, word, fields):
        search_query = {
            "query": {
                "term": {
                    "word": {
                        "value": word
                    }
                }
            }
        }   
        
        results = []
        res = self.es.search(index=self.INDEX, body=search_query, _source_includes=fields,size=20)  
        res = res["hits"]["hits"]
        if len(res)>0:
            for el in res:
                doc = {"id": el["_id"]}
                for field in fields:
                    doc[field] = el["_source"][field]
                results.append(doc)     
            return results
        else:
            return None



    def find_by_author(self, author, fields, version=None):
        if version:
            search_query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "author": {
                                        "value": author
                                    }
                                }
                            },
                            {
                                "term": {
                                    "version": {
                                        "value": version  # Replace with the specific version value you want to filter on
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        else:
            search_query = {
            "query": {
                "term": {
                    "author": {
                        "value": author
                    }
                }
            }
        }   
                    
                    
        results = []
        res = self.es.search(index=self.INDEX, body=search_query, _source_includes=fields)  
        res = res["hits"]["hits"]
        if len(res)>0:
            for el in res:
                doc = {"id": el["_id"]}
                for field in fields:
                    doc[field] = el["_source"][field]
                results.append(doc)     
            return results
        else:
            return None



    def find_by_is_custom(self, is_custom, fields):
        search_query = {
            "query": {
                "term": {
                    "is_custom": is_custom
                }
            }
        }   
        results = []
        res = self.es.search(index=self.INDEX, body=search_query, _source_includes=fields)  
        res = res["hits"]["hits"]
        if len(res)>0:
            for el in res:
                doc = {"id": el["_id"]}
                for field in fields:
                    doc[field] = el["_source"][field]
                results.append(doc)     
            return results
        else:
            return None
 
        

    def find_by_id(self, id, fields):
        result = self.es.get(index=self.INDEX, id=id,  _source_includes=fields, ignore=404)
        if result["found"]:
            return result["_source"]
        else:
            return None


    def suggest(self, user_input):
        suggest_query = {
            "suggest": {
                "words-suggest": {
                    "prefix": user_input,
                    "completion": {
                        "field": "word",
                        "size": 50
                    }
                }
            }
        }
        return_fields = ["word"]

        results = self.es.search(index=self.INDEX, body=suggest_query, _source_includes=return_fields)
        results = results['suggest']["words-suggest"][0]['options']
        suggestions = list(set( [res["_source"]["word"] for res in results]))
        suggestions.sort()
        return suggestions


    def exist_word(self, word):
        search_query = {
            "query": {
                "term": {
                    "word": {
                        "value": word
                    }
                }
            }
        }   
        
        response = self.es.search(index=self.INDEX, body=search_query)      
        if response["hits"]["total"]["value"]==0:
            return False
        return True
    

    def knn_by_id(self, user_input, fields, is_custom):
        doc = self.find_by_id(user_input, ["word", "sbert_ita"])
        if is_custom == None:
            es_query = {
            "size":25,
            "knn": {
                "field": "sbert_ita",
                "query_vector": doc["sbert_ita"],
                "k": 25,
                "num_candidates": 200,
            }
            }
        else:
            es_query = {
            "size":25,
            "knn": {
                "field": "sbert_ita",
                "query_vector": doc["sbert_ita"],
                "k": 25,
                "num_candidates": 200,
                "filter": {
                    "term": {
                        "is_custom": is_custom
                    }
                }
            }
            }

        results = self.es.search(index=self.INDEX, body=es_query, _source_includes=fields)
        results = results["hits"]["hits"]  
        outs = list()
        for result in results:
            out = { "score": result["_score"], "id": result["_id"]}
            for field in fields:
                out[field] = result["_source"][field]
            outs.append(out)
        return outs          



    def knn_by_embedding(self, input_embedding, fields, is_custom):
        if is_custom == None:
            es_query = {
            "size":35,
            "knn": {
                "field": "sbert_ita",
                "query_vector": input_embedding,
                "k": 35,
                "num_candidates": 200,
            }
            }
        else:
            es_query = {
            "size":35,
            "knn": {
                "field": "sbert_ita",
                "query_vector": input_embedding,
                "k": 35,
                "num_candidates": 200,
                "filter": {
                    "term": {
                        "is_custom": is_custom
                    }
                }
            }
            }

        results = self.es.search(index=self.INDEX, body=es_query, _source_includes=fields)
        results = results["hits"]["hits"]  
        outs = list()
        for result in results:
            out = { "score": result["_score"], "id": result["_id"]}
            for field in fields:
                out[field] = result["_source"][field]
            outs.append(out)
        return outs          

        

es = ES()
# # mappings = {
# #         "properties": {
# #             "id": {"type": "text", "analyzer": "standard"},
# #             "word": {"type": "text", "analyzer": "standard"},
# #             "meaning": {"type": "text", "analyzer": "italian"},
# #             "umberto": {"type": "dense_vector", "dims": 768},
# #             "umberto_3d": {"type": "dense_vector", "dims": 3},
# #             "sbert_ita": {"type": "dense_vector", "dims": 768},
# #             "sbert_ita_3d": {"type": "dense_vector", "dims": 3}
# #             }
# #         }
#es.create_index(mappings, "tmp")
#es.reindex_docs("words", "words_ok")
#es.delete_field_from_all_docs("sbert_ita")
#res = es.find_by_word("tavolo", ["word"])

# es.knn("gatto")
# results = es.get_all_docs(["word", "is_custom"], ("is_custom", None), ["word"])
# print(len(results))
# for el in results:
#     es.update_is_custom(el["id"], False)


print(es.find_by_author("sperto",  ["word"]))
