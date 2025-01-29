# Sentiment and Semantic Shift Analysis  

This project investigates **sentiment analysis** and **semantic shift** in the conceptualization of key terms within the [Datasinc](https://www.datasinc.it/) team. By leveraging **pre-trained language models**, the goal is to numerically demonstrate how human communication is inherently distorted and how information transmission is imperfect. The analysis is **visual, interactive, and qualitative**, utilizing vector space representations, including definitions sourced from the Treccani dictionary, as a semantic reference. The data considered is in Italian langauge.

For details on the methodology, refer to the **PDF** in the project root.  

## Analyzed Concepts  

- Abandomware  
- Evangelismo  
- Opinionated  
- Ownership  

## Methodology  

### Sentiment Analysis  
Sentiment classification is performed using **pre-trained BERT-based models**, fine-tuned on datasets like Sentipolc EVALITA 2016 and multilingual tweet corpora. These models assess sentiment polarity (**positive, neutral, negative**) across definitions and participant interpretations.  

### Semantic Analysis  
Semantic shift is analyzed through **Sentence-BERT (SBERT)**, using **cosine similarity** to measure the conceptual distance between different representations of the same term. Treccani definitions serve as a **semantic anchor**, providing a stable reference point.  

## Deployment  

```sh  
python3 -m venv venv  
source venv/bin/activate  
pip3 install -r requirements.txt  
docker-compose up  
python3 src/pipeline.py  # Runs the vectorization and indexing pipeline  
streamlit run src/app.py  # Launches the Streamlit app for visualization  
```  

## Limitations & Future Work  

### Human Limitations  
- **Exhaustivity**: Do written responses fully capture participants' understanding?  
- **Expressivity**: Are responses formulated clearly?  
- **Commitment**: Did participants engage seriously?  

### Model Limitations  
- Sentiment analysis models were trained on **tweets**, not definitions.  
- Semantic similarity was measured using **SBERT**, not fine-tuned on dictionary definitions.  

### Future Directions  
- Fine-tune **SBERT** on curated definitions to improve semantic similarity detection.  
- Leverage **LLMs** to rephrase Treccani definitions for better alignment.  
- Explore **prompt-based sentiment scoring** for richer insights.  