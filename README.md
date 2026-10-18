# Idea Seeds

A small garden for your ideas. Plant an idea as a seed, then move it to growing and built. Python, Flask and MongoDB Atlas.

## What it does
- Plant ideas with an optional tag from the web page
- Move each idea from Seed to Growing to Built, or delete it
- Command-line version too: `add`, `list`, `water`, `grow`, `built`, `page`
- Data lives in MongoDB Atlas

## Stack
Python, Flask, pymongo, MongoDB Atlas, plain HTML and CSS

## Run it
1. Clone and enter the folder:
```
   git clone https://github.com/hiyalukka/idea-seeds.git
   cd idea-seeds
```
2. Create an environment and install packages:
```
   conda create -n idea-seeds python=3.12 -y
   conda activate idea-seeds
   pip install -r requirements.txt
```
3. Create a `.env` file with your Atlas connection string:
```
   MONGODB_URI=your-connection-string
```
4. Start the web app and open http://127.0.0.1:5000:
```
   python app.py
```

## CLI examples
```
python seeds.py add "quiz maker from my notes" --tag ml
python seeds.py list
python seeds.py water
python seeds.py grow 1
```

## What I learned
- pymongo basics: `insert_one`, `find`, `update_one` with `$set`, `delete_one`
- Routes, forms, and POST then redirect in Flask
- Why buttons should carry a document `_id` instead of a list position
- Keeping secrets in `.env` and out of Git

Part of my 10-day MongoDB challenge. Built in public.