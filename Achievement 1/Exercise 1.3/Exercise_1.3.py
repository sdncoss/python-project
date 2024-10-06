recipe_list = []
ingredient_list = []

def take_recipe():
    name = input("Name of recipe: ")
    cooking_time = int(input("Cooking time: "))
    ingredients = input("Ingredients: ").split(", ")
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    return recipe

n = int(input("How many recipies would you like to enter?: "))

for num in range(n): 
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if not ingredient in ingredient_list:
            ingredient_list.append(ingredient)
    recipe_list.append(recipe)

for recipe in recipe_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = "Easy"
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = "Medium"
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = "Intermediate"
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = "Hard"

for recipe in recipe_list:
    print("Recipe: ", recipe['name'])
    print("Cooking time: ", recipe['cooking_time'], "minutes")
    print("Ingredients: ")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print("Difficulty: ", recipe['difficulty'])

def all_ingredients():
    ingredient_list.sort()
    print("......................................")
    print("Ingredients available for all recipies")
    print("--------------------------------------")
    for ingredient in ingredient_list:
        print(ingredient)

all_ingredients()