import pickle 

with open('recipe_binary.bin', 'rb') as my_file: 
    recipe = pickle.load(my_file)

print("Recipe: ")
print("Name: " + recipe['name'])
print("Ingredients: " + str(recipe['ingredients']))
print("Cooking Time: " + str(recipe['cooking_time']) + " minutes")
print("Difficutly: " + recipe['difficulty'])