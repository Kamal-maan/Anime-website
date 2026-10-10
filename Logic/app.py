from flask import Flask, render_template, redirect, url_for, session, Response;
import requests;
import json;
import time;
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "Templates"),
    static_folder=str(BASE_DIR / "Static")
)

def exp():
    url = "https://graphql.anilist.co"

    i = 1
    anime_list=[]

    while i < 3:
        query = f"""
        query {{
            Page(page:{i}, perPage:100){{
                media(type: ANIME){{
                    siteUrl
                    title{{
                        english
                        romaji
                    }}
                    episodes
                    coverImage{{
                        large
                    }}
                }}
            }}
        }}
        """
        i+= 1

        response = requests.post(
        url, json={"query": query},
        timeout=15
        )
        response.raise_for_status()
        anime = response.json()["data"]["Page"]["media"]
        anime_list.extend(anime)

    return anime_list

def animo():
    url = "https://graphql.anilist.co"

    anime_lo = []

    with open(BASE_DIR / "Data" / "anime.json", "r", encoding="utf-8") as File:
        titles = json.load(file)

    for title in titles:
        query = f"""
        query{{
            Page{{
                media(search: "{title}", type: ANIME){{
                            siteUrl
                            title{{
                            english
                            romaji
                            }}
                            coverImage{{
                            large
                            }}
                            episodes
                }}
            }}
        }}
        """

        time.sleep(1)

        response = requests.post(
            url, json={"query": query},
            timeout=15
        )

        response.raise_for_status()
        anime = response.json()["data"]["Page"]["media"]
        anime_lo.extend(anime)

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

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)