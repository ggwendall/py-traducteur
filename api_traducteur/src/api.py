from fastapi import FastAPI, Request
import uvicorn

from config.parametres import VERSIONS
from model.nlp import traduire
from model.prompt import Prompt
from dto.service_traducteur import Service_Traducteur as st
from model.utilisateur import Utilisateur
from prometheus_fastapi_instrumentator import Instrumentator
import time
from prometheus_client import Counter


tags =[
       {
         "name":"index",
         "description":"Index"     
       },
     {
          "name":"traduction",
          "description":"Traduction"
     },
     {
          "name":"authentification",
          "description":"authentification"
     }
]

app = FastAPI(
     title="Appli de traduction",
     description="API de traudction",
     version="1.0.0",
     openapi_tags = tags
)

http_errors = Counter("http_errors", "HTTP errors", ["http_status"])

Instrumentator().instrument(app).expose(app)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    http_errors.labels(http_status=response.status_code).inc()

    # Appeler la méthode enregistrer_metric pour sauvegarder les métriques
    try:
        st.enregistrer_metric(endpoint=request.url.path, method=request.method, duration=duration, status_code=response.status_code)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la métrique : {e}")

    return response

@app.get("/versions", tags=["index"])
def versions():
        return VERSIONS

@app.post("/traductions", tags=["traduction"])
def traducteur(prompt:Prompt):
        traduire(prompt)
        st.sauvegarder_prompt(prompt)
        return prompt

@app.get("/traductions/auteur/{id}", tags=["traduction"])
def versions_par_auteur(id:int):
       return st.lister_prompts(id)

@app.post("/login", tags=["authentification"])
def authentifier(utilisateur:Utilisateur):
       st.verifier_login(utilisateur)
       return {"authentifié" : utilisateur.authentifie, "id":utilisateur.id}

if __name__ == "__main__" :
    uvicorn.run(app, host="0.0.0.0", port=8080)