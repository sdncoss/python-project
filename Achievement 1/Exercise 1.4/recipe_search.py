import pickle

#fucntion that will print the information of the recipe
def display_recipe(recipe):
    print("-----------------------------")
    print("Recipe: ", recipe['name'])
    print("Cooking Time: ", recipe['cooking_time'], "minutes")
    print("Ingredients: ")
    for i in recipe['ingredients']:
        print("- ", i)
    print("Difficulty: ", recipe['difficulty'])
    print("----------------------------")

#function to search for an ingredient in data dictionary    
def search_ingredient(data):
    #creates number for each ingredient in list
    listed_ingredients = enumerate(data['ingredient_list'])
    numbered_ingredient = list(listed_ingredients)
    print("Ingredient List:")
    for i in numbered_ingredient:
        print("- ", i[0], i[1])
    
    try:
        num = int(input("Please enter the number correspoding with the ingredient you would like to search: "))
        ingredient_searched = numbered_ingredient[num][1]
    except:
        print("Please search by number only.")
    else: 
        for i in data['recipe_list']:
            if ingredient_searched in i['ingredients']:
                print(display_recipe(i))
        
        
#asking user for file to save data to     
filename = input("Enter the name of the file you would like to save to: ")        
try:
    file = open(filename, 'rb')
    data = pickle.load(file)
except FileNotFoundError:
    print("File does not exist")
except:
    print("Unexpected error")
else:
    file.close()
    search_ingredient(data)