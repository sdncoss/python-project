import pickle
#initiate empty lists
recipe_list = []
ingredient_list = []

#function to calculate the difficulty of a recipe
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
        return difficulty
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
        return difficulty
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
        return difficulty
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "Hard"
        return difficulty


#function to take the recipe information
def take_recipe():
    name = input("Name of recipe: ")
    cooking_time = int(input("Cooking time (in minutes): "))
    ingredients = input("Ingredients (please separate by comma): ").split(", ")
    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }
    return recipe

#variable to ask user to input a current file name          
filename = input("Enter the filename where you've stred your recipes: ") + ".bin"
#open file and load the recipe data
try:
    recipe_file = open(filename, 'rb') 
    data = pickle.load(recipe_file)
#throw error if not found
except FileNotFoundError:
    print("File does not exist - exiting")
    data = {
        'recipe_list': recipe_list,
        'ingredient_list': ingredient_list
    }
#throw error if some other error happens
except:
    print("An unexpected error occurred.")
    data = {
        'recipe_list': recipe_list,
        'ingredient_list': ingredient_list
    }
#close file
else: 
    recipe_file.close()
#adding recipe information to lists
finally: 
    recipe_list = data['recipe_list']
    ingredient_list = data['ingredient_list']

#asking user for input  on how many recipe's they would like to add    
n = int(input("How many recipies would you like to enter?: "))
#loop through the recipe entered to add to ingredient list
for num in range(n):
    recipe = take_recipe()
    recipe_list.append(recipe)
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredient_list:
            ingredient_list.append(ingredient)
    

#opening file and updating
update_file = open(filename, 'wb')
pickle.dump(data, update_file)
update_file.close()
print("Recipes have been updated")