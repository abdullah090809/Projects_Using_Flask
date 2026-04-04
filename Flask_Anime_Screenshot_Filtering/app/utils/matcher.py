def match_against_watchlist(anime,watchlist):
    if anime is None:
        return None
    english = (anime["title_english"] or "").lower()
    japanese=(anime["title_japanese"] or "").lower()
    for entry in watchlist:
        entry_name=entry["name"].lower()
        if entry_name in english or entry_name in japanese or \
        english in entry_name or japanese in entry_name:
            return{
                "matched":True,
                "watchedlist_name":entry["name"],
                "watchedlist_rating":entry["rating"]
            }
    return {"matched":False}