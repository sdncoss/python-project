
class Recipe(object):
    #initial variable for all ingredients
    all_ingredients = []
    #initial method for recipe information
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None
    #getter for name    
    def get_name(self):
        return self.name
    #setter for name
    def set_name(self, name):
        self.name = name
    #getter for cooking time    
    def get_cooking_time(self):
        return self.cooking_time
    #setter for cooking time
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        
    #method to add ingredients 
    def add_ingredients(self, *ingredients):
        for ingredient in ingredients:
            if not ingredient in self.ingredients:
                self.ingredients.append(ingredient)
                self.update_all_ingredients()
            else:
                print("Ingredient -" + str(item) + "- already listed in ingredients.")
    #getter for ingredients added        
    def get_ingredient(self):
        print("-------------------------------------------")
        print("Ingredients: ")
        for ingredient in self.ingredients:
            print("-" + ingredient)
    #method for determining difficulty of recipe        
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"
    #getter for difficulty calculation    
    def get_difficulty(self):
        if not self.difficulty:
            self.calculate_difficulty()
        return self.difficulty
    #method to search recipe's by ingredient
    def search_ingredient(self, ingredients):
        for ingredient in self.ingredients:
            if ingredient == ingredients:
                return True
            else: 
                return False
    #method ot update all ingredient variable
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if not ingredient in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)
    #method to create string for output in console    
    def __str__(self):
        output = "----------------------------" + \
            "\nRecipe: " + self.name + \
            "\nCooking Time: " + str(self.cooking_time) + " mins" + \
            "\nIngredients: " + str(self.ingredients) + \
            "\nDifficulty: " + str(self.difficulty)
        return output
    #method to search recipe's by name 
    def recipe_search(data, search_term):
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe)
#variable for all recipes        
recipes_list = []    
        
tea = Recipe("Tea")
tea.add_ingredients("Water", "Tea Leaves", "Sugar")
tea.set_cooking_time(5)
tea.get_difficulty()


coffee = Recipe("Coffee")
coffee.add_ingredients("Water", "Coffee Powder", "Sugar")
coffee.set_cooking_time(5)
coffee.get_difficulty()

cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
cake.get_difficulty()

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)
banana_smoothie.get_difficulty()

recipes_list.append(tea)
recipes_list.append(coffee)
recipes_list.append(cake)
recipes_list.append(banana_smoothie)

print(".....................................")
print("Search: Water")
Recipe.recipe_search(recipes_list, "Water")

print(".....................................")
print("Search: Sugar")
Recipe.recipe_search(recipes_list, "Sugar")

print(".....................................")
print("Search: Bananas")
Recipe.recipe_search(recipes_list, "Bananas")