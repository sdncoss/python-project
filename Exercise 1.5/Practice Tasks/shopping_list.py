#initiate class for shopping list
class ShoppingList(object):
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []
    #add to list method
    def add_item(self, item):
        if not item in self.shopping_list:
            self.shopping_list.append(item)
        else:
            print("Item " + str(item) + " already in shopping list.")
    #remove from list method        
    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
    #view whole list method 
    def view_list(self):
        print("....................")
        print(self.list_name)
        for item in self.shopping_list:
            print(item)
            
    #merge lists method
    def merge_lists(self, obj):
        merged_lists_name = "Merged List - " + str(self.list_name) + " + " + str(obj.list_name)
        merged_lists_obj = ShoppingList(merged_lists_name)
        merged_lists_obj.shopping_list = self.shopping_list.copy()
        
        for item in obj.shopping_list:
            if not item in merged_lists_obj.shopping_list:
                merged_lists_obj.shopping_list.append(item)
        return merged_lists_obj
     
#initiate list name   
pet_store_list = ShoppingList("Pet Store Shopping List")
grocery_store_list = ShoppingList("Grocery Store List")

#add items to shopping list
for item in ['fruits' ,'vegetables', 'bowl', 'ice cream']:
    grocery_store_list.add_item(item)
    
pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")
#remove item from shopping list
pet_store_list.remove_item("flea collars")
#check to see if adding same item 
pet_store_list.add_item("frisbee")
#view whole list
pet_store_list.view_list()

merged_list = ShoppingList.merge_lists(pet_store_list, grocery_store_list)
merged_list.view_list()
