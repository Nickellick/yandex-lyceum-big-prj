from flask import Flask, render_template, redirect, request, make_response, session
from dotenv import load_dotenv
import os
from data import db_session
from data.users import User
from data.news import News
from forms.users import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('KEY')
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count >= 10:
        res = make_response(
            f'Вы пришли на эту страницу {visits_count + 1} раз. Самое время почистить вам куки!')
        res.set_cookie("visits_count", '0', max_age=0)
        return res
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.is_private != True)
        res = make_response(
            render_template('index.html', news=news))
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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
