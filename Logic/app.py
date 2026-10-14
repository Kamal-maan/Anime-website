from flask import Flask, render_template, redirect, url_for, session, Response;
import requests;
import json;
import time;
from pathlib import Path;
from livereload import Server;

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "Templates"),
    static_folder=str(BASE_DIR / "Static")
)

def exp():
    Url = "https://www.animedubhindi.link/wp-json/wp/v2/posts"

    anime_li = []

    with requests.Session() as session:
        for page in range (1,3):
            params = {
                "per_page": 20,
                "page": page,
                "_embed": "true"
            }

            response = session.get( Url,
                params=params, timeout=15
            )

            posts = response.json()
            response.raise_for_status()

            for post in posts:
                Title = post.get("title", {}).get("rendered")
                link = post.get("link")
                media = post.get("_embedded", {}).get("wp:featuredmedia", [])
                cover = media[0].get("source_url") if media else None

                anime_li.append({"Title":Title, "Link":link, "Cover":cover})

    return anime_li 
        

def animo():
    Url = "https://www.animedubhindi.link/wp-json/wp/v2/posts"

    anime_lo = []

    with open(BASE_DIR / "Data" / "anime.json", "r", encoding="utf-8") as file:
        name = json.load(file)

    with requests.Session() as sussion:
        for title in name:
            print(title)

            params={
                "search": title,
                "_embed": "true"
            }

            response = sussion.get(Url,
                params=params
            )

            posts = response.json()

            for post in posts:
                Title = post["title"]["rendered"]
                coverImage = post["_embedded"]["wp:featuredmedia"][0]["source_url"]
                link = post["link"]

                anime_lo.append({"Title": Title, "Cover": coverImage, "Link": link})

        return anime_lo

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/anime", methods=["GET"])
def anime():
    explore = exp()
    return render_template("Anime.html", anime_list=explore)

@app.route("/manga")
def manga():
    return render_template("Manga.html")

@app.route("/support")
def support():
    return render_template("Support.html")

@app.route("/masterpiece", methods = ["GET"])
def master():
    uno = animo()
    return render_template("Masterpiece.html", anime_list=uno)