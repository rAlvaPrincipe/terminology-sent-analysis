from transformers import pipeline
from transformers import AutoTokenizer, AutoModel
import torch


class Model():

    pipelines_names = ["neuraly/bert-base-italian-cased-sentiment", "citizenlab/twitter-xlm-roberta-base-sentiment-finetunned", "neuraly/bert-base-italian-cased-sentiment", "lxyuan/distilbert-base-multilingual-cased-sentiments-student", "cardiffnlp/twitter-xlm-roberta-base-sentiment"]
    embedders_names = ["nickprock/sentence-bert-base-italian-uncased"] #"bert-base-uncased",]

    def __init__(self):
        self.pipelines = dict()
        self.embedders = dict()
        self.tokenizers = dict()
        
        for pipeline_name in self.pipelines_names:
            p = pipeline("text-classification",model=pipeline_name,top_k=3, device=0)#, device=0)
            self.pipelines[pipeline_name] = p
            
        for embedder_name in self.embedders_names:
            if embedder_name == "nickprock/sentence-bert-base-italian-uncased":
                self.tokenizers[embedder_name] = AutoTokenizer.from_pretrained(embedder_name)
            else:
                self.tokenizers[embedder_name] = AutoTokenizer.from_pretrained(embedder_name)     
            m = AutoModel.from_pretrained(embedder_name, output_hidden_states = True).to("cuda")
            self.embedders[embedder_name] = m
            
            
    def list_pipelines(self):
        return list(self.pipelines.keys())
    
    def list_embedders(self):
        return list(self.embedders.keys())
            
    def get_pipeline(self, name):
        return self.pipelines[name]

    def get_tokenizer(self, name):
        return self.tokenizers[name]
    
    def get_embedder(self, name):
        return self.embedders[name]
    

    def get_sentiment(self, docs, model_name):
        #classifier = pipeline("text-classification",model=model_name,top_k=3)
        predictions = self.pipelines[model_name](docs)    
        positives, neutrals, negatives = [], [], []
        for prediction in predictions:
            for el in prediction:
                if el["label"].lower() == "positive":
                    positives.append(el["score"])
                elif el["label"].lower() == "neutral":
                    neutrals.append(el["score"])
                elif el["label"].lower() == "negative":
                    negatives.append(el["score"])  
        return positives, negatives, neutrals
        
        

    def get_embeddings(self, docs, model_name, is_pooled_output=False):
        tokenizer = self.tokenizers[model_name]
        embedder = self.embedders[model_name]
        encodings = tokenizer(docs, truncation=True, padding=True, max_length=512, add_special_tokens=True, return_tensors='pt')
        with torch.no_grad():
            outputs = embedder(input_ids=encodings["input_ids"].to("cuda"), attention_mask=encodings["attention_mask"].to("cuda"))
            if is_pooled_output:
                return outputs.pooler_output
            else:
                return  outputs.last_hidden_state[:, 0, :] 
                


# def embeddings_to_plot(self, docs, model_name, is_pooled_output, reduction_alg):
#     embeddings = self.get_embeddings(docs, model_name, is_pooled_output)
#     embeddings = self.dim_reduction(reduction_alg, embeddings, 3)
#     return list(embeddings[:,0]), list(embeddings[:,1]), list(embeddings[:,2])
    
