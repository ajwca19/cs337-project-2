# Importing necessary modules - commented-out code is necessary download steps that need to be run before modules are imported
import re
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

# Importing external files used in program
import web_scraping

# Obtaining list of ingredients and directions from specified recipe web link
recipe_link = "https://www.allrecipes.com/recipe/21176/baked-dijon-salmon/"
ingredients, directions = web_scraping.recipe_extract(recipe_link)

# Creating a list of units commonly used in cooking
units_list = ["ounce", "pinch", "dash", "cup", "gallon", "pint", "milliliter", "liter", "gram", "pound", "fluid ounce", "kilogram",
             "spoon", "quart", "container", "can", "box", "package", "packet", "tablespoon", "teaspoon", "small", "medium", "large", "stalk"]

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

# Stripping away stopwords, predetermined units and/or equipment from list of ingredients for direction parsing purposes
inflection_engine = inflect.engine()
new_ingredients = ingredients.copy()
for ingredient_idx, i in enumerate(ingredients):
    new_ingredients[ingredient_idx] = i.replace(',', "")
    new_sentence = new_ingredients[ingredient_idx]
    for word in new_ingredients[ingredient_idx].split(" "):
        for unit in units_list:
            if word == unit or word == inflection_engine.plural(unit):
                new_sentence = new_sentence.replace(word, "")
        for equipment in equipment_list:
            if word == equipment:
                new_sentence = new_sentence.replace(word, "")
    new_ingredients[ingredient_idx] = new_sentence

# Defining a function to determine whether or not a given direction word should be split up (can the word be a verb)
# Taken from https://www.reddit.com/r/LanguageTechnology/comments/egh7jk/how_to_check_if_a_word_can_be_interpreted_as_a/
def possible_verb(surface):
    return 'v' in set(s.pos() for s in wordnet.synsets(surface))

# Defining a function to generate a search table for the parsed directions
def direction_search_table(directions, ingredients, units_list, unit_conversion, equipment_list, units_of_time_list, temp_levels_list):
    direction_df = pd.DataFrame(columns = ['direction_index', 'raw_text', 'action', 'action_duration', 'action_temperature', 'action_details', 'ingredient_amount', 'ingredient_unit', 'ingredient_name', 'equipment'])
    direction_index = 0 # First direction in a recipe
    current_direction_length = len(directions)
    while direction_index < current_direction_length:
        # Creating a Doc object from the directions
        direction_doc = nlp(directions[direction_index])
        # Pulling out the relevant information from the dependency parsed directions
        raw_text = direction_doc.text
        action = ""
        action_duration = ""
        action_temperature = ""
        action_details = ""
        ingredient_amount = [] # stored as array so that corresponding unit can be retrieved w/ the same idx
        ingredient_unit = []  # stored as array so that corresponding amount can be retrieved w/ the same idx
        ingredient_name = [] # stored as array so that corresponding unit/amount can be retrieved w/ the same idx
        equipment = []
        direction_not_split = True
        duration_index = float('inf')
        for token_index, token in enumerate(direction_doc):
            token_is_action_preceded_by_and = possible_verb(token.text) and direction_doc[token_index-1].text == 'and'
            token_is_root = token.dep_ == 'ROOT'
            token_is_lower_range_of_action_duration = token.dep_ == 'quantmod' and token.head.dep_== 'nummod'
            token_is_higher_range_of_action_duration = token.dep_ == 'nummod' and token.head.text in units_of_time_list
            token_is_action_temperature = token.dep_ == 'nummod' and token.head.text == 'degrees'
            token_is_action_temperature_unit = (token.text == 'F' or re.match('[Ff]ahrenheit', token.text)) or (token.text == 'C' or re.match('[Cc]elsius', token.text))
            token_is_ingredient_amount_and_abbreviated_unit = direction_doc[token_index-1].pos_ == 'NUM' and token.text in unit_conversion.keys() and unit_conversion[token.text] in units_list
            token_is_ingredient_amount_and_unit = direction_doc[token_index-1].pos_ == 'NUM' and (token.text in units_list or inflection_engine.plural(token.text) in units_list)
            if token_is_action_preceded_by_and:
                and_space_str = "and "
                idx_of_and_action = raw_text.index(and_space_str + token.text)
                split_raw_text = raw_text.split(and_space_str, 1)
                first_half_of_raw_text = raw_text[ : idx_of_and_action]
                second_half_of_raw_text = raw_text[ idx_of_and_action + len(and_space_str) :].capitalize()
                # Altering directions array to reflect new sub-directions
                directions[direction_index] = split_raw_text[0] # Replace the original direction string with the first new direction
                directions.insert(direction_index+1, split_raw_text[1].capitalize()) # Insert the second new direction after the first
                current_direction_length += 1
                direction_not_split = False
                break
            elif token_is_root:
                action = token.text
            if token.text == "until":
                duration_index = token_index
            if token_index >= duration_index:
                action_duration += ' ' + token.text
                if token_index == len(direction_doc):
                    duration_index = float('inf')
            elif token_is_lower_range_of_action_duration:
                if token.text not in action_duration:
                    action_duration += token.text + ' '
            elif token_is_higher_range_of_action_duration:
                if token.text not in action_duration:
                    action_duration += token.text + ' ' + token.head.text        
            elif token_is_action_temperature:
                action_temperature = token.text + ' ' + token.head.text
            elif token_is_action_temperature_unit:
                action_temperature += ' ' + token.text
            elif token.text == "over":
                action_temperature += token.text
            elif "over" in action_temperature:
                if token.text in temp_levels_list or token.text == "heat":
                    action_temperature += ' ' + token.text
            elif token.text in temp_levels_list:
                action_temperature += token.text
            elif token_is_ingredient_amount_and_abbreviated_unit:
                ingredient_amount.append(direction_doc[token_index-1].text)
                ingredient_unit.append(unit_conversion[token.text])
            elif token_is_ingredient_amount_and_unit:
                ingredient_amount.append(direction_doc[token_index-1].text)
                ingredient_unit.append(token.text)
            if token.text != "'s":
                plural_version = inflection_engine.plural(token.text)
            elif token.text == "'s":
                plural_version = "'s"
            for i in ingredients:
                ingredient_words = i.split(" ")
                for ingredient_word in ingredient_words:
                    if (token.text == ingredient_word or plural_version == ingredient_word) and token.pos_ != 'NUM' and token.text not in ['and', 'a', 'or', 'of', 'into', 'cut', 'chopped', 'to']:
                        ingredient_name.append(token.text)
            for e in equipment_list:
                if token.text.lower() == e:
                    equipment_string = ''
                    equipment_adj_idx = token_index-1
                    while equipment_adj_idx > 0 and direction_doc[equipment_adj_idx].head.text == token.text and direction_doc[equipment_adj_idx].dep_ != 'det':
                        equipment_string = direction_doc[equipment_adj_idx].text + ' ' + equipment_string
                        equipment_adj_idx -= 1
                    equipment_string += token.text
                    equipment.append(equipment_string)
        if direction_not_split:
            new_row = {'direction_index': direction_index, 'raw_text': raw_text, 'action': action, 'action_duration': action_duration, 'action_temperature': action_temperature, 'action_details': action_details, 'ingredient_amount': ingredient_amount, 'ingredient_unit': ingredient_unit, 'ingredient_name': ingredient_name, 'equipment': equipment}
            direction_df = direction_df.append(new_row, ignore_index = True)
            direction_index += 1
    return direction_df

# Generating a search table for the parsed directions
direction_df = direction_search_table(directions, new_ingredients, units_list, unit_conversion, equipment_list, units_of_time_list, temp_levels_list)

# Defining a function to join ingredient names that are part of the same word - e.g., ["ground", "beef"] to ["ground beef"]
def ingredient_name_join(direction_df, ingredients):
    for ind in direction_df.index:
        ingredient_index = []
        for ing in direction_df['ingredient_name'][ind]:
            for i in range(len(ingredients)):
                if ing in ingredients[i] or ing[:-1] in ingredients[i]:
                    ingredient_index.append(i)
        new_ingredient_list = []
        dup = {x for x in ingredient_index if ingredient_index.count(x) > 1}
        for j in range(0, len(direction_df['ingredient_name'][ind])-1):
            if ingredient_index[j] == ingredient_index[j+1]:
                ingredients_joined = direction_df['ingredient_name'][ind][j] + " " + direction_df['ingredient_name'][ind][j+1]
                new_ingredient_list.append(ingredients_joined)
            elif ingredient_index[j] not in dup:
                new_ingredient_list.append(direction_df['ingredient_name'][ind][j])
            if j+1 == len(direction_df['ingredient_name'][ind])-1:
                if ingredient_index[j+1] not in dup:
                    new_ingredient_list.append(direction_df['ingredient_name'][ind][j+1])
        if len(direction_df['ingredient_name'][ind]) == 1:
            new_ingredient_list = direction_df['ingredient_name'][ind].copy()
        direction_df['ingredient_name'][ind] = new_ingredient_list.copy()
    return direction_df

# Joining ingredient names that are part of the same word - e.g., ["ground", "beef"] to ["ground beef"]
direction_df = ingredient_name_join(direction_df, ingredients)

# Defining a function to infer the ingredient amount and unit from the ingredient list, if none are provided
def ingredient_infer(direction_df, ingredients, units_list):
    for ind in direction_df.index:
        if len(direction_df['ingredient_name'][ind]) > 0 and len(direction_df['ingredient_amount'][ind]) == 0 and len(direction_df['ingredient_unit'][ind]) == 0:
            for ing in direction_df['ingredient_name'][ind]:
                for i in ingredients:
                    match_index = re.search(ing, i)
                    if not match_index:
                        match_index = re.search(ing[:-1], i)
                    if match_index:
                        i_extract = i[0:match_index.span()[0]]
                i_extract_list = i_extract.split(" ")
                for i_ex in i_extract_list:
                    if re.match('\d', i_ex):
                        direction_df['ingredient_amount'][ind].append(i_ex)
                    for unit in units_list:
                        if i_ex == unit or i_ex == inflection_engine.plural(unit):
                            direction_df['ingredient_unit'][ind].append(i_ex)
    return direction_df

# If there are ingredient names, but no amounts and units, then inferring the amount and unit from the ingredient list
direction_df = ingredient_infer(direction_df, ingredients, units_list)

# Defining a function to infer the equipment from the action, if no equipment is provided
def equipment_infer(direction_df):
    for ind in direction_df.index:
        if len(direction_df['equipment'][ind]) == 0:
            if direction_df['action'][ind].lower() == "preheat":
                direction_df['equipment'][ind].append("oven")
            if direction_df['action'][ind].lower() == "bake":
                direction_df['equipment'][ind].append("oven")  
            if direction_df['action'][ind].lower() == "broil":
                direction_df['equipment'][ind].append("oven")            
            if direction_df['action'][ind].lower() == "roast":
                direction_df['equipment'][ind].append("oven")
            if direction_df['action'][ind].lower() == "pulse":
                direction_df['equipment'][ind].append("food processor")
            if direction_df['action'][ind].lower() == "microwave":
                direction_df['equipment'][ind].append("microwave")
            if direction_df['action'][ind].lower() == "freeze":
                direction_df['equipment'][ind].append("freezer")
            if direction_df['action'][ind].lower() == "cut":
                direction_df['equipment'][ind].append("knife")            
            if direction_df['action'][ind].lower() == "chop":
                direction_df['equipment'][ind].append("knife")            
            if direction_df['action'][ind].lower() == "mince":
                direction_df['equipment'][ind].append("knife")
            if direction_df['action'][ind].lower() == "stir":
                direction_df['equipment'][ind].append("spoon")
    return direction_df

# If there is an action name but no equipment, then inferring the equipment from the action
direction_df = equipment_infer(direction_df)

# Defining a function to clean all elements of the directions search table
def directions_clean(direction_df):
    for ind in direction_df.index:
        direction_df['raw_text'][ind] = re.sub('\(|\)', "", direction_df['raw_text'][ind])
        direction_df['raw_text'][ind] = direction_df['raw_text'][ind].strip()
        direction_df['action'][ind] = re.sub('\(|\)', "", direction_df['action'][ind])
        direction_df['action'][ind] = direction_df['action'][ind].strip()
        direction_df['action_duration'][ind] = re.sub('\(|\)', "", direction_df['action_duration'][ind])
        direction_df['action_duration'][ind] = direction_df['action_duration'][ind].strip()
        direction_df['action_temperature'][ind] = re.sub('\(|\)', "", direction_df['action_temperature'][ind])
        direction_df['action_temperature'][ind] = direction_df['action_temperature'][ind].strip()
        direction_df['action_details'][ind] = re.sub('\(|\)', "", direction_df['action_details'][ind])
        direction_df['action_details'][ind] = direction_df['action_details'][ind].strip()
        new_list = []
        for x in direction_df['ingredient_amount'][ind]:
            x = re.sub('\(|\)', "", x)
            x = x.strip()
            new_list.append(x)
        direction_df['ingredient_amount'][ind] = new_list.copy()
        new_list = []
        for x in direction_df['ingredient_unit'][ind]:
            x = re.sub('\(|\)', "", x)
            x = x.strip()
            new_list.append(x)
        direction_df['ingredient_unit'][ind] = new_list.copy()
        new_list = []
        for x in direction_df['ingredient_name'][ind]:
            x = re.sub('\(|\)', "", x)
            x = x.strip()
            new_list.append(x)
        direction_df['ingredient_name'][ind] = new_list.copy()
        new_list = []
        for x in direction_df['equipment'][ind]:
            x = re.sub('\(|\)', "", x)
            x = x.strip()
            new_list.append(x)
        direction_df['equipment'][ind] = new_list.copy()
    return direction_df

# Cleaning all elements of the directions search table
direction_df = directions_clean(direction_df)


# Displaying the cleaned search table, not necessary for final program
# for i in range(len(direction_df)):
#     print(direction_df.loc[i].to_string())