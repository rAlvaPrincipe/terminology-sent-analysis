import torch
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import joblib
import os 



def reductor_fit_transform(alg, embeddings, n_components):
    if not os.path.exists("./reducers"): 
        os.makedirs("./reducers")
        
    if type(embeddings) == torch.Tensor:
        embeddings = embeddings.cpu()
    if alg == "tsne":
        tsne = TSNE(n_components=n_components, random_state=0) #, perplexity=5)
        reduced_embeddings = tsne.fit_transform(embeddings)
    elif alg == "pca":
        pca = PCA(n_components=n_components)
        reduced_embeddings = pca.fit_transform(embeddings)
    return reduced_embeddings


        
    # def embeddings_to_plot(self, docs, model_name, is_pooled_output, reduction_alg):
    #     embeddings = self.get_embeddings(docs, model_name, is_pooled_output)
    #     embeddings = self.dim_reduction(reduction_alg, embeddings, 3)
    #     return list(embeddings[:,0]), list(embeddings[:,1]), list(embeddings[:,2])
        
