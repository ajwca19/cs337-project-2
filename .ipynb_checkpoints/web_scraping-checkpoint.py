# Importing necessary modules
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import unicodedata

# Defining a function to extract the HTML class and tag key words to search for ingredients
def ingredient_class_tag(recipe_html):
    # HTML class
    ingredients_class = re.findall('class=".*[Ii]ngredients[^ ]*"', str(recipe_html))
    ingredients_class_dict = dict(Counter(ingredients_class))
    most_common_ingredients_class = ""
    max_value = 0
    for key, value in ingredients_class_dict.items():
        if value > max_value:
            most_common_ingredients_class = key
            max_value = value
        elif value == max_value:
            if "label" in key.lower():
                most_common_ingredients_class = key
    most_common_ingredients_class = re.sub('class=|"', '', most_common_ingredients_class)
    # HTML tag
    tag_list = re.findall(rf'<.*{most_common_ingredients_class}.*>', str(recipe_html))
    clean_tag_list = []
    for t in tag_list:
        tag = re.search('<.* class', t)
        if tag:
            tag = re.sub('<| class', '', tag[0])
            clean_tag_list.append(tag)
    ingredients_tag_dict = dict(Counter(clean_tag_list))
    most_common_ingredients_tag = ""
    max_value = 0
    for key, value in ingredients_tag_dict.items():
        if value > max_value:
            most_common_ingredients_tag = key
            max_value = value
    return (most_common_ingredients_class, most_common_ingredients_tag)

# Defining a function to extract the HTML class and tag key words to search for directions
def direction_class_tag(recipe_html):
    # HTML class
    directions_class = re.findall('class=".*[Mm]ethod[^ ]*"|class=".*comp mntl-sc-block mntl-sc-block-html[^ ]*"', str(recipe_html))
    directions_class_dict = dict(Counter(directions_class))
    most_common_directions_class = ""
    max_value = 0
    for key, value in directions_class_dict.items():
        if value > max_value:
            most_common_directions_class = key
            max_value = value
    most_common_directions_class = re.sub('class=|"', '', most_common_directions_class)    
    # HTML tag
    tag_list = re.findall(rf'<.*{most_common_directions_class}.*>', str(recipe_html))
    clean_tag_list = []
    for t in tag_list:
        tag = re.search('<.* class', t)
        if tag:
            tag = re.sub('<| class', '', tag[0])
            clean_tag_list.append(tag)
    directions_tag_dict = dict(Counter(clean_tag_list))
    most_common_directions_tag = ""
    max_value = 0
    for key, value in directions_tag_dict.items():
        if value > max_value:
            most_common_directions_tag = key
            max_value = value
    return (most_common_directions_class, most_common_directions_tag)

# Defining a function to extract the ingredients and directions from an online recipe
def recipe_extract(URL):
    # Getting HTML of selected recipe
    webpage = requests.get(URL)
    recipe_html = BeautifulSoup(webpage.content, "html.parser")
    # Extracting the HTML class and tag key words to search for ingredients
    most_common_ingredients_class, most_common_ingredients_tag = ingredient_class_tag(recipe_html)
    # Extracting the ingredients and storing in list                
    ingredients_text = recipe_html.find_all(most_common_ingredients_tag, class_ = most_common_ingredients_class)
    ingredients_list = []
    for ingredient in ingredients_text:
        ingredient = str(ingredient)
        ingredient = re.sub('</', "", ingredient)
        ingredient = re.sub(rf'<{most_common_ingredients_tag}|{most_common_ingredients_tag}>', "", ingredient)
        ingredient = re.sub('<', "", ingredient)
        ingredient = re.sub(rf'{most_common_ingredients_class}', "", ingredient)
        ingredient = re.sub(' class=', "", ingredient)
        ingredient = re.sub('"', "", ingredient)
        ingredient = re.sub('Deselect All', "", ingredient)
        ingredient = re.sub('data.*?>', "", ingredient)
        ingredient = re.sub('span>|span', "", ingredient)
        ingredient = re.sub('p>', "", ingredient)
        ingredient = re.sub('>', "", ingredient)
        ingredient = re.sub('\xa0', " ", ingredient)
        ingredient = re.sub('\u202f', " ", ingredient)
        ingredient = re.sub("⁄", "/", unicodedata.normalize("NFKC", ingredient))
        ingredient = re.sub(' +', " ", ingredient)
        ingredient = re.sub('\n', "", ingredient)
        ingredient = ingredient.strip()
        if ingredient:
            ingredients_list.append(ingredient)
    # Extracting the HTML class and tag key words to search for directions
    most_common_directions_class, most_common_directions_tag = direction_class_tag(recipe_html)
    # Extracting directions and storing in list
    if "allrecipes" in URL:
        recipe_html = recipe_html.find("div", class_ = "comp recipe__steps-content mntl-sc-page mntl-block")
    directions_text = recipe_html.find_all(most_common_directions_tag, class_ = most_common_directions_class)
    directions_list = []
    for direction in directions_text:
        direction = str(direction)
        direction = re.sub('</', "", direction)
        direction = re.sub(rf'<{most_common_directions_tag}|{most_common_directions_tag}>', "", direction)
        direction = re.sub('<', "", direction)
        direction = re.sub(rf'{most_common_directions_class}', "", direction)
        direction = re.sub(' class=', "", direction)
        direction = re.sub('"', "", direction)
        direction = re.sub('id=.*>', "", direction)
        direction = re.sub('p>', "", direction)
        direction = re.sub('>', "", direction)
        direction = re.sub('\xa0', " ", direction)
        direction = re.sub('\u202f', " ", direction)
        direction = re.sub("⁄", "/", unicodedata.normalize("NFKC", direction))
        direction = re.sub(' +', " ", direction)
        direction = re.sub('\n', "", direction)
        if "https" not in direction:
            direction = direction.strip().split(".")
            if len(direction) > 1:
                for d in direction:
                    directions_list.append(d.strip())
    while("" in directions_list):
        directions_list.remove("")        
    return (ingredients_list, directions_list)