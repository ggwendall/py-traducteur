from transformers import pipeline
from config.parametres import VERSIONS
from model.prompt import Prompt

def traduire(prompt:Prompt) :
    if prompt.version == VERSIONS[0] :
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
    elif prompt.version == VERSIONS[1]:
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
    else:
        return "La version de traduction est incorrecte."
    prompt.traduction = translator(prompt.atraduire)[0]['translation_text']
    return(prompt)
    