from allrecipes import AllRecipes
import pandas as pd

# Ask for ingredients
def ingredientInput(ingredients):
    # Ask user for ingredients list and keep going
    print("Please enter the ingredients you have: (hit Enter twice to end)")
    counter = 1
    while True:
        user_input = input("Enter ingredient {}: ".format(counter))
        if not user_input.strip():
            break
        ingredients.append(user_input)
        counter += 1
    print("Ingredients entered:", ingredients)

def exclingredientInput(ingredients):
    # Ask user for ingredients list and keep going
    print("Please enter the ingredients you do not want in your recipe: (hit Enter twice to end)")
    counter = 1
    while True:
        user_input = input("Enter ingredient {}: ".format(counter))
        if not user_input.strip():
            break
        ingredients.append(user_input)
        counter += 1

    print("Ingredients entered:", ingredients)

    # Check if user wants to add more ingredients
    ans = input("Would you like to add more ingredients? (Yes/No): ")
    while ans.lower() in ["yes", "y"]:
        user_input = input("Enter ingredient {}: ".format(counter))
        if not user_input.strip():
            break
        ingredients.append(user_input)
        counter += 1
        ans = input("Would you like to add more ingredients? (Yes/No): ")

def main():
    # User input
    print("Welcome to Recip.io! To get started, please choose \nwhether you would like to type or take a picture of your ingredients ")
    user_input = input("Please enter \"TYPE\" or \"PICTURE\": ")

    if user_input.upper() == "TYPE":
        # Empty ingredients list
        ingredients = []
        exclIngred = []
        ingredientInput(ingredients)
        exclingredientInput(exclIngred)

        #if ingredients list is still empty, ask again
        while ingredients == []:
            print("No ingredients were entered. \n")
            ingredientInput(ingredients)
            
        # Search:
        query = " ".join(ingredients)
        print("Searching for recipes with ingredients:", query)
        # Perform search based on the concatenated query
        recipe_result = AllRecipes.search(query)
        # exit()

        # Get the main recipe URL from the search results
        if recipe_result:
            #REMOVE INGREDIENTS 
            main_recipe_url = recipe_result[0]['url']
            # Get the detailed information about the first recipe
            detailed_recipe = AllRecipes.get(main_recipe_url)

            

            # Display result:
            print("## %s:" % detailed_recipe['name'])  # Name of the recipe
            # Print other details of the recipe (like ingredients and steps) as needed
        else:
            print("No recipes found for the provided ingredients.")

    elif user_input.upper() == "PICTURE":
        print("I am sorry, we do not have that feature right now!")
    else:
        print("Invalid input. Please enter \"TYPE\" or \"PICTURE\".")

    # Search:
    comboList = ingredients + exclIngred
    print(comboList)
    query_result = AllRecipes.search(ingredients)
    eclquery_result = AllRecipes.search(comboList)

    for recipe in query_result:
        for excl in eclquery_result:
            if(recipe == excl):
                query_result.remove(recipe)

    print(query_result)
    #print(list(set(query_result.intersection(eclquery_result))))
    # Get:
    main_recipe_url = query_result[0]['url']
    detailed_recipe = AllRecipes.get(main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)

    
    # Calling DataFrame constructor on list

    df = pd.DataFrame(query_result)
    print(df)

    filtered_data = df[['name', 'rate']]

    #descending
    filtered_data = filtered_data.sort_values(by='rate', ascending=False)
    print(filtered_data)
    query_result = AllRecipes.search(query)

main()