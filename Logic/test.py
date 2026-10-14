import json;
import requests;
from pathlib import Path;

def exp():
    Url = "https://www.animedubhindi.link/wp-json/wp/v2/posts"

    BASE_DIR = Path(__file__).resolve().parent.parent

    anime_li = []

    for page in range (1,4):
        page = 1
        params = {
            "perpage": 20,
            "page": page,
            "_embed": "true"
        }

        response = requests.get( Url,
            params=params, timeout=15
        )

        posts = response.json()

        for post in posts:
            Title = post["title"]["rendered"]
            link = post["link"]
            coverImage = post["_embedded"]["wp:featuredmedia"][0]["source_url"]

        anime_li.append({"Title":Title, "Link":link, "Cover":coverImage}) 

    return anime_li

call = exp()
print(call)