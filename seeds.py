import os
import html
import argparse
from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
seeds = client["idea_seeds"]["seeds"]

# SETTING: which statuses `water` may pick from.
# Change this one line to change the rule, e.g. ["seed", "growing"].
WATER_STATUSES = ["seed"]


def now():
    return datetime.now(timezone.utc)


def add_seed(text, tag=None):
    t = now()
    seeds.insert_one({
        "text": text,
        "status": "seed",
        "tag": tag,
        "created_at": t,
        "last_touched": t,
    })
    print(f"Planted: {text}")


def all_seeds():
    return list(seeds.find().sort("created_at", -1))


def list_seeds(tag=None):
    for number, s in enumerate(all_seeds(), start=1):
        if tag and s.get("tag") != tag:
            continue
        label = f"  #{s['tag']}" if s.get("tag") else ""
        print(f"{number}. [{s['status']}] {s['text']}{label}")


def water_seed():
    seed = seeds.find_one(
        {"status": {"$in": WATER_STATUSES}},
        sort=[("last_touched", 1)],
    )
    if seed is None:
        print("Nothing to water.")
        return
    print(f"Water this one: {seed['text']}")
    seeds.update_one({"_id": seed["_id"]}, {"$set": {"last_touched": now()}})


def set_status(number, status):
    items = all_seeds()
    if number < 1 or number > len(items):
        print("No seed with that number. Run `list` to see the numbers.")
        return
    seed = items[number - 1]
    seeds.update_one(
        {"_id": seed["_id"]},
        {"$set": {"status": status, "last_touched": now()}},
    )
    print(f"Marked as {status}: {seed['text']}")


def make_page():
    groups = {"seed": [], "growing": [], "built": []}
    for s in all_seeds():
        groups.get(s["status"], groups["seed"]).append(s)

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="UTF-8">',
        "<title>Idea Seeds</title>",
        '<link rel="stylesheet" href="style.css">',
        "</head>",
        "<body>",
        "<h1>Idea Seeds</h1>",
    ]
    for status, items in groups.items():
        parts.append(f'<section class="column {status}">')
        parts.append(f"<h2>{status.capitalize()} ({len(items)})</h2>")
        for s in items:
            parts.append('<div class="card">')
            parts.append(f"<p>{html.escape(s['text'])}</p>")
            if s.get("tag"):
                parts.append(f'<span class="tag">{html.escape(s["tag"])}</span>')
            parts.append("</div>")
        parts.append("</section>")
    parts += ["</body>", "</html>"]

    with open("seeds.html", "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print("Wrote seeds.html. Open it in your browser.")


def main():
    parser = argparse.ArgumentParser(description="Idea Seeds")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="plant a new seed")
    p_add.add_argument("text")
    p_add.add_argument("--tag")

    p_list = sub.add_parser("list", help="show seeds")
    p_list.add_argument("--tag")

    sub.add_parser("water", help="show the seed that needs attention")

    p_grow = sub.add_parser("grow", help="mark a seed as growing")
    p_grow.add_argument("number", type=int)

    p_built = sub.add_parser("built", help="mark a seed as built")
    p_built.add_argument("number", type=int)

    sub.add_parser("page", help="generate seeds.html")

    args = parser.parse_args()

    if args.command == "add":
        add_seed(args.text, args.tag)
    elif args.command == "list":
        list_seeds(args.tag)
    elif args.command == "water":
        water_seed()
    elif args.command == "grow":
        set_status(args.number, "growing")
    elif args.command == "built":
        set_status(args.number, "built")
    elif args.command == "page":
        make_page()


if __name__ == "__main__":
    main()