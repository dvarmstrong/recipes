
from flask import redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():

    

    if not User.validate_user(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }

    user_id = User.save(data)
    if not user_id:
        flash("Email already taken!!!", "register")
        return redirect('/')
    session['user_id'] = user_id
    return redirect('/dashboard.html')

@app.route('/login', methods=['POST'])
def login():

    data = {
        "email": request.form['email'],
        "password": request.form['password']
    }

    user = User.get_by_email(data)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid password", "login")
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id" : session['user_id']
    }
    user = User.get_by_id(data)
    users = User.get_all_users()
    recipes = Recipe.get_all()

    return render_template('dashboard.html', user=user, users=users, recipes=recipes)