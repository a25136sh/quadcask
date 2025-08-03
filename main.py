import os
import csv
import json
import requests
import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Whisky(BaseModel):
    purchased: Optional[str]
    name: str
    price: str
    store: Optional[str]
    category: str
    country: str
    flavor: str
    critic: str
    score: Optional[int]
    cost: str
    reviewers: str
    cluster: str
    type: str
    stdev: str


@app.get("/database")
async def database():
    with open('whisky_database.csv', encoding='UTF-8') as f:
        reader = csv.reader(f)
        whiskies = []
        for i, line in enumerate(reader):
            if i == 0:
                continue
            whiskies.append({
                "name": line[0],
                "critic": line[1],
                "stdev": line[2],
                "reviewers": line[3],
                "cost": line[4],
                "category": line[5],
                "cluster": line[6],
                "flavor": line[7],
                "country": line[8],
                "type": line[9]
            })
    return whiskies


@app.get("/exchange")
async def exchange():
    if os.path.exists("exchange_cache.json"):
        last = datetime.fromtimestamp(os.path.getmtime("exchange_cache.json"))
        if datetime.now() - last < timedelta(days=1):
            with open("exchange_cache.json", "r", encoding="UTF-8") as f:
                return json.load(f)
    url = "https://forex-api.coin.z.com/public/v1/ticker"
    response = requests.get(url)
    cad_jpy = next(
        filter(lambda x: x["symbol"] == "CAD_JPY", response.json()["data"])
    )
    with open("exchange_cache.json", "w", encoding="UTF-8") as f:
        json.dump(cad_jpy, f)
    return cad_jpy


@app.put("/storage")
async def update_storage(whiskies: List[Whisky]):
    conn = sqlite3.connect("storage.sqlite3")
    cur = conn.cursor()
    cur.execute("""DELETE FROM storage""")
    for whisky in whiskies:
        cur.execute(f"""
            INSERT INTO storage values(
                '{whisky.purchased}',
                '{whisky.name}',
                '{whisky.price}',
                '{whisky.store}',
                '{whisky.category}',
                '{whisky.country}',
                '{whisky.flavor}',
                '{whisky.critic}',
                '{whisky.score}',
                '{whisky.cost}',
                '{whisky.reviewers}',
                '{whisky.cluster}',
                '{whisky.type}',
                '{whisky.stdev}'
            )
        """)
    conn.commit()
    conn.close()
    print(whiskies)
    return "ok"


@app.get("/storage")
async def get_storage():
    conn = sqlite3.connect("storage.sqlite3")
    cur = conn.cursor()
    whiskies = []
    for whisky in cur.execute("select * from storage"):
        whiskies.append({
            "purchased": whisky[0],
            "name": whisky[1],
            "price": str(whisky[2]),
            "store": whisky[3],
            "category": whisky[4],
            "country": whisky[5],
            "flavor": whisky[6],
            "critic": str(whisky[7]),
            "score": whisky[8],
            "cost": whisky[9],
            "reviewers": str(whisky[10]),
            "cluster": whisky[11],
            "type": whisky[12],
            "stdev": str(whisky[13])
        })
    conn.close()
    return whiskies


@app.put("/wishlist")
async def update_wishlist(whiskies: List[Whisky]):
    conn = sqlite3.connect("storage.sqlite3")
    cur = conn.cursor()
    cur.execute("""DELETE FROM wishlist""")
    for whisky in whiskies:
        cur.execute(f"""
            INSERT INTO wishlist values(
                '{whisky.name}',
                '{whisky.price}',
                '{whisky.category}',
                '{whisky.country}',
                '{whisky.flavor}',
                '{whisky.critic}',
                '{whisky.cost}',
                '{whisky.reviewers}',
                '{whisky.cluster}',
                '{whisky.type}',
                '{whisky.stdev}'
            )
        """)
    conn.commit()
    conn.close()
    print(whiskies)
    return "ok"


@app.get("/wishlist")
async def get_wishlist():
    conn = sqlite3.connect("storage.sqlite3")
    cur = conn.cursor()
    whiskies = []
    for whisky in cur.execute("select * from wishlist"):
        whiskies.append({
            "name": whisky[0],
            "price": str(whisky[1]),
            "category": whisky[2],
            "country": whisky[3],
            "flavor": whisky[4],
            "critic": str(whisky[5]),
            "cost": whisky[6],
            "reviewers": str(whisky[7]),
            "cluster": whisky[8],
            "type": whisky[9],
            "stdev": str(whisky[10])
        })
    conn.close()
    return whiskies


app.mount(
    "/",
    StaticFiles(directory="frontend/dist", html=True),
    name="static"
)


if not os.path.exists("storage.sqlite3"):
    conn = sqlite3.connect("storage.sqlite3")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE storage(
            purchased STRING,
            name STRING,
            price STRING,
            store STRING,
            category STRING,
            country STRING,
            flavor STRING,
            critic STRING,
            score STRING,
            cost STRING,
            reviewers STRING,
            cluster STRING,
            type STRING,
            stdev STRING
        )
    """)
    cur.execute("""
        CREATE TABLE wishlist(
            name STRING,
            price STRING,
            category STRING,
            country STRING,
            flavor STRING,
            critic STRING,
            cost STRING,
            reviewers STRING,
            cluster STRING,
            type STRING,
            stdev STRING
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", reload=True)
