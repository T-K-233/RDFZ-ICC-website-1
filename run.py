import csv
from flask import Flask, render_template
from feeds import news_feed, post_feed

app = Flask(__name__)


@app.route('/')
def home():
    feed = news_feed if len(news_feed) < 5 else news_feed[:5]
    return render_template('home.html', FEEDS=feed)

@app.route('/news')
def news():
    return render_template('news.html', FEEDS=news_feed)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faculty')
def faculty():
    return render_template('faculty.html')

@app.route('/matriculation')
def matriculation():
    data_list = []
    for i in range(2010, 2019):
        with open('./matriculation/%s.csv' % i, newline='', encoding='utf-8') as csvfile:
            data_list.append(list(csv.reader(csvfile, delimiter=',')))
    return render_template('matriculation.html', DATA=data_list)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/culture')
def culture():
    return render_template('culture.html')

@app.route('/post/<title>')
def post(title):
    post = post_feed.get(title)
    if post:
        return render_template('post.html', POST=post)
    else:
        return render_template('404.html')

@app.route('/<any_text>')
def default_handler(any_text):
    return render_template('404.html')

app.run(host='0.0.0.0', port=80, debug=True)
