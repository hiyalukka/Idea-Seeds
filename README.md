<h1 align="center">Idea Seeds</h1>

<p align="center">
  Every idea starts as a seed. Water it, grow it, ship it.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-2a7d42?style=flat-square" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Flask-web%20app-2a7d42?style=flat-square" alt="Flask">
  <img src="https://img.shields.io/badge/MongoDB-Atlas-2a7d42?style=flat-square" alt="MongoDB Atlas">
  <img src="https://img.shields.io/badge/built%20in-public-2a7d42?style=flat-square" alt="Built in public">
</p>

<!-- Add a screenshot: save it as docs/screenshot.png, then uncomment -->
<!-- ![Idea Seeds board](docs/screenshot.png) -->

## Why I built it
My ideas kept dying in notes apps. Idea Seeds gives each one a life cycle, so old ideas keep getting attention. It is also the project where I learned pymongo, after building a Node and MongoDB app first.

## Features
- **Plant** an idea with an optional tag, right from the web page
- **Move it along:** Seed, then Growing, then Built, or delete it
- **Garden board** with three stages, each styled differently
- **CLI too:** `add`, `list`, `water`, `grow`, `built`, `page`
- **Cloud data** stored in MongoDB Atlas

## How it works
```
Browser form  ->  Flask route  ->  pymongo  ->  MongoDB Atlas
                       |
                       +-> returns the board as HTML
```
Forms send a POST request, Flask saves or updates the seed, then redirects back to the board. Each button carries the seed's real `_id`, not its position in a list.

## Run it locally
```
git clone https://github.com/hiyalukka/idea-seeds.git
cd idea-seeds
conda create -n idea-seeds python=3.12 -y
conda activate idea-seeds
pip install -r requirements.txt
```
Create a `.env` file:
```
MONGODB_URI=your-atlas-connection-string
```
Start the app and open http://127.0.0.1:5000:
```
python app.py
```

## CLI examples
```
python seeds.py add "quiz maker from my notes" --tag ml
python seeds.py list
python seeds.py water
python seeds.py grow 1
python seeds.py page
```

## Project structure
```
idea-seeds/
  app.py          Flask web app
  seeds.py        command-line version
  static/
    style.css     the garden theme
  requirements.txt
  .env            private, never committed
```

## What I learned
- pymongo: `insert_one`, `find`, `sort`, `update_one` with `$set`, `delete_one`
- Flask routes, forms, and POST then redirect
- Why to use a document `_id` instead of a list position
- Keeping secrets in `.env` and out of Git

## Roadmap
- [ ] Edit a seed's text
- [ ] Stats with MongoDB aggregation
- [ ] Deploy online

## About
Part of my 10-day MongoDB challenge, built in public by [Hiya](https://github.com/hiyalukka).