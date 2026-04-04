import requests
import time

JIKAN_BASE = "https://api.jikan.moe/v4"

def search_anime(query):
    try:
        response = requests.get(f"{JIKAN_BASE}/anime", params={"q": query, "limit": 1})
        time.sleep(0.4)  # stay under 3 requests/second
        if response.status_code != 200:
            return None
        
        data = response.json()
        if not data["data"]:
            return None

        anime = data["data"][0]
        return {
            "title_english": anime.get("title_english") or anime.get("title"),
            "title_japanese": anime.get("title_japanese"),
            "score": anime.get("score"),
            "genres": [g["name"] for g in anime.get("genres", [])],
            "mal_id": anime.get("mal_id")
        }
    except requests.exceptions.RequestException:
        return None


def is_confident_match(query, result):
    if result is None:
        return False
    
    query_lower = query.lower()
    english = (result["title_english"] or "").lower()
    japanese = (result["title_japanese"] or "").lower()

    return query_lower in english or query_lower in japanese