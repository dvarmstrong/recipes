from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipe:

    db_name = 'recipes'

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']
        self.user_id= data['user_id']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db_name).query_db(query)

        all_recipes = []
        for row in results:
            recipe = cls(row)
            print(results)
            all_recipes.append(recipe)
        return all_recipes


    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes ( name, description, instructions, under_30, user_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(user_id)s);"

        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(f"{results} + here:")
        return cls(results[0]) #ERRROr I am reciveing is tuple is out index range ????????



    @classmethod #Throwing error of id 
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_30=%(under_30)s, user_id =%(user_id)s WHERE id = %(id)s;"
        
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)








    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Invalid recipe name", "recipie login")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Invalid description", "recipe login")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Invalid instructions", "recipe login")
            is_valid = False
        # if len(recipe['under_30']) == "0":
        #     flash("Choose yes or no", "recipe login")
        #     is_valid = False
        return is_valid