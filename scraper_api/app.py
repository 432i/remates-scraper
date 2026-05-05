from fastapi import FastAPI
import requests
import time

cache = None
last_fetch = 0


app = FastAPI()

URL = "https://www.rematesinmobiliarios.cl/api-remates.php"

@app.get("/remates")
def get_remates():
    global cache, last_fetch
    now = time.time()
    if cache and now - last_fetch < 56000:
        return cache
    
    res = requests.get(URL, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    })

    data = res.json()
    cache = data
    last_fetch = now
    # opcional: transformar aquí
    return data