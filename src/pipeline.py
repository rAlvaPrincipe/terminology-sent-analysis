from definitions import scrape_vocabulary
from lemmatizer import vocabulary2lemmas
from vectorizer import vectorize_and_load
from vectorizer import reduce_and_load
from definitions import load_custom_defs

def main():
    vocab_path = 'data/60000_parole_italiane.txt'
    lemmas_path = 'data/60k_lemmas.txt'
    vocabulary2lemmas(vocab_path, lemmas_path)
    scrape_vocabulary(lemmas_path)
    load_custom_defs()
    vectorize_and_load(120, "nickprock/sentence-bert-base-italian-uncased")
    reduce_and_load("sbert_ita")
    



if __name__ == "__main__":
    main()
