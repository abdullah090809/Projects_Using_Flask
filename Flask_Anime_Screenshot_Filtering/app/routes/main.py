from flask import Blueprint, render_template, request, session, jsonify, flash
import os
import json
from app.utils.watchlist import parse_watchlist
from app.utils.ocr import extract_text, clean_text
from app.utils.jikan import search_anime, is_confident_match
from app.utils.matcher import match_against_watchlist
from app.config import UPLOAD_FOLDER, DATA_FOLDER

main=Blueprint("main",__name__)

def save_data(results,matched,discarded):
    data={
        "results": results,
        "matched": matched,
        "discarded": discarded
    }
    path=os.path.join(DATA_FOLDER,"scan_data.json")
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data, f)
def load_data():
    path=os.path.join(DATA_FOLDER,"scan_data.json")
    if not os.path.exists(path):
        return [], [], []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["results"], data["matched"], data["discarded"]
@main.route("/",methods=["POST","GET"])
def index():
    if request.method=="POST":
        watchlist_file =request.files["watchlist"]
        watchlist_path=os.path.join(UPLOAD_FOLDER,watchlist_file.filename)
        watchlist_file.save(watchlist_path)
        session["watchlist_path"]=watchlist_path

        screenshots = request.files.getlist("screenshot")
        screenshot_paths = []
        for screenshot_file in screenshots:
            screenshot_path = os.path.join(UPLOAD_FOLDER, screenshot_file.filename)
            screenshot_file.save(screenshot_path)
            screenshot_paths.append(screenshot_path)
        session["screenshot_paths"] = screenshot_paths

        watchlist = parse_watchlist(watchlist_path)

        results=[]
        matched=[]
        discarded=[]
        already_seen = set() 

        for screenshot_path in screenshot_paths:
            raw_text = extract_text(screenshot_path)
            cleaned = clean_text(raw_text)        
            cleaned = list(set(cleaned))
            for chunk in cleaned:
                if chunk in already_seen:
                    continue
                already_seen.add(chunk)
                anime=search_anime(chunk)
                if is_confident_match(chunk,anime):
                    match=match_against_watchlist(anime,watchlist)
                    entry={
                        "anime":anime,
                        "match":match
                    }
                    if match["matched"]:
                        matched.append(entry)
                    else:
                        results.append(entry)
                else:
                    discarded.append(chunk)
        save_data(results,matched,discarded)
        return render_template("results.html",results=results,matched=matched,discarded=discarded,screenshot=screenshot_path)
    return render_template("index.html")

@main.route("/search_discarded",methods=["POST"])
def search_discarded():
    query=request.form.get("query")
    watchlist_path=session.get("watchlist_path")
    screenshot_paths=session.get("screenshot_paths")
    results, matched, discarded = load_data()
    watchlist = parse_watchlist(watchlist_path)
    anime = search_anime(query)

    if anime:
        match = match_against_watchlist(anime, watchlist)
        entry = {"anime": anime, "match": match}
        if match["matched"]:
            matched.append(entry)
        else:
            results.append(entry)
        if query in discarded:
            discarded.remove(query)
        save_data(results, matched, discarded)
        if match["matched"]:
            flash(f"{query} Added to Matched List")
        else:
            flash(f"{query} Added to New Anime List")
    return render_template("results.html", results=results, matched=matched, discarded=discarded, screenshot=screenshot_paths)

@main.route("/download_results")
def download_results():
    results, _, _ = load_data()
    return jsonify(results), 200, {
        "Content-Disposition": "attachment; filename=results.json"
    }