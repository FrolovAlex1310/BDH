from timeit import default_timer
from flask import Flask, render_template,  request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user # код для авторизации
from flask_login import LoginManager  # код для авторизации
from flask_login import logout_user  # код для авторизации
from flask_login import login_required   # код для авторизации
from transliterate import translit
from werkzeug.exceptions import abort

login_manager = LoginManager()  # код для авторизации


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager.init_app(app) # код длдя авторизации
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'   # код для авторизации



db = SQLAlchemy(app)


# app = Flask(__name__, static_folder="static")
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user = db.Column(db.Integer)
    fotoart = db.Column(db.String(300), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(10), nullable=True)
    patronymic = db.Column(db.String(20), nullable=True)
    initials = db.Column(db.String(4), nullable=True)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    addreshome = db.Column(db.Text, nullable=True)
    laddreshome = db.Column(db.Text, nullable=True)
    lsurname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(10), nullable=True)
    lpatronymic = db.Column(db.String(20), nullable=True)
    linitials = db.Column(db.String(4), nullable=True)
    is_active = db.Column(db.Boolean(), default=True)
    avatar = db.Column(db.String(), nullable=True)


    def get_id(self):
        return str(self.id)
        


@login_manager.user_loader
def load_user(user_id):
    try:
        return Users.query.get(user_id)
    except:
        return None

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/enter')
def enter():
    return render_template("enter.html")


@app.route('/offis/<int:id>')
def offis(id):
    user = Users.query.get(id)
    return render_template("offis.html", user=user)




# Транслитация в форме
@app.route('/offis-user/<user_id>')
def offis_user(user_id):
    user = db.session.query(Users).filter(Users.id==user_id).first()
    surname_uk = translit(user.surname, language_code='ru', reversed=True)
    name_uk = translit(user.name, language_code='ru', reversed=True)
    patronymic_uk = translit(user.patronymic, language_code='ru', reversed=True)
    initials_uk = translit(user.initials, language_code='ru', reversed=True)

    print("Имя транслитерированное:", name_uk, )
    return render_template("offis-user.html", user=user, lname=name_uk,
        lsurname=surname_uk, lpatronymic=patronymic_uk, linitials=initials_uk)



# Добавление статьи (записи) в таблицу Article
@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        user = request.form['user']


        article = Article(title=title, intro=intro, text=text, user=user)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
               return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create-article.html')


# Открытие списка статей (записей) в таблице Article
@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)

# Открытие списка статей (записей) в таблице Article
@app.route('/posts-main')
def post_main():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts-main.html', articles=articles)


# Открытие конкретной статьи (записи) в таблице базы
@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html", article=article)

# Удаление конкретной статьи (записи) в таблице базы Article
@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"

# Изменеие конкретной статьи (записи) в таблице Article
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:

        return render_template('post-update.html', article=article)

# Добавление пользователя (записи) в таблицу Users
@app.route('/create-user', methods=['POST', 'GET'])
def create_user():
    if request.method == "POST":
        surname = request.form['surname']
        name = request.form['name']
        patronymic = request.form['patronymic']
        initials = request.form['initials']
        addreshome = request.form['addreshome']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        surname_uk = translit(surname, language_code='ru', reversed=True)
        name_uk = translit(name, language_code='ru', reversed=True)
        patronymic_uk = translit(patronymic, language_code='ru', reversed=True)
        initials_uk = translit(initials, language_code='ru', reversed=True)
        addreshome_uk = translit(addreshome, language_code='ru', reversed=True)


        user = Users(surname=surname, name=name, patronymic=patronymic, initials=initials,
                     addreshome=addreshome, email=email, phone=phone, password=password,
                     lsurname=surname_uk, lname=name_uk, lpatronymic=patronymic_uk,
                     linitials=initials_uk, laddreshome=addreshome_uk)

        try:
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)  # Залогиневаем созданоого поьзователя
            url='/offis-user/{user_id}'.format(user_id=user.id)
            print(url)
            return redirect(url)
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create-user.html')


# # Изменеие конкретной статьи (записи) в таблице Users ????
# @app.route('/offis-user/<int:id>/update', methods=['POST', 'GET'])
# def user_update(id):
#     users = Users.query.get(id)
#     if request.method == "POST":
#         users.surname = request.form['surname']
#         users.name = request.form['name']
#         users.patronymic = request.form['patronymic']
#         users.initials = request.form['initials']
#         users.phone = request.form['phone']
#         users.email = request.form['email']
#         users.created_on = request.form['created_on']
#         users.updated_on = request.form['updated_on']
#         users.addreshome = request.form['addreshome']
#         users.laddreshome = request.form['laddreshome']
#         users.lsurname = request.form['lsurname']
#         users.lname = request.form['lname']
#         users.linitials = request.form['linitials']
#         users.is_active = request.form['is_active']
#         users.avatar = request.form['avatar']
#
#         try:
#             db.session.commit()
#             return redirect('//offis-user')
#         except:
#             return "При редактировании статьи произошла ошибка"
#     else:
#
#         return render_template('offis-user.html', users=users)

# Вход в портал
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":  # проверяем что форма отправила запрос методом POST
        email = request.form['email'] # Получаем значения для пароля и для емайла
        password = request.form['password']
        print(email, password)

# ищем в базе/таблице Users запись соответсвующую паролю и емайлу
        user = db.session.query(Users).filter(Users.email==email).first()
        if str(user.password) == password: # сравниваем пароль из формы и пароль из базы
            login_user(user, remember=True) # При совпадении пароля открывает страницу
            print("Пользователь найден пароль верный")
            return redirect("/")
        else:   # при ошибке --------
            print("Пароль не верный")
            return "Пароль не верный"

    return "not_ok"

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


# foto в кабинет
@app.route('/avatar_uploader/<user_id>', methods = ['GET', 'POST'])
def upload_file(user_id):
   if request.method == 'POST':
      f = request.files['file']
      filename = user_id + "_" + f.filename
      path ="static/images/avatar/"
      f.save(path + filename)

      user = db.session.query(Users).filter(Users.id == user_id).first()

      user.avatar = filename
      db.session.add(user)
      db.session.commit()

      url = '/offis-user/{user_id}'.format(user_id=user.id)
      return redirect(url)



if __name__ == "__main__":
    app.run(debug=True)
