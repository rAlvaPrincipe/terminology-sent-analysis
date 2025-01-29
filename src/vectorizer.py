from models import Model
from es import ES
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from reductor import reductor_fit_transform

def vectorize_and_load(batch_size, model_name):
    es = ES()
    models = Model()
    es_docs = es.get_all_docs(["word", "meaning"], None, ["word", "meaning"])
    docs = [ es_doc["meaning"] for es_doc in es_docs]
    ids = [ es_doc["id"] for es_doc in es_docs]
    
    docs_batch = []
    ids_batch = []

    for id, doc in zip(ids, docs):
        ids_batch.append(id)
        docs_batch.append(doc)
        
        if len(docs_batch) == batch_size:
            batch_embeddings = models.get_embeddings(docs_batch, model_name)
            for id, embedding in zip(ids_batch, batch_embeddings):
                print(id, embedding.shape)
                es.update_embedding(id, "sbert_ita", embedding.tolist())
            batch_embeddings = []
            docs_batch = []
            ids_batch = []
            print()

    # Process the remaining documents in the last batch
    if docs_batch:
        batch_embeddings = models.get_embeddings(docs_batch, model_name)
        for id, embedding in zip(ids_batch, batch_embeddings):
            print(id, embedding.shape)
            es.update_embedding(id, "sbert_ita", embedding.tolist())
         
         
def reduce_and_load(embedder_label):
    es = ES()
    results = es.get_all_docs( [embedder_label], None,  [embedder_label])
    ids = [res["id"] for res in results]
    embeddings = [res[embedder_label] for res in results]
    embedding_size = len(embeddings[0])
   
    embeddings = np.array(embeddings)
    embeddings = embeddings.reshape(-1, embedding_size)
    embeddings3d = reductor_fit_transform("tsne", embeddings, 3)
    
    for id, embedding3d in zip(ids, embeddings3d):
        es.update_embedding(id, "sbert_ita_3d", embedding3d)





#vectorize(120, "nickprock/sentence-bert-base-italian-uncased")
# reduce("sbert_ita")