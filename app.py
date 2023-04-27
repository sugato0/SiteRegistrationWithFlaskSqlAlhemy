import os

from flask import Flask, render_template, request, redirect,session
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем экземпляр класса Flask
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'hasudfhsdahfDFHDH23'
# Создаем экземпляр класса Engine для работы с базой данных SQLite
engine = create_engine('sqlite:///users.db', echo=True)
app.config['UPLOAD_FOLDER'] = 'static/media'
HOSTNAME = "http://127.0.0.1:5000/"
# Создаем базовый класс для определения моделей таблиц
Base = declarative_base()

# Описываем модель таблицы "users"
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    username = Column(String)
    
    email = Column(String)
    sity = Column(String)
    image_link = Column(String)
    password = Column(String)



# Создаем таблицу "users"
Base.metadata.create_all(engine)

# Создаем объект Session для работы с базой данных
Session = sessionmaker(bind=engine)
sessionBD = Session()

# Маршрут для отображения формы регистрации пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Проверяем, существует ли пользователь с таким же email
        user = sessionBD.query(User).filter_by(email=email).first()
        if user:
            return render_template('register.html', error='Пользователь с таким email уже зарегистрирован')
        sityname = "где-то"
        image_link = HOSTNAME+"static/media/Avatar-Profile-Vector-PNG-File.png"
        # Создаем нового пользователя и добавляем его в базу данных
        new_user = User(username=username, email=email, password=password, sity = sityname,image_link = image_link )
        sessionBD.add(new_user)
        sessionBD.commit()

        # Перенаправляем пользователя на страницу входа
        return redirect('/login')

    # Отображаем форму регистрации
    return render_template('register.html')

# Маршрут для отображения формы входа пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получаем данные из формы
        email = request.form['email']
        password = request.form['password']

        # Проверяем, существует ли пользователь с таким email и паролем
        user = sessionBD.query(User).filter_by(email=email, password=password).first()

        if user:
            # Сохраняем пользователя в сессии

            session['user'] = {'id': user.id, 'username': user.username,'email':user.email}
            # Перенаправляем пользователя на главную страницу

            return redirect('/')

        else:
            return render_template('login.html', error='Неправильный email или пароль')

    # Отображаем форму входа
    return render_template('login.html')
# Маршрут для отображения формы входа пользователя
@app.route('/', methods=['GET', 'POST'])
def mainer():
    return render_template('main1.html',data=session)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in {'jpg', 'jpeg', 'png', 'gif'}

@app.route('/main/profile/', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Обработка данных из формы
        file = request.files['image']

        # проверяем, что файл имеет допустимое расширение
        if not allowed_file(file.filename):
            return "Допустимы только файлы с расширением jpg, jpeg, png, gif"
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # # возвращаем URL загруженного изображения
        #     return render_template('index.html', result='/' + os.path.join(app.config['UPLOAD_FOLDER'], filename))

        name = request.form['name']

        email = request.form['email']
        password = request.form['password']
        sity = request.form['sity']
        image_link = HOSTNAME+os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\","/")

        # Обновление данных в БД

        users = sessionBD.query(User).filter_by(id = session["user"]["id"]).first()

        users.username = name

        users.email = email

        users.password = password

        users.sity = sity

        users.image_link = image_link

        sessionBD.commit()

        session['user'] = {'id': users.id, 'username': users.username,'email':users.email}


        return render_template('profile.html', name=name,image = image_link, email=email,password=password,sity = sity)
    

    else:

        users = sessionBD.query(User).filter_by(id=session['user']['id']).first()

        return render_template('profile.html', name=users.username,image = users.image_link, email=users.email,password=users.password,sity = users.sity)


@app.route('/main/people', methods=['GET', 'POST'])
def people():
    if request.method == 'POST':
        # Получаем данные из формы
        sities = request.form['sity']

        blocki = sessionBD.query(User).filter_by(sity = sities)
        return render_template('people.html',data=blocki)
    else:
        blocki = sessionBD.query(User).all()
        return render_template('people.html', data=blocki)
        
@app.route('/main/noYour/<int:ids>', methods=['GET', 'POST'])
def peopleProfile(ids):
    murrr = False
    try:
        murrr = ids == session['user']['id']
    except:
        pass
    if murrr:
        # Получаем данные из формы
        users = sessionBD.query(User).filter_by(id=session['user']['id']).first()

        return render_template('profile.html', name=users.username,image = users.image_link, email=users.email,password=users.password,sity = users.sity)

        
    else:
        users = sessionBD.query(User).filter_by(id=ids).first()
        return render_template('userProfiles.html', data=users)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")


if __name__ == '__main__':

    app.run(debug=True)