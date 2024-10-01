import mysql.connector
#initialize connection with server
conn = mysql.connector.connect(
    host="localhost", 
    user="cf-python", 
    password="password"
)
#initiallizing variable cursor to connect to database
cursor = conn.cursor()

#create database task_database
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# Use the newly created database
cursor.execute("USE task_database")

#create table Recipes
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
    )
               ''')


            
#function to calculate the difficulty of a recipe
def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
        return difficulty
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
        return difficulty
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
        return difficulty
    elif cooking_time >= 10 and num_ingredients >= 4:
        difficulty = "Hard"
        return difficulty
            
def create_recipe(conn, cursor):
    name = input("Name of recipe: ")
    cooking_time = int(input("Cooking time (in minutes): "))
    ingredients = input("Ingredients (separate each with a comma): ")
    difficulty = calculate_difficulty(cooking_time, ingredients.split(", "))
    
    ingredient_str = ", ".join(ingredients.split(", "))
    
    sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
    val = (name, ingredient_str, cooking_time, difficulty)

    cursor.execute(sql, val)
    conn.commit()
    print("Recipe created successfully.")
    

 #function to allow user to search for a recipe  by ingredient   
def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    all_ingredients = []
    #loop through all rows of ingredients
    for row in results:
        ingredients = row[0].split(", ")
        for ingredient in ingredients:
            if not ingredient in all_ingredients:
                all_ingredients.append(ingredient)
            
            
    listed_ingredients = enumerate(all_ingredients)
    numbered_ingredient = list(listed_ingredients)
    print("Ingredient List:")
    for i in numbered_ingredient:
        print("- ", i[0], i[1])
    
    try:
        num = int(input("Please enter the number correspoding with the ingredient you would like to search: "))
        ingredient_searched = numbered_ingredient[num][1]
    except (ValueError, IndexError):
        print("Please search by number only.")
        return
    
    query = 'SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s'
    cursor.execute(query, ('%' + ingredient_searched + '%',))
    
    search_results = cursor.fetchall()
    if search_results:
        print("Recipies containting: " + ingredient_searched)
        for row in search_results:
            print(
                "ID: " + str(row[0]) 
                + "\nName: " + row[1] 
                + "\nIngredients: " + row[2] 
                + "\nCooking Time: " + str(row[3]) + " mins" 
                + "\nDifficulty: " + row[4]
            )
    else: 
        print("No recipes found with " + ingredient_searched)
        
#function to update a recipe
def update_recipe(conn, cursor):
    cursor.execute('SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes')
    recipes = cursor.fetchall()
    if recipes:
        print("Available Recipes: ")
        for row in recipes:
            print(
                "ID: " + str(row[0])
                + "\nName: " + row[1] 
                + "\nIngredients: " + row[2] 
                + "\nCooking Time: " + str(row[3]) + " mins" 
                + "\nDifficulty: " + row[4]
            )
    else: 
        print("No recipes found")
    
    try:
        recipe_id = int(input("Enter the ID of the recipe you would like to update: "))
    except ValueError:
        print("Please enter a valid recipe ID.")
        return
    
    print("What would you like to update?")
    print("1. Name")
    print("2. Cooking Time")
    print("3. Ingredients")
    column_choice = input("Enter the number corresponding to your choice: ")
    #choice 1 Name
    if column_choice == "1":
        new_value = input("Enter the new recipe name: ")
        query = "UPDATE Recipes SET name = %s WHERE id = %s"
        cursor.execute(query, (new_value, recipe_id))
    #choice 2 Cooking Time
    elif column_choice == "2":
        new_value = int(input("Enter the new cooking time (in minutes): "))
        #update cooking time
        query = "UPDATE Recipes SET cooking_time = %s WHERE id = %s"
        cursor.execute(query, (new_value, recipe_id))
        #update difficulty calculations
        cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        ingredients_str = cursor.fetchone()[0]  
        ingredients = ingredients_str.split(", ") 
        new_difficulty = calculate_difficulty(new_value, ingredients)
        #update difficulty
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))
    #choice 3 Ingredients
    elif column_choice == "3":
        new_value = input("Enter the new ingredients (comma-separated): ").split(", ")
        # Update ingredients
        new_ingredients_str = ", ".join(new_value)
        query = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
        cursor.execute(query, (new_ingredients_str, recipe_id))

        #Recalculate difficulty
        cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
        cooking_time = cursor.fetchone()[0]  
        new_difficulty = calculate_difficulty(cooking_time, new_value)

        # Update difficulty
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))

    else:
        print("Invalid choice.")
        return
        
    conn.commit()
    print("Recipe with ID " + str(recipe_id) + " updated successfully.")
    
#funtion to allow user to delete recipe from database
def delete_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()

    print("Available Recipes:")
    for row in recipes:
        print("ID: " + str(row[0]) + ", Name: " + row[1])

    #Ask the user to choose a recipe by id
    try:
        recipe_id = int(input("Enter the ID of the recipe you want to delete: "))
    except ValueError:
        print("Please enter a valid recipe ID.")
        return

    # Step 3: Delete the recipe
    query = "DELETE FROM Recipes WHERE id = %s"
    cursor.execute(query, (recipe_id,))

    # Step 4: Commit the changes
    conn.commit()
    print("Recipe with ID " + str(recipe_id) + " deleted successfully.")
    
    
#function main_menu of app
def main_menu(conn, cursor):
    while True:
        print("---------------------------------------")
        print("Main Menu")
        print("=======================================")
        print("Pick a choice:")
        print("1. Create new recipe.")
        print("2. Search for a recipe by ingredient.")
        print("3. Update an existing recipe.")
        print("4. Delete a recipe.")
        print("Type 'quit' to exit the program.")
        choice = input("Your choice: (please enter corresponding number or quit): ")
    
        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == 'quit':
            print("Exiting...")
            conn.commit()
            cursor.close()
            conn.close()
            break
# Run the main menu
main_menu(conn, cursor)