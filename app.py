import os
import random
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from datetime import datetime
from pprint import pprint
import requests
import omdb
import uuid
from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "film_dazzle"
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

API_KEY = os.environ.get('API_KEY')
omdb.set_default('apikey', API_KEY)


mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    # Popular titles based on reviews
    reviews = mongo.db.reviews.find()
    sorted_reviews = sorted(reviews, key=lambda k: k['date'], reverse=True)

    # Avoid duplicates
    duplicates_list = []
    for review in sorted_reviews:
        imdb_id = review['imdb_id']
        duplicates_list.append(imdb_id)

    duplicates_dict = dict.fromkeys(duplicates_list)
    duplicates_keys = duplicates_dict.keys()

    no_duplicates = []
    for keys in duplicates_keys:
        no_duplicates.append(keys)

    # Pull titles from Mongo
    titles_list = []
    for ids in no_duplicates:
        titles = mongo.db.titles.find_one({'imdb_id': ids})
        titles_list.append(titles)

    # Top Box Office
    boxoffice = mongo.db.boxoffice.find().limit(10)
    titles = mongo.db.titles.find()
    boxoffice_limited = []

    for bo in boxoffice:
        imdb_id = bo['imdb_id']
        titles = mongo.db.titles.find_one({'imdb_id': imdb_id})
        poster = titles['poster']
        bo['poster'] = poster
        boxoffice_limited.append(bo)

    return render_template("index.html", titles=titles_list[0:10],
                           boxoffice=boxoffice_limited)


@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        user_search = request.form.get('query')
        return redirect(url_for('result', query=user_search.lower()))
    else:
        return render_template("index.html")


@app.route('/search/<query>')
def result(query):
    data_request = omdb.search_movie(query, page=1)
    if data_request:
        return render_template("results.html",
                               data_request=data_request, query=query)
    else:
        return render_template("no_results.html")


@app.route('/add_title/<users_choice>')
def add_title(users_choice):
    data_request = omdb.imdbid(f'{users_choice}')
    data_reduced = data_request
    keys = {
        "dvd", "website", 'ratings', 'imdb_votes',
        "language", "response", "type", 'box_office'
    }
    for key in keys:
        del data_reduced[key]

    #  Youtube API
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    search_params = {
        'key': YOUTUBE_API_KEY,
        'q': f"{data_reduced['title']} official trailer",
        'part': 'snippet',
        'maxResults': 1,
        'type': 'video'
    }
    results = requests.get(search_url, params=search_params).json()
    items = results['items']
    for item in items:
        video_id = item['id']['videoId']
    data_reduced['youtube_id'] = video_id
    data_reduced['users_rating'] = 'N/A'

    # Push to Mongo
    titles = mongo.db.titles
    title_exists = titles.find_one({'imdb_id': users_choice})

    if not title_exists:
        titles.insert_one(data_reduced)
        find_imdb_id = titles.find_one({'imdb_id': users_choice})
        imdb_id = find_imdb_id['imdb_id']
        return redirect(url_for('title', title_id=imdb_id))
    else:
        imdb_id = title_exists.get('imdb_id')
        return redirect(url_for('title', title_id=imdb_id))


@app.route('/title/<title_id>')
def title(title_id):
    title = mongo.db.titles.find_one({'imdb_id': title_id})
    id_exists = title['imdb_id']

    # Load Reviews
    imdb_id = title['imdb_id']
    reviews = list(mongo.db.reviews.find({'imdb_id': imdb_id}))
    sorted_reviews = sorted(reviews, key=lambda k: k['date'], reverse=True)
    limited_reviews = sorted_reviews[0:5]

    if not id_exists:
        return render_template("404.html")
    else:
        return render_template('title.html', title=title,
                               reviews=limited_reviews)


@app.route('/user_review/<title_id>', methods=["GET", "POST"])
def user_review(title_id):
    if request.method == "POST":
        title = mongo.db.titles.find_one({'imdb_id': title_id})
        imdb_id = title['imdb_id']

        # Push to Mongo
        user_review = request.form.get('text')
        user_name = request.form.get('user')
        user_rating = request.form.get('rating')
        user_title = request.form.get('title')
        date = datetime.now().strftime("%B %d, %Y at %H:%M:%S")
        review = {'title': user_title,
                  'user': user_name,
                  'text': user_review,
                  'rating': user_rating,
                  'imdb_id': imdb_id,
                  'review_id': str(uuid.uuid4()),
                  'date': date}
        mongo.db.reviews.insert_one(review)

        # Ratings to Mongo
        reviews = list(mongo.db.reviews.find({'imdb_id': title_id}))
        reviews_length = len(reviews)
        reviews_sum = 0
        for review in reviews:
            review_int = int(review['rating'])
            reviews_sum = reviews_sum + review_int
        avg = round(reviews_sum / reviews_length, 1)
        mongo.db.titles.update_one({'imdb_id': title_id},
                                   {'$set': {'users_rating': str(avg)}})

        # Reload page
        imdb_id = title['imdb_id']
        return redirect(url_for('title', title_id=imdb_id))
    else:
        return render_template("index.html")


@app.route('/review/<review_choice>')
def review(review_choice):
    review = mongo.db.reviews.find_one({'review_id': review_choice})
    review_id = review['review_id']
    imdb_id = review['imdb_id']
    title = mongo.db.titles.find_one({'imdb_id': imdb_id})
    return render_template('review.html', review_id=review_id,
                           review=review, title=title)


@app.route('/top_imdb')
def top_imdb():
    titles = list(mongo.db.titles.find())
    sorted_titles = sorted(titles, key=lambda k: k['imdb_rating'],
                           reverse=True)
    sorted_titles_list = []
    for sorted_title in sorted_titles:
        if not sorted_title['imdb_rating'] == 'N/A':
            sorted_titles_list.append(sorted_title)
    return render_template('top_imdb.html', titles=sorted_titles_list)


@app.route('/top_metacritic')
def top_metacritic():
    titles = list(mongo.db.titles.find())
    sorted_titles = sorted(titles, key=lambda k: k['metascore'],
                           reverse=True)
    sorted_titles_list = []
    for sorted_title in sorted_titles:
        if not sorted_title['metascore'] == 'N/A':
            sorted_titles_list.append(sorted_title)
    return render_template('top_metacritic.html', titles=sorted_titles_list)


@app.route('/top_users')
def top_users():
    titles = list(mongo.db.titles.find())
    sorted_titles = sorted(titles, key=lambda k: k['users_rating'],
                           reverse=True)
    sorted_titles_list = []
    for sorted_title in sorted_titles:
        if not sorted_title['users_rating'] == 'N/A':
            sorted_titles_list.append(sorted_title)
    return render_template('top_users.html', titles=sorted_titles_list)


@app.route('/box_office')
def box_office():
    boxoffice = mongo.db.boxoffice.find()
    offset = request.args.get('offset', 0, type=int)
    page = 25
    boxoffice_limited = boxoffice.skip(offset).limit(page)

    return render_template('box_office.html', boxoffice=boxoffice_limited)


@app.route('/randomize')
def randomize():

    def random_title():
        titles = mongo.db.titles.find()
        titles_id_list = []
        for title in titles:
            imdb_id = title['imdb_id']
            titles_id_list.append(imdb_id)
        random_title_id = random.choice(titles_id_list)
        return random_title_id

    return redirect(url_for('title', title_id=random_title()))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
