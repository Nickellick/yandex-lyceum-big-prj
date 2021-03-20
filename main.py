from flask import Flask
from dotenv import load_dotenv
import os
from data import db_session
from data.users import User


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('KEY')


def main():
    db_session.global_init('db/blogs.db')
    user = User()
    user.name = 'Пользователь 1'
    user.about = 'Я пользователь 1'
    user.email = 'user1@yandex.ru'
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    # app.run()


if __name__ == '__main__':
    main()
