from flask import Flask, render_template
from dotenv import load_dotenv
import os
from data import db_session
from data.users import User
from data.news import News


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('KEY')


@app.route('/create_news/<news_title>')
def create_news(news_title):
    db_sess = db_session.create_session()
    news = News(title=news_title, content='Содержимое новости (тестовое)', is_private=False)
    db_sess.add(news)
    db_sess.commit()
    return f'<p>Успех! Добавлена новость {news_title}</p>'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


def main():
    db_session.global_init('db/blogs.db')
    # db_sess = db_session.create_session()
    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Первая новость", content="Привет блог!",
    #             is_private=True)
    # user.news.append(news)
    # db_sess.commit()
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
