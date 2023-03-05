# Importing necessary modules
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import unicodedata
import spacy
import nltk
nltk.download('wordnet', quiet = True)
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from spacy import displacy
#python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")
import pandas as pd
import inflect
import googlesearch as search

import web_scraping
import direction_parsing
import ingredient_parsing

def main():
    # Creating a list of units commonly used in cooking
    units_list = ["ounce", "pinch", "dash", "cup", "gallon", "pint", "milliliter", "liter", "gram", "pound", "fluid ounce", "kilogram",
                 "spoon", "quart", "container", "can", "box", "package", "packet", "tablespoon", "teaspoon", "small", "medium", "large", "stalk", "clove", "head"]

    # Creating a dictionary of unit conversions
    unit_conversion = {"oz": "ounce", "c": "cup", "pt": "pint", "gal": "gallon", "ml": "milliliter", "mL": "milliliter",
                      "g": "gram", "lb": "pound", "kg": "kilogram", "kilo": "kilogram", "qt": "quart", "l": "liter", "L": "liter",
                      "tb": "tablespoon", "tbs": "tablespoon", "tbsp": "tablespoon", "tsp": "teaspoon"}

    # Creating a list of equipment commonly used in cooking
    equipment_list = ["pot", "pan", "sheet pan", "tray", "dish", "pressure cooker", "blender", "toaster", "microwave", "stove", "oven",
                      "range", "burner", "cooktop", "measuring cup", "bowl", "mixing bowl", "spoon", "fork", "knife", "ladle",
                      "spatula", "tongs", "paddle", "strainer", "mixer", "whisk", "toothpick", "foil", "parchment", "paper", "plastic wrap", "wrap",
                      "paper towel", "food processor", "processor", "skillet", "baking dish", "saute pan"]

    # Creating a list of units of time
    units_of_time_list = ["second", "seconds", "minute", "minutes", "hour", "hours"]

    # Creating a list of common temperature levels used in cooking
    temp_levels_list = ["low", "-", "medium", "high", "simmer", "boil"]
    
    while True:
        #enter a recipe to begin!
        print("Hi! I'm CARA - your Computer-Aided Recipe Assistant. Let's cook a meal!")
        recipe_url = input("Paste a recipe URL here to follow!")
    
        #scrape the recipe
        ingredients_raw, directions_raw = web_scraping.recipe_extract(recipe_link)
        if len(ingredients_raw) != 0 and len(directions_raw) != 0:
            print("Sounds delicious! I'm ready to go when you are!")
            break
        else:
            print("Sorry, I've never seen a recipe like this before. Can you try something different?")
    
    #get list of ingredients
    ingredients = ingredients_raw #will change this for project 3
    
    #get list of steps
    steps = direction_parsing.direction_search_table(directions_raw, ingredients, units_list, unit_conversion, equipment_list, units_of_time_list, temp_levels_list)
    
    #ask about initial viewing
    get_started = input("Do you want to [1] view the list of ingredients or [2] start with the cooking?")
    while True:
        if get_started == "1" or "ingredient" in get_started.lower():
            print("Got it. For this recipe, you will need...")
            for i in ingredients_raw:
                print(i)
            after_ingredients = input("Do you want to [1] ask questions about the ingredient list, or [2] get started cooking?")
            while after_ingredients == "1" or "question" in after_ingredients.lower() or "ingredient" in after_ingredients.lower():
                ingredient_question = input("Ask away!")
                answer_question(ingredient_question, ingredients_parsed, directions_parsed)
                after_ingredients = input("Do you want to [1] ask questions about the ingredient list, or [2] get started cooking?")
            print("Glad I could help! Let's get cooking!")
            break
        elif get_started == "2" or "start" in get_started.lower() or "cook" in get_started.lower():
            print("Let's get cooking!")
            break
        else:
            print("I'm sorry, I didn't quite get that. Let's try again!")
            get_started = input("Do you want to [1] view the list of ingredients or [2] start with the cooking?")
    
    assistant_guide = input("Before we get started, do you want to know what I can do? [Y/N]")
    if "y" in assistant_guide.lower():
        print("Okay! Here's a list of things that you can ask me about:")
        print("")
    elif "n" in assistant_guide.lower():
        print("Don't worry, I'm itching to get started too.")
    else:
        print("I didn't quite get that. We can get started, but try to be nicer next time! I can only help you if I know what you're asking.")
    #read out the first step of a recipe
    step_ptr = 0
    
    #start asking questions/navigating
    while True:
        question = input()
        if re.search("[Ll]ast|[Pp]revious|[Bb]ack|[Bb]efore", question):
            #question is going back a step
            print("Sure, we can go back a step!\nThe previous step says the following:")
            step_ptr-=1
            print(steps[step_ptr])
        elif re.search("[Rr]epeat|[Aa]gain|[Oo]n(c)?e more", question):
            #question is repeating the most recent step
            print("One more time? Okay! You need to do the following:")
            print(steps[step_ptr])
        elif re.search("[Nn]ext|[Aa]fter|O[Kk](ay)?|[Yy]es", question):
            #question is asking to move forward
            print("The next step says to do the following:")
            step_ptr+=1
            print(steps[step_ptr])
        elif re.search("[Hh]ow", question):
            if re.search("[Hh]ow long", question):
                #talking about time
                print()
            if re.search("[Hh]ow (hot|cold|warm|high|low)", question):
                #talking about temperature
                print()
        elif contains_ingredient(question):
            print()
        elif "quit" in question or step_ptr:
            break
        else:
            print("Sorry, I didn't quite get what you were saying. Maybe Google has an answer...")
            look_it_up(question, good_question = False)

#def answer_question(question, ingredients, directions):
    
def look_it_up(query, good_question = True):
    if good_question:
        print("I don't know off the top of my head. Let me google that!")
    for i in search(query, num_results = 100):  
        print("I found a source that might help: " + i)
        go_again = input("Do you need to see another site? [Y/N]")
        if go_again.lower() == "n" or go_again.lower() == "no":
            print("Great! Glad I could help.")
            break
        elif go_again.lower() != "y" and go_ahead.lower() != "yes":
            print("I didn't quite get that, but I'm assuming you're good for now.")
            break
            
if __name__ == "__main__":
    main()