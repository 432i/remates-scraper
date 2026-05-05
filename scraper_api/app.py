from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import time

app = FastAPI()

cache = None
last_fetch = 0

def scrape():
    results = []
    page = 1
    id = 1

    while True:
        url = f"https://www.rematesinmobiliarios.cl/page/{page}/"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if res.status_code != 200:
            break

        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.select("article")  # ajustar

        if not cards:
            break

        for c in cards:
            text = c.get_text()

            results.append({
                "id": id,
                "tipo": "N/A",
                "region": "N/A",
                "comuna": "N/A",
                "direccion": c.select_one("h2, h3").get_text(strip=True) if c.select_one("h2, h3") else "",
                "metros2": None,
                "habitaciones": None,
                "precio_uf": "",
                "precio_clp": "",
                "fecha_remate": "",
                "avaluo_comercial_uf": None,
                "postura_min_uf": None
            })
            id += 1

        page += 1
        if page > 20:
            break

    return results


@app.get("/remates")
def get_data():
    global cache, last_fetch

    now = time.time()

    if cache and now - last_fetch < 600:
        return cache

    data = scrape()
    cache = data
    last_fetch = now

    return data