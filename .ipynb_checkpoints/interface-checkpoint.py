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
    units_of_time_list = ["second", "seconds", "minute", "minutes", "hour", "hours", "day", "days", "overnight"]

    # Creating a list of common temperature levels used in cooking
    temp_levels_list = ["low", "-", "medium", "high", "simmer", "boil"]
    
    while True:
        #enter a recipe to begin!
        print("Hi! I'm CARA - your Computer-Aided Recipe Assistant. Let's cook a meal!")
        recipe_url = input("Paste a recipe URL here to follow!")
        while not re.match("^http(s)?://[a-zA-Z0-9;,/?:@&=+$-_.!~*'()#]+$", recipe_url):
            print("This doesn't look like a URL to me:")
            recipe_url = input("Paste a recipe URL here to follow!")
        #scrape the recipe
        ingredients_raw, directions_raw = web_scraping.recipe_extract(recipe_url)
        if len(ingredients_raw) != 0 and len(directions_raw) != 0:
            print("Sounds delicious! I'm ready to go when you are!")
            break
        else:
            print("Sorry, I've never seen a recipe like this before. Can you try something different?")
    
    #get list of ingredients
    ingredients = ingredients_raw #will change this for project 3
    
    #get list of steps
    steps = direction_parsing.direction_search_table(directions_raw, ingredients, units_list, unit_conversion, equipment_list, units_of_time_list, temp_levels_list)
    
    print("I just looked it over: the recipe you picked calls for " + str(len(ingredients)) + " ingredients and has " 
         + str(len(steps)) + " steps.")
    
    #ask about initial viewing
    get_started = input("Do you want to [1] view the list of ingredients or [2] start with the cooking?")
    while True:
        if get_started == "1" or "ingredient" in get_started.lower():
            print("Got it. For this recipe, you will need...\n")
            for i in ingredients_raw:
                print(i)
            after_ingredients = input("\nDo you want to [1] ask questions about the ingredient list, or [2] get started cooking?")
            while after_ingredients == "1" or "question" in after_ingredients.lower() or "ingredient" in after_ingredients.lower():
                ingredient_question = input("Ask away!")
                if re.search("substitut[e|ion]|replace", ingredient_question):
                    #REPLACE THIS WHEN IT'S DONE
                    print("I'm still learning how to substitute ingredients in a recipe. For now, I'll let Google answer.")
                    look_it_up(ingredient_question, good_question = False)
                elif re.search("[Ww]hat (is|are)", ingredient_question):
                    look_it_up(ingredient_question)
                else:
                    print("I'm not sure how to answer that. I'll ask Google for you!")
                    look_it_up(ingredient_question, good_question = False)
                after_ingredients = input("Do you [1] have more questions or [2] want to get started cooking?")
            print("Glad I could help! Let's get cooking!")
            break
        elif get_started == "2" or "start" in get_started.lower() or "cook" in get_started.lower():
            print("Let's get cooking!")
            break
        else:
            print("I'm sorry, I didn't quite get that. Let's try again!")
            get_started = input("Do you want to [1] view the list of ingredients or [2] start with the cooking?")
    
    assistant_guide = input("Before we get started, do you want to know what I can do? [Y/N]")
    if "y" == assistant_guide.lower() or "yes" in assistant_guide.lower():
        #give a list of sample questions
        print("Okay! Here's a list of things that you can ask me about:")
        print("Recipe navigation: ask me to move forward, back, or repeat a step")
        print("Cooking explainers: ask me how to do something, or what an unfamiliar piece of equipment or ingredient is")
        print("Recipe clarifications: ask me how much of something you need, how long it cooks for, how hot, etc.")
        print("Ingredient substitutions: I'm still learning, but ask me if you need to replace something")
        print("If you're ever confused, type \"help\". If you want to quit recipe guidance, I won't be offended either. Just type \"quit\" at any point")
        print("Let's get started with the recipe!")
    elif "n" == assistant_guide.lower() or "no" in assistant_guide.lower():
        print("Don't worry, I'm itching to get started too.")
    else:
        print("I didn't quite get that. We can get started, but try to be nicer next time! I can only help you if I know what you're asking.")
    #read out the first step of a recipe
    step_ptr = 0
    print("Step 1: " + steps.loc[step_ptr].raw_text)
    
    
    #start asking questions/navigating
    while True:
        question = input()
        #navigation takes priority
        if re.search("step", question) and re.search("[0-9]+", question):
            new_step = int(re.search("[0-9]+", question)[0])
            if new_step <= len(steps) and new_step > 0:
                print("Moving you to step " + str(new_step) + ".")
                step_ptr = new_step - 1
                print("Step " + str(new_step) + ": " + steps.loc[step_ptr].raw_text)
                continue
            else:
                print("That's an invalid step number. Sorry!")
        elif re.search("[Ll]ast|[Pp]revious|[Bb]ack|[Bb]efore", question):
            #question is going back a step
            print("Sure, we can go back a step!\nThe previous step says the following:")
            step_ptr-=1
            print("Step " + str(step_ptr + 1) +": " + steps.loc[step_ptr].raw_text)
            continue
        elif re.search("[Rr]epeat|[Aa]gain|[Oo]n(c)?e more", question):
            #question is repeating the most recent step
            if re.search("[Ii]ngredient", question):
                print("Here's the list of ingredients for the recipe once more:")
                for i in ingredients_raw:
                    print(i)
            else:
                print("One more time? Okay! You need to do the following:")
                print(steps.loc[step_ptr].raw_text)
        elif re.search("[Nn]ext|[Aa]fter|O[Kk](ay)?|[Yy]es", question):
            #question is asking to move forward
            if step_ptr < len(steps) - 1:
                print("The next step says to do the following:")
                step_ptr+=1
                print("Step " + str(step_ptr + 1) +": " + steps.loc[step_ptr].raw_text)
                continue
            else:
                print("We're on the last step already!")
                keep_going = input("Do you have any more questions? [Y/N]")
                if keep_going.lower() == "y" or "yes" in keep_going.lower():
                    print("Ask away!")
                    continue
                elif keep_going.lower() == "n" or "no" in keep_going.lower() or "quit" in keep_going.lower():
                    print("Thanks for working with me! Bon appetit!")
                    break
                else:
                    print("I didn't quite catch that, but I think you're good to go! Bon appetit!")
                    break
        elif re.search("[Ww]hat step", question) or re.search("[Hh]ow many steps", question):
            #question is asking what step I'm on
            print("You're on step " + str(step_ptr + 1) + " out of " + str(len(steps)))
        
        #question is asking about a replacement or substitution
        elif re.search("substitut(e|ion)|replace", question):
            print("I'm still learning how to substitute ingredients in a recipe. For now, I'll let Google answer.")
            look_it_up(ingredient_question, good_question = False)
                
        #other questions that contain the word how
        elif re.search("[Hh]ow", question):
            if re.search("[Hh]ow long", question):
                #talking about time
                if steps.loc[step_ptr].action_duration != "":
                    #there's some duration mentioned
                    print(steps.loc[step_ptr].action_duration)
                else:
                    print("I can't find anything in this step about time. Let me look around.")
                    step, duration = nearest_field("duration", step_ptr, ingredients, steps)
                    print("I found this information in step " + str(step) + ". I hope it helps: " + str(duration))
            elif re.search("[Hh]ow (hot|cold|warm|high|low)", question):
                if steps.loc[step_ptr].action_temperature != "":
                    #there's some temperature mentioned
                    print(steps.loc[step_ptr].action_temperature)
                else:
                    print("I can't find anything in this step about temperature. Let me look around.")
                    step, temperature = nearest_field("temperature", step_ptr, ingredients, steps)
                    print("I found this information in step " + str(step) + ". I hope it helps: " + str(temperature))
            elif re.search("[Hh]ow (much|many)", question):
                about_time = False
                for unit in units_of_time_list:
                    if re.search(unit, question):
                        about_time = True
                if about_time:
                    #question is about duration
                    if steps.loc[step_ptr].action_duration != "":
                        #there's some duration mentioned in the step
                        print(steps.loc[step_ptr].action_duration)
                    else:
                        print("I can't find anything in this step about time. Let me look around.")
                        step, duration = nearest_field("duration", step_ptr, ingredients, steps)
                        print("I found this information in step " + str(step) + ". I hope it helps: " + str(duration))
                else:
                    #question is about quantity
                    relevant_ingredient = identify_relevant_ingredient(question, ingredients, units_list, unit_conversion)
                    if relevant_ingredient == "":
                        print("I can't tell which ingredient you're asking about. Can you rephrase the question?")
                        continue
                    else:
                        local_amount = steps.loc[step_ptr].ingredient_amount
                        local_units = steps.loc[step_ptr].ingredient_unit
                        if len(local_amount) == 0:
                            print("The recipe calls for " + relevant_ingredient)
                        else:
                            local_ingredients = steps.loc[step_ptr].ingredient
                            ingredient_index = -1
                            for i in range(len(local_ingredients)):
                                if re.search(local_ingredients[i], relevant_ingredient):
                                    #the amount is specified in the step
                                    print("This step calls for " + str(local_amount[i]) + " " + str(local_units[i]) + " " + str(local_ingredients[i]))
                            if ingredient_index == -1:
                                print("I couldn't find any information in this step. The recipe calls for " + relevant_ingredient)
            
            #HOW TO/HOW DO I SHOULD BE THE LOWEST PRIORITY "HOW" QUESTION ANSWERED
            elif re.search("[Hh]ow (do|to)", question):
                all_actions = steps["action"].tolist()
                found_action = False
                for action in all_actions:
                    if action.lower() in question:
                        #the question is a valid one to ask Google
                        print("I don't know how to " + action.lower() + ". Let me ask Google!")
                        found_action = True
                        look_it_up(question, good_question = False)
                if found_action == False:
                    #simple "How do I do that" inferring an answer
                    predicted_action = steps.loc[step_ptr].action
                    if predicted_action != "":
                        print("I don't know how to " + predicted_action.lower() + ". I'll ask Google.")
                        look_it_up("how to "+ predicted_action.lower(), good_question = False)
                    else:
                        print("I can't figure out what you're asking me about.")
                        look_it_up("how to " + input("What am I asking Google how to do?"), good_question = False)
            else:
                print("I don't understand your question. Can you ask it again a different way?")
                continue

        #questions that contain the word what
        elif re.search("[Ww]hat", question):
            if re.search("ingredient", question):
                if len(steps.loc[step_ptr].ingredient_name) > 0:
                    print(pretty_list_print(steps.loc[step_ptr].ingredient_name))
                else:
                    print("I can't find anything about ingredients in this step.")
                    where_to_look = input("Should I [1] look around to nearby steps, or [2] tell you the ingredient list again?")
                    if "1" in where_to_look:
                        print("Okay. I'll look now.")
                        step, ingredient_name = nearest_field("ingredient", step_ptr, ingredients, steps)
                        print("I found this information in step " + str(step) + ". I hope it helps: " + pretty_list_print(ingredient_name))
                    elif "2" in where_to_look:
                        print("Here's the list of ingredients for the whole recipe:")
                        for i in ingredients_raw:
                            print(i)
                    else:
                        print("I didn't quite get that. Here's the ingredients for the entire recipe:")
                        for i in ingredients_raw:
                            print(i)
            elif re.search("temperature|heat", question):
                if steps.loc[step_ptr].action_temperature != "":
                    #there's some temperature mentioned
                    print(steps.loc[step_ptr].action_temperature)
                else:
                    print("I can't find anything in this step about temperature. Let me look around.")
                    step, temperature = nearest_field("temperature", step_ptr, ingredients, steps)
                    print("I found this information in step " + str(step) + ". I hope it helps: " + str(temperature))
            elif re.search("time", question):
                #talking about time
                if steps.loc[step_ptr].action_duration != "":
                    #there's some duration mentioned
                    print(steps.loc[step_ptr].action_duration)
                else:
                    print("I can't find anything in this step about time. Let me look around.")
                    step, duration = nearest_field("duration", step_ptr, ingredients, steps)
                    print("I found this information in step " + str(step) + ". I hope it helps: " + str(duration))
            elif re.search("amount|quantity", question):
                #talking about quantity
                #question is about quantity
                relevant_ingredient = identify_relevant_ingredient(question, ingredients, units_list, unit_conversion)
                if relevant_ingredient == "":
                    print("I can't tell which ingredient you're asking about. Can you rephrase the question?")
                    continue
                else:
                    local_amount = steps.loc[step_ptr].ingredient_amount
                    local_units = steps.loc[step_ptr].ingredient_unit
                    if len(local_amount) == 0:
                        print("The recipe calls for " + relevant_ingredient)
                    else:
                        local_ingredients = steps.loc[step_ptr].ingredient
                        ingredient_index = -1
                        for i in range(len(local_ingredients)):
                            if re.search(local_ingredients[i], relevant_ingredient):
                                #the amount is specified in the step
                                print("This step calls for " + str(local_amount[i]) + " " + str(local_units[i]) + " " + str(local_ingredients[i]))
                        if ingredient_index == -1:
                            print("I couldn't find any information in this step. The recipe calls for " + relevant_ingredient)
            #WHAT IS QUESTIONS HAVE LOWEST PRIORITY
            elif re.search("[Ww]hat (is|are)", question):
                if re.search("this|that|these|those", question):
                    potential_topics = steps.loc[step_ptr].ingredient.append(steps.loc[step_ptr].equipment)
                    if len(potential_topics) == 1:
                        print("I don't know much about " + potential_topics[0] + ". I'll ask Google!")
                        look_it_up("what is " + potential_topics[0], good_question = False)
                    else:
                        print("I can't tell what you're asking about.")
                        look_it_up("what is " + input("What do you want to learn more about?"), good_question = False)
                else:
                    if re.search("is", question):
                        print("I don't know what that is, but I can ask Google for you!")
                        look_it_up(question, good_question = False)
                    else:
                        print("I don't know what those are, but I can ask Google for you!")
                        look_it_up(question, good_question = False)
            else:
                print("I don't understand your question. Can you ask it another way?")
                continue
                    
        #metadata/control of the application            
        elif question.lower() == "quit":
            break
        elif question.lower() == "help":
            print("Okay! Here's a list of things that you can ask me about:")
            print("Recipe navigation: ask me to move forward, back, or repeat a step")
            print("Cooking explainers: ask me how to do something, or what an unfamiliar piece of equipment or ingredient is")
            print("Recipe clarifications: ask me how much of something you need, how long it cooks for, how hot, etc.")
            print("Ingredient substitutions: I'm still learning, but ask me if you need to replace something")
            print("If you're ever confused, type \"help\". If you want to quit recipe guidance, I won't be offended either. Just type \"quit\" at any point")
            print("Let's get back to cooking now.")
            
        #other fun little quirky answers    
        elif question == "" or re.match("^[ \n\t]+$", question):
            print("Why so quiet? Ask something else.")
            continue
        elif re.search("[Tt]hank(s| you)", question):
            print("You're welcome!")
        
        #question answering via google
        else:
            print("Sorry, I didn't quite get what you were saying. Maybe Google has an answer...")
            look_it_up(question, good_question = False)
            
        #finished answering a question, ask if you want to move on
        if step_ptr < len(steps) - 1:
            move_on = input("Would you like to move on to step " + str(step_ptr + 2) + "? [Y/N]")
            if "y" == move_on.lower() or "yes" in move_on.lower():
                print("Sure thing!")
                step_ptr += 1
                print("Step " + str(step_ptr + 1) +": " + steps.loc[step_ptr].raw_text)
            elif "n" == move_on.lower() or "no" in move_on.lower():
                print("Okay!")
            else:
                print("I didn't quite get that. We can stay on this step for now.")
        else:
            #we're on the last step!
            print("We're on the last step already!")
            keep_going = input("Do you have any more questions? [Y/N]")
            if keep_going.lower() == "y" or "yes" in keep_going.lower():
                print("Ask away!")
                continue
            elif keep_going.lower() == "n" or "no" in keep_going.lower() or "quit" in keep_going.lower():
                print("Thanks for working with me! Bon appetit!")
                break
            else:
                print("I didn't quite catch that, but I think you're good to go! Bon appetit!")
                break
        

def nearest_field(field, step_ptr, ingredients, steps):
    #look before
    before_ptr = step_ptr - 1
    before_step = -1000
    before_answer = ""
    while before_ptr >= 0:
        if field == "duration":
            if steps.loc[before_ptr].action_duration != "":
                before_step = before_ptr
                before_answer = steps.loc[before_ptr].action_duration
                break
        elif field == "action":
            if steps.loc[before_ptr].action != "":
                before_step = before_ptr
                before_answer = steps.loc[before_ptr].action
                break
        elif field == "temperature":
            if steps.loc[before_ptr].action_temperature != "":
                before_step = before_ptr
                before_answer = steps.loc[before_ptr].action_temperature
                break
        elif field == "equipment":
            if steps.loc[before_ptr].equipment != "":
                before_step = before_ptr
                before_answer = steps.loc[before_ptr].equipment
                break
        elif field == "ingredient":
            if steps.loc[before_ptr].ingredient_name != []:
                before_step = before_ptr
                before_answer = steps.loc[before_ptr].ingredient_name
                break
        elif field == "amount":
            if steps.loc[before_ptr].ingredient_amount != []:
                before_step = before_ptr
                before_answer = steps.loc[before_ptr].ingredient_amount #CHANGE ME
                break
        else:
            return (-1, "")
        before_ptr -= 1
    after_ptr = step_ptr + 1
    after_step = 1000
    after_answer = ""
    while after_ptr < len(steps):
        if field == "duration":
            if steps.loc[after_ptr].action_duration != "":
                after_step = after_ptr
                after_answer = steps.loc[after_ptr].action_duration
                break
        elif field == "action":
            if steps.loc[after_ptr].action != "":
                after_step = after_ptr
                after_answer = steps.loc[after_ptr].action
                break
        elif field == "temperature":
            if steps.loc[after_ptr].action_temperature != "":
                after_step = after_ptr
                after_answer = steps.loc[after_ptr].action_temperature
                break
        elif field == "equipment":
            if steps.loc[after_ptr].equipment != "":
                after_step = after_ptr
                after_answer = steps.loc[after_ptr].equipment
                break
        else:
            return (-1, "")
        after_ptr += 1
    if after_step - step_ptr < step_ptr - before_step:
        return (after_step, after_answer)
    else:
        return (before_step, before_answer)
    
def pretty_list_print(string_list):
    final_string = ""
    for i in range(len(string_list) - 1):
        final_string += string_list[i] + ", "
    final_string += string_list[-1]
    return final_string

def look_it_up(query, good_question = True):
    if good_question:
        print("I don't know off the top of my head. Let me google that!")
    try:
        search_results = search.search(query, num_results = 10)
        for i in search_results:  
            print("I found a source that might help: " + i)
            go_again = input("Do you need to see another site? [Y/N]")
            if go_again.lower() == "n" or go_again.lower() == "no":
                print("Great! Glad I could help.")
                break
            elif go_again.lower() != "y" and go_again.lower() != "yes":
                print("I didn't quite get that, but I'm assuming you're good for now.")
                break
        print("I'm fresh out of sources! Better luck next time.")
    except:
        print("Google's not having a good time with that question for some reason. Guess it'll have to go unanswered. Sorry!")
        return

def identify_relevant_ingredient(question, ingredients_list, units_list, units_conversion): 
    parsed_question = nlp(question)
    for token in parsed_question:
        if re.search("[Hh]ow", token.text):
            continue
        elif re.search("many|much", token.text):
            continue
        elif token.lemma_ in units_list or token.text in units_conversion.keys():
            continue
        elif token.text in ["of", "in"]:
            continue
        elif token.pos_ != "NOUN":
            continue
        else:
            for ingredient in ingredients_list:
                if token.text in ingredient:
                    return ingredient
            return ""
    
if __name__ == "__main__":
    main()