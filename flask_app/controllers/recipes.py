
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask import redirect, render_template, request, session, flash 



@app.route('/recipe/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    
    
    
    data = {
        "id":session['user_id']
    }
    
    user = User.get_by_id(data)
    
    return render_template('new.html', user=user)

@app.route('/recipe/add', methods=['POST'])
def add_recipe():
    if 'user_id' not in session:
        return redirect('/')
    
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')

    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "under_30" :(request.form["under_30"]),
        "user_id" : session["user_id"]
    }

    Recipe.create_recipe(data)
    return redirect('/dashboard')

@app.route('/recipe/<int:id>')
def view(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id" : id,
    }

    user_data = {
        "id": session['user_id']
    }

    recipe = Recipe.get_recipe_by_id(data)
    user = User.get_by_id(user_data)

    return render_template("recipe.html", recipe=recipe, user=user)

@app.route('/recipe/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id" : id,
    }

    user_data = {
        "id": session['user_id']
    }

    edit = Recipe.get_recipe_by_id(data)
    user = User.get_by_id(user_data)

    return render_template('edit.html', edit=edit, user=user)


@app.route('/update/recipe/<int:id>', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    
    data = {
        "name" : request.form["name"],
        "id" : id,
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "under_30" :request.form["under_30"],
        "user_id" : session["user_id"]
    }

    Recipe.update(data)
    return redirect('/dashboard')






@app.route('/recipe/destroy/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id" : id,
    }

    Recipe.destroy(data)

    return redirect('/dashboard')






