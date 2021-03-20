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
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user.name)
    # app.run()


if __name__ == '__main__':
    main()
