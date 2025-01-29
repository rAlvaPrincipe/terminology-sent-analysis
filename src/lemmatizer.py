import requests
import json
import sys
from pprint import pprint 


def tint(text, format_='json', baseurl='http://127.0.0.1:8012/tint'):
    if len(text) > 0:
        payload = {
            'text': text,
            'format': format_
        }
        res = requests.post(baseurl, data=payload)
        if res.ok:
            # success
            return json.loads(res.text)
        else:
            return None
    else:
        print('WARNING: Tint Server Wrapper got asked to call tint with empty text.', file=sys.stderr)
        return None, None
    
    
def get_lemmas(res):
    try:
        lemmas_raw = res["sentences"][0]["tokens"][0]["full_morpho"] 
        lemmas = lemmas_raw.split()
        out = set()
        if len(lemmas) == 1:
            return {lemmas[0]}
        elif len(lemmas) > 1:
            out = set()
            for lemma in lemmas[1:]:
                if "+" in lemma:
                    out.add(lemma[:lemma.index("+")])
                else:
                    print("error +")
            return out
        else:
            print("error return None")
            return set()
    except:
        print("error")
        return set()



def vocabulary2lemmas(path_input, path_output):
    with open(path_input, 'r') as file:
        words = file.read().splitlines()
        lemmas = set()
        for word in words:
            res = tint(word)
            lemmas.update(get_lemmas(res))
        
    with open(path_output, 'w') as file:
        for lemma in lemmas:
            file.write(lemma + '\n')
    

