from flask import Flask
from dotenv import load_dotenv
import os
from data import db_session

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('KEY')


def main():
    db_session.global_init('db/blogs.db')
    app.run()


if __name__ == '__main__':
    main()
