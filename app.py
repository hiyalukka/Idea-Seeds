import os
import html
from datetime import datetime, timezone
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, redirect, request
from pymongo import MongoClient

load_dotenv()
seeds = MongoClient(os.getenv("MONGODB_URI"))["idea_seeds"]["seeds"]
app = Flask(__name__)

STATUS = {"grow": "growing", "built": "built"}


def now():
    return datetime.now(timezone.utc)


def button(sid, action, label):
    return (f'<form method="post" action="/{action}/{sid}">'
            f'<button>{label}</button></form>')


def card(s):
    sid = str(s["_id"])
    tag = f'<span class="tag">{html.escape(s["tag"])}</span>' if s.get("tag") else ""
    buttons = ""
    if s["status"] == "seed":
        buttons += button(sid, "grow", "Grow")
    if s["status"] != "built":
        buttons += button(sid, "built", "Built")
    buttons += button(sid, "delete", "Delete")
    return (f'<div class="card"><p>{html.escape(s["text"])}</p>{tag}'
            f'<div class="actions">{buttons}</div></div>')


@app.get("/")
def home():
    groups = {"seed": [], "growing": [], "built": []}
    for s in seeds.find().sort("created_at", -1):
        groups.get(s["status"], groups["seed"]).append(s)

    columns = ""
    for status, items in groups.items():
        cards = "".join(card(s) for s in items)
        columns += (f'<section class="column {status}">'
                    f'<h2>{status.capitalize()} ({len(items)})</h2>{cards}</section>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Idea Seeds</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<h1>Idea Seeds</h1>
<form class="add" method="post" action="/add">
  <input name="text" aria-label="Idea" placeholder="Plant a new idea" required maxlength="200">
  <input name="tag" aria-label="Tag (optional)" placeholder="Tag (optional)" maxlength="20">
  <button>Plant seed</button>
</form>
{columns}
</body>
</html>"""


@app.post("/add")
def add():
    text = request.form.get("text", "").strip()
    tag = request.form.get("tag", "").strip() or None
    if text:
        t = now()
        seeds.insert_one({"text": text, "status": "seed", "tag": tag,
                          "created_at": t, "last_touched": t})
    return redirect("/")


@app.post("/<action>/<sid>")
def change(action, sid):
    _id = ObjectId(sid)
    if action == "delete":
        seeds.delete_one({"_id": _id})
    elif action in STATUS:
        seeds.update_one({"_id": _id},
                         {"$set": {"status": STATUS[action], "last_touched": now()}})
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)