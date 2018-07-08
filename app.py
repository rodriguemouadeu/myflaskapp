from flask import Flask, render_template, flash, redirect, url_for, session, logging,request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_APSSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# config SECRET_KEY
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

# init MySQL
mysql = MySQL(app)

Article = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

class RegisterForm(Form):
    name = StringField(u'Name', validators=[validators.Length(min=1, max=50),validators.input_required()])
    username  = StringField(u'Username', validators=[validators.Length(min=4, max=25),validators.optional()])
    email  = StringField(u'Email', validators=[validators.Length(min=1, max=50),validators.optional()])
    password  = PasswordField(u'Password', validators=[
                    validators.input_required(),
                    validators.EqualTo('confirm', message='Passwords do not match')
                ])
    confirm  = PasswordField(u'Confirm Password')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if(request.method == 'POST') and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # create cursor
        cur = mysql.connection.cursor()

        # Execute DB insert
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'succes')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
