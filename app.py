from flask import Flask, render_template, request
from db_config import get_connection  # Ensure this is correctly implemented and working

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    conn = get_connection()
    if conn is None:
        return "Failed to connect to the database.", 500  # Handle database connection errors gracefully

    cursor = conn.cursor()

    try:
        if request.method == 'POST':
            ingredient = request.form.get('ingredient')
            if not ingredient:  # Check if ingredient is provided
                return "Ingredient is required.", 400
            
            query = """
                SELECT DISTINCT r.recipe_name, r.category, r.preparation_time 
                FROM Recipes r
                JOIN Recipe_Ingredients ri ON r.recipe_id = ri.recipe_id
                JOIN Ingredients i ON ri.ingredient_id = i.ingredient_id
                WHERE LOWER(i.ingredient_name) = LOWER(:ingredient_name)
            """
            cursor.execute(query, {"ingredient_name": ingredient})
        else:
            query = "SELECT recipe_name, category, preparation_time FROM Recipes"
            cursor.execute(query)
        
        recipes = cursor.fetchall()
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    finally:
        cursor.close()
        conn.close()

    return render_template('recipes.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
