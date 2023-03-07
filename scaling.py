# Specifying the scaling factor, which will be user-provided
scaling_factor = float(input('Scaling factor: '))

# Defining function to convert recipe unit fractions to decimals
def fraction_to_decimal(recipe_unit):
    try:
        return float(recipe_unit)
    except ValueError:
        try:
            numerator, denominator = recipe_unit.split('/')
        except ValueError:
            return None
        try:
            whole_number, numerator = numerator.split(' ')
        except ValueError:
            return float(numerator) / float(denominator)
        return float(whole_number) + (float(numerator) / float(denominator))

# Defining function to scale the ingredients list
def ingredients_scale(ingredients, scaling_factor, units_list):
	ingredients_temp = [] # List of new scaled ingredients
	wording_sub_dict = {} # Dictionary of wording substitutions
	for ingredient in ingredients:
		# Finding all digits
		digits_list = re.findall('\d+', ingredient)
		if digits_list:
			first_digit = digits_list[0]
			last_digit = digits_list[-1]
			recipe_unit = re.search(rf'{first_digit}*.*{last_digit}', ingredient)
			recipe_unit = recipe_unit.group(0)
		else:
			recipe_unit = ""
		# Getting rid of stuff in parentheses
		recipe_unit = re.sub('\(.*', '', recipe_unit)
		recipe_unit = recipe_unit.strip()
		# Converting fractions to decimals
		recipe_unit_decimal = fraction_to_decimal(recipe_unit)
		# Scaling the ingredient units by the scaling factor
		if recipe_unit_decimal is not None:
			new_recipe_unit = recipe_unit_decimal*scaling_factor
		else:
			new_recipe_unit = ""
		# Subbing in the new scaled ingredient unit
		ingredient = re.sub(rf'{recipe_unit}', rf'{new_recipe_unit}', ingredient, count = 1)
		# Adjusting the wording (plurals) of the scaled ingredient if necessary
		inflection_engine = inflect.engine()
		recipe_amount = ""
		new_recipe_amount = ""
		recipe_ing_name = ""
		new_recipe_ing_name = ""
		for unit in units_list:
			if re.search(rf' {unit} | {inflection_engine.plural(unit)} ', ingredient):
				recipe_amount = re.search(rf' {unit} | {inflection_engine.plural(unit)} ', ingredient)
				recipe_amount = recipe_amount.group(0)
				recipe_amount = recipe_amount.strip()
		if new_recipe_unit and new_recipe_unit > 1:
			if recipe_amount:
				if inflection_engine.plural(recipe_amount) != inflection_engine.singular_noun(recipe_amount):
					new_recipe_amount = inflection_engine.plural(recipe_amount)
			else:
				for_regex = re.sub('\(.*\) ', '', ingredient)
				recipe_ing_name = re.search(rf'{new_recipe_unit} [a-zA-Z]*', for_regex)
				recipe_ing_name = recipe_ing_name.group(0)
				recipe_ing_name = re.sub(rf'{new_recipe_unit}', '', recipe_ing_name)
				recipe_ing_name = recipe_ing_name.strip()
				if inflection_engine.plural(recipe_ing_name) != inflection_engine.singular_noun(recipe_ing_name):
					new_recipe_ing_name = inflection_engine.plural(recipe_ing_name)
		elif new_recipe_unit and new_recipe_unit <= 1:
			if recipe_amount:
				if inflection_engine.plural(recipe_amount) == inflection_engine.singular_noun(recipe_amount):
					new_recipe_amount = inflection_engine.singular_noun(recipe_amount)
			else:
				for_regex = re.sub('\(.*\) ', '', ingredient)
				recipe_ing_name = re.search(rf'{new_recipe_unit} [a-zA-Z]*', for_regex)
				recipe_ing_name = recipe_ing_name.group(0)
				recipe_ing_name = re.sub(rf'{new_recipe_unit}', '', recipe_ing_name)
				recipe_ing_name = recipe_ing_name.strip()
				if inflection_engine.plural(recipe_ing_name) == inflection_engine.singular_noun(recipe_ing_name):
					new_recipe_ing_name = inflection_engine.singular_noun(recipe_ing_name)
		# Subbing in the new ingredient wording
		if new_recipe_amount:
			ingredient = re.sub(rf'{recipe_amount}', rf'{new_recipe_amount}', ingredient, count = 1)
			wording_sub_dict[recipe_amount] = new_recipe_amount
		if new_recipe_ing_name:
			ingredient = re.sub(rf'{recipe_ing_name}', rf'{new_recipe_ing_name}', ingredient, count = 1)
			wording_sub_dict[recipe_ing_name] = new_recipe_ing_name
		ingredients_temp.append(ingredient)
	# Returning the scaled ingredients list, as well as the dictionary of wording substitutions
	return (ingredients_temp, wording_sub_dict)

# Scaling the ingredients list, and getting dictionary of wording substitutions
ingredients, wording_sub_dict = ingredients_scale(ingredients, scaling_factor, units_list)


# Defining function to scale the directions steps
def directions_scale(direction_df, scaling_factor, wording_sub_dict):
	for ind in direction_df.index:
		new_recipe_unit_list = []
		for recipe_unit in direction_df['ingredient_amount'][ind]:
			# Converting fractions to decimals
			recipe_unit_decimal = fraction_to_decimal(recipe_unit)
			# Scaling the ingredient units by the scaling factor
			new_recipe_unit = recipe_unit_decimal*scaling_factor
			new_recipe_unit_list.append(new_recipe_unit)
		# Subbing in the new scaled ingredient unit
		direction_df['ingredient_amount'][ind] = new_recipe_unit_list.copy()
		# Changing the ingredient wording (plurals) if necessary
		old_wording_list = wording_sub_dict.keys()
		new_unit_list = []
		for unit in direction_df['ingredient_unit'][ind]:
			if unit in old_wording_list:
				new_unit_list.append(wording_sub_dict[unit])
			else:
				new_unit_list.append(unit)
		# Subbing in the new ingredient unit wording
		direction_df['ingredient_unit'][ind] = new_unit_list.copy()
		new_name_list = []
		for name in direction_df['ingredient_name'][ind]:
			new_name_split_list = []
			name_split_list = name.split(" ")
			for name_split in name_split_list:
				if name_split in old_wording_list:
					new_name_split_list.append(wording_sub_dict[name_split])
				else:
					new_name_split_list.append(name_split)
			new_name = " ".join(new_name_split_list)
			new_name_list.append(new_name)
		# Subbing in the new ingredient name wording
		direction_df['ingredient_name'][ind] = new_name_list.copy()
	# Returning the scaled directions steps
	return direction_df

# Scaling the directions steps
direction_df = directions_scale(direction_df, scaling_factor, wording_sub_dict)