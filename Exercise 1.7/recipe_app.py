#imports from sql alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

# Database credentials
username = 'cf-python'
password = 'password'
hostname = 'localhost'  # Or your server's hostname
database = 'task_database'

#engine variable to create connection to sql database
engine = create_engine("mysql+pymysql://" + username + ":" + password + "@" + hostname + "/" + database)
# Base variable 
Base = declarative_base()

#create Recipe class 
class Recipe(Base):
    __tablename__ = "final_recipes"
    #defining the columns in the table
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    
    #quick representation of the recipe
    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"
    
    # method for a formatted version of the recipe
    def __str__(self):
        return (
            "Recipe ID: " + str(self.id) +
            "\nName: " + self.name +
            "\nIngredients: " + self.ingredients +
            "\nCooking Time: " + str(self.cooking_time) + " minutes" +
            "\nDiffculty: " + self.difficulty
        )
   #method for determining difficulty of recipe        
    def calculate_difficulty(self):
        ingredients_list = self.ingredients.split(", ")
        if self.cooking_time < 10 and len(ingredients_list) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(ingredients_list) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(ingredients_list) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(ingredients_list) >= 4:
            self.difficulty = "Hard"

#initialize Base
Base.metadata.create_all(engine)
#session class 
Session = sessionmaker(bind=engine)
#initiallize session
session = Session()

#function for creating a recipe
def create_recipe():
    # Get and validate the recipe name
    while True:
        name = input("Enter the name of the recipe (max 50 characters): ")
        if len(name) > 50:
            print("Error: Name exceeds 50 characters. Try again.")
        elif not name.replace(" ", "").isalnum():
            print("Error: Name should contain only letters, numbers, and spaces. Try again.")
        else:
            break

    # Collect ingredients
    ingredients = []
    while True:
        try:
            num_ingredients = int(input("How many ingredients would you like to enter? "))
            break
        except ValueError:
            print("Error: Please enter a valid number.")

    for i in range(num_ingredients):
        ingredient = input(f"Enter ingredient {i+1}: ")
        ingredients.append(ingredient)

    # Convert list of ingredients into a string
    ingredients_str = ", ".join(ingredients)

    # Get and validate the cooking time
    while True:
        cooking_time = input("Enter the cooking time in minutes: ")
        if not cooking_time.isnumeric():
            print("Error: Cooking time must be a number. Try again.")
        else:
            cooking_time = int(cooking_time)
            break

    # Create a new Recipe object
    recipe_entry = Recipe(
        name=name,
        ingredients=ingredients_str,
        cooking_time=cooking_time
    )

    # Calculate difficulty based on ingredients and cooking time
    recipe_entry.calculate_difficulty()

    # Add the new recipe to the database and commit the changes
    session.add(recipe_entry)
    session.commit()
    
#function to view all recipes
def view_all_recipes():
    # Retrieve all recipes from the database
    recipes = session.query(Recipe).all()

    if not recipes:
        print("There are no recipes in the database.")
        return None

    # Loop through and display each recipe
    for recipe in recipes:
        print("...........................")
        print(recipe)
        
 #function to search recipe by ingredient
def search_by_ingredients():
    # Check if there are any recipes
    if session.query(Recipe).count() == 0:
        print("No recipes found in the database.")
        return None

    # Retrieve all ingredients
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []

    # Build a list of unique ingredients
    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    # Display all available ingredients
    print("Ingredients available:")
    for idx, ingredient in enumerate(all_ingredients, start=1):
        print(idx + ". " + ingredient)

    # Ask user to pick ingredients by numbers
    selected_numbers = input("Enter the numbers of ingredients to search for, separated by spaces: ")
    selected_numbers = selected_numbers.split()

    # Validate user input
    search_ingredients = []
    try:
        for num in selected_numbers:
            search_ingredients.append(all_ingredients[int(num) - 1])
    except (IndexError, ValueError):
        print("Invalid selection.")
        return None

    # Build search conditions using like()
    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))

    # Query the database with the conditions
    matching_recipes = session.query(Recipe).filter(*conditions).all()

    # Display matching recipes
    if not matching_recipes:
        print("No recipes match the selected ingredients.")
    else:
        for recipe in matching_recipes:
            print(recipe)
    
#function to edit recipes     
def edit_recipe():
    # Check if any recipes exist
    if session.query(Recipe).count() == 0:
        print("No recipes found in the database.")
        return None

    # List available recipes
    recipes = session.query(Recipe.id, Recipe.name).all()
    for recipe in recipes:
        print(f"{recipe.id}: {recipe.name}")

    # Ask user to pick a recipe by ID
    try:
        recipe_id = int(input("Enter the ID of the recipe you'd like to edit: "))
        recipe_to_edit = session.get(Recipe, recipe_id)
        if not recipe_to_edit:
            print("Recipe ID not found.")
            return None
    except ValueError:
        print("Invalid ID.")
        return None

    # Display the recipe details
    print("1. Name: " + recipe_to_edit.name)
    print("2. Ingredients: " + recipe_to_edit.ingredients)
    print("3. Cooking Time: " + str(recipe_to_edit.cooking_time) + " minutes")

    # Ask user which attribute to edit
    choice = input("Which attribute would you like to edit (1, 2, or 3)? ")

    # Edit based on user selection
    if choice == "1":
        new_name = input("Enter the new name: ")
        recipe_to_edit.name = new_name
    elif choice == "2":
        new_ingredients = input("Enter the new ingredients (comma separated): ")
        recipe_to_edit.ingredients = new_ingredients
    elif choice == "3":
        try:
            new_cooking_time = int(input("Enter the new cooking time (in minutes): "))
            recipe_to_edit.cooking_time = new_cooking_time
        except ValueError:
            print("Invalid cooking time.")
            return None
    else:
        print("Invalid choice.")
        return None

    # Recalculate difficulty
    recipe_to_edit.calculate_difficulty()

    # Commit the changes
    session.commit()
    print("Recipe updated successfully.")
    
#function to delete recipe
def delete_recipe():
    # Check if any recipes exist
    if session.query(Recipe).count() == 0:
        print("No recipes found in the database.")
        return None

    # List available recipes
    recipes = session.query(Recipe.id, Recipe.name).all()
    for recipe in recipes:
        print(str(recipe.id) + ": " + recipe.name)

    # Ask user to pick a recipe by ID
    try:
        recipe_id = int(input("Enter the ID of the recipe you'd like to delete: "))
        recipe_to_delete = session.get(Recipe, recipe_id)
        if not recipe_to_delete:
            print("Recipe ID not found.")
            return None
    except ValueError:
        print("Invalid ID.")
        return None

    # Confirm deletion
    confirm = input("Are you sure you want to delete " + recipe_to_delete.name + "? (yes/no): ")
    if confirm.lower() == 'yes':
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully.")
    else:
        print("Deletion canceled.")

#main menu starting place when running script        
def main_menu():
    while True:
        # Display the options
        print("\nMain Menu:")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to quit the application.")

        # Get the user's choice
        choice = input("\nEnter your choice: ").lower()

        # Launch the appropriate function based on the user's choice
        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == 'quit':
            print("Closing the application...")
            session.close()
            engine.dispose()
            break
        else:
            print("Invalid choice, please try again.")

# Run the main menu
if __name__ == "__main__":
    main_menu()