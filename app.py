from flask import Flask, render_template, request, redirect,session
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем экземпляр класса Flask
app = Flask(__name__)
app.secret_key = b'hasudfhsdahfDFHDH23'
# Создаем экземпляр класса Engine для работы с базой данных SQLite
engine = create_engine('sqlite:///users.db', echo=True)

# Создаем базовый класс для определения моделей таблиц
Base = declarative_base()

# Описываем модель таблицы "users"
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
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

        # Создаем нового пользователя и добавляем его в базу данных
        new_user = User(username=username, email=email, password=password)
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

            session['user'] = {'id': user.id, 'username': user.username}
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

@app.route('/main/people', methods=['GET', 'POST'])
def people():

    return render_template('people.html',data=sessionBD)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")


if __name__ == '__main__':

    app.run()