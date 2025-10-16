from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import string
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

digits = '0123456789'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
punctuation = '!@#$%^&*()_+-=[]{};:,<.>/?'
ally = digits + uppercase + lowercase + punctuation


def load_users():
    users_list = []
    try:
        with open('users.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                user_dict = {}
                pairs = line.split(', ')
                for pair in pairs:
                    key, value = pair.split(': ')
                    key = key.strip().strip("'")
                    value = value.strip().strip("'")
                    user_dict[key] = value
                users_list.append(user_dict)

    except FileNotFoundError:
        print("Файл users.txt не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")

    return users_list


def save_user_to_file(username, password, role):
    user_data = f"'username': '{username}', 'password': '{password}', 'role': '{role}'"

    with open('users.txt', 'a', encoding='utf-8') as file:
        file.write(user_data + '\n')

def user_exists(username):
    try:
        with open('users.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if f"'username': '{username}'" in line:
                    return True
    except FileNotFoundError:
        return False
    return False

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Пожалуйста, войдите в систему', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if user_exists(username):
            return render_template('register.html',message="Пользователь с таким логином уже существует!")

        save_user_to_file(username, password, role)

        return render_template('register.html',message="Регистрация успешна!")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        user_found = False
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = user['username']
                session['role'] = user.get('role', 'user')
                print(session)
                flash(f'Добро пожаловать, {username}!', 'success')
                user_found = True
                return redirect(url_for('index'))

        if not user_found:
            flash('Неверное имя пользователя или пароль', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))


def generate_password(pwd_length, pwd_digits, pwd_uppercase, pwd_lowercase, pwd_punctuation):
    password = ''
    chars = ''
    if pwd_digits:
        chars += string.digits
    if pwd_uppercase:
        chars += string.ascii_uppercase
    if pwd_lowercase:
        chars += string.ascii_lowercase
    if pwd_punctuation:
        chars += string.punctuation

    password = ''.join(random.choice(chars) for _ in range(pwd_length))
    return password

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    password = ''
    error = None

    current_values = {
        'pwd_length': '4',
        'pwd_digits': True,
        'pwd_uppercase': True,
        'pwd_lowercase': True,
        'pwd_punctuation': True
    }

    if request.method == 'POST':
        try:
            pwd_length = int(request.form.get('pwd_length', 4))
            pwd_digits = 'pwd_digits' in request.form
            pwd_uppercase = 'pwd_uppercase' in request.form
            pwd_lowercase = 'pwd_lowercase' in request.form
            pwd_punctuation = 'pwd_punctuation' in request.form

            password=generate_password(pwd_length, pwd_digits, pwd_uppercase, pwd_lowercase, pwd_punctuation)

        except Exception as e:
            error = f'Ошибка: {str(e)}'

    return render_template('index.html',
                           password=password,
                           error=error,
                           **current_values)

if __name__ == '__main__':
    app.run(debug=True)
