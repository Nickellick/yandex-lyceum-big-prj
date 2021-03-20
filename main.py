from flask import Flask
from dotenv import load_dotenv
import os
from data import db_session
from data.users import User
from data.news import News


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('KEY')


def main():
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 1).first()
    news = News(title="Первая новость", content="Привет блог!",
                is_private=True)
    user.news.append(news)
    db_sess.commit()
    # app.run()


if __name__ == '__main__':
    main()
