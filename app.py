from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

digits = '0123456789'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
punctuation = '!@#$%^&*()_+-=[]{};:,<.>/?'
ally = digits + uppercase + lowercase + punctuation

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

            current_values.update({
                'pwd_length': str(pwd_length),
                'pwd_digits': pwd_digits,
                'pwd_uppercase': pwd_uppercase,
                'pwd_lowercase': pwd_lowercase,
                'pwd_punctuation': pwd_punctuation
            })

            password=generate_password(pwd_length, pwd_digits, pwd_uppercase, pwd_lowercase, pwd_punctuation)

        except Exception as e:
            error = f'Ошибка: {str(e)}'

    return render_template('index.html',
                           password=password,
                           error=error,
                           **current_values)

if __name__ == '__main__':
    app.run(debug=True)