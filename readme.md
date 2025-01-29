# Sentiment Analysis
Questo progetto analizza il sentiment analysis e l'analisi semantica mostrando lo shift semantico che sussiste tra le diverse concettualizzazioni di un concetto noto x per il team Datasinc. L'analisi fornita è visuale, interattiva e qualitativa.
Per fornire uno spazio vettoriale in cui orientarsi semanticamente sono state aggiunte le rappresentazioni di definizioni prese dalla Treccani.
Per i fondamenti sul metodo usato fare riferimento al PDF nella root del progetto.

## Concetti analizzati

- abandomware
- evangelismo
- opinionated
- ownership

## persone coinvolte
- Renzo
- Francesco Braggiotti
- Francesco Gamondi
- Raffaele
- Giulio
- Andrea 
- Daniele
- Nicola

## Deployment

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements
$ docker-compose up
$ python3 src/pipeline.py  # esegue la pipeline di vettorizzazione e indexing
$ streamlit run src/app.py  # lancia l'app streamlit per visualizzare i risultati

```