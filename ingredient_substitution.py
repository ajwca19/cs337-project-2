# Generating a dictionary of common ingredient substitutions
substitution_dictionary = {
	'bread crumbs': ['cracker crumbs', 'matzo meal', 'ground oats', 'rice'],
	'butter': ['margarine'],
	'buttermilk': ['yogurt'],
	'cornstarch': ['flour'],
	'corn syrup': ['honey'],
	'cottage cheese': ["farmer's cheese", 'ricotta cheese'],
	'cracker crumbs': ['bread crumbs', 'matzo meal', 'ground oats'],
	'light cream': ['evaporated milk'],
	'cream of tartar': ['lemon juice', 'vinegar'],
	'egg': ['pureed tofu', 'mayonnaise', 'powdered flax seed'],
	'evaporated milk': ['light cream'],
	"farmer's cheese": ['cottage cheese'],
	'bread flour': ['all-purpose flour'],
	'cake flour': ['all-purpose flour'],
	'garlic': ['garlic powder'],
	'green onion': ['onion', 'leek', 'shallots'],
	'hazelnuts': ['macadamia nuts', 'almonds'],
	'herring': ['sardines'],
	'honey': ['corn syrup'],
	'lard': ['shortening', 'vegetable oil', 'butter'],
	'lemon': ['lime', 'vinegar'],
	'lemongrass': ['lemon zest'],
	'lemon juice': ['vinegar', 'white wine', 'lime juice'],
	'lemon zest': ['lemon extract', 'lemon juice'],
	'lime': ['lemon', 'vinegar'],
	'lime juice': ['vinegar', 'white wine', 'lemon juice'],
	'lime zest': ['lemon zest'],
	'macadamia nuts': ['hazelnuts', 'almonds'],
	'mace': ['nutmeg'],
	'margarine': ['butter'],
	'mayonnaise': ['sour cream', 'plain yogurt'],
	'whole milk': ['soy milk', 'water'],
	'onion': ['green onion', 'shallots', 'leek', 'onion powder'],
	'orange juice': ['lemon juice', 'lime juice'],
	'orange zest': ['orange extract', 'lemon juice'],
	'pepperoni': ['salami'],
	'raisin': ['dried currants', 'dried cranberries', 'pitted prunes'],
	'rice': ['barley', 'bulgur'],
	'ricotta': ['cottage cheese', 'tofu'],
	'saffron': ['turmeric'],
	'salami': ['pepperoni'],
	'chocolate chips': ['nuts', 'dried fruit'],
	'shallots': ['onion', 'leek', 'green onion'],
	'shortening:': ['butter'],
	'sour cream': ['plain yogurt'],
	'soy sauce': ['Worcestershire sauce'],
	'vegetable oil': ['lard', 'olive oil'],
	'vinegar': ['lemon juice', 'lime juice', 'white wine'],
	'sugar': ['honey', 'corn syrup'],
	'wine': ['chicken broth', 'beef broth', 'water', 'fruit juice'],
	'yogurt': ['sour cream', 'buttermilk', 'sour milk'],
	'beef': ['turkey', 'beans', 'chickpeas', 'lentils', 'jackfruit', 'mushrooms'],
	'chicken': ['tofu', 'chickpeas', 'jackfruit', 'tempeh', 'soy', 'cauliflower'],
	'pork': ['turkey', 'beef', 'chicken', 'tofu'],
	'fish': ['tofu', 'jackfruit'],
	'parsley': ['mint', 'cilantro', 'basil', 'sorrel'],
	'mint': ['parsley', 'cilantro', 'basil', 'sorrel'],
	'cilantro': ['mint', 'parsley', 'basil', 'sorrel'],
	'basil': ['mint', 'parsley', 'cilantro', 'sorrel'],
	'sorrel': ['mint', 'parsley', 'cilantro', 'basil'],
	'thyme': ['rosemary', 'sage', 'oregano'],
	'rosemary': ['thyme', 'sage', 'oregano'],
	'sage': ['thyme', 'rosemary', 'oregano'],
	'oregano': ['thyme', 'rosemary', 'sage'],
	'spinach': ['chard', 'collard greens', 'kale'],
	'chard': ['spinach', 'collard greens', 'kale'],
	'collard greens': ['spinach', 'chard', 'kale'],
	'kale': ['spinach', 'chard', 'collard greens'],
	'potato': ['parsnip', 'beets', 'turnip', 'rutabaga', 'carrots'],
	'parsnip': ['potato', 'beets', 'turnip', 'rutabaga', 'carrots'],
	'beets': ['potato', 'parsnip', 'turnip', 'rutabaga', 'carrots'],
	'turnip': ['potato', 'parsnip', 'beets', 'rutabaga', 'carrots'],
	'rutabaga': ['potato', 'parsnip', 'beets', 'turnip', 'carrots'],
	'carrots': ['potato', 'parsnip', 'beets', 'turnip', 'rutabaga'],
	'broccoli': ['broccolini', 'cabbage', 'brussels sprouts'],
	'broccolini': ['broccoli', 'cabbage', 'brussels sprouts'],
	'cabbage': ['broccoli', 'broccolini', 'brussels sprouts'],
	'brussels sprouts': ['broccoli', 'broccolini', 'cabbage'],
	'celery': ['snow peas', 'radish'],
	'snow peas': ['celery', 'radish'],
	'radish': ['celery', 'snow peas'],
	'zucchini': ['peas', 'green beans', 'asparagus'],
	'peas': ['zucchini', 'green beans', 'asparagus'],
	'green beans': ['zucchini', 'peas', 'asparagus'],
	'asparagus': ['zucchini', 'peas', 'green beans'],
	'tomato': ['bell pepper', 'eggplant'],
	'bell pepper': ['tomato', 'eggplant'],
	'eggplant': ['tomato', 'bell pepper'],
	'lettuce': ['radicchio', 'arugula'],
	'radicchio': ['lettuce', 'arugula'],
	'arugula': ['lettuce', 'radicchio']
}

# Generating a dictionary of foods you cannot eat on common diets
diet_dictionary = {
	'vegetarian': ['beef', 'turkey', 'chicken', 'pork', 'fish'],
	'vegan': ['beef', 'turkey', 'chicken', 'pork', 'fish', 'milk', 'cream', 'cheese', 'egg', 'honey'],
	'keto': ['rice', 'corn', 'oatmeal', 'beans', 'lentils', 'yogurt', 'juice', 'honey', 'syrup', 'sugar', 'chips', 'crackers'],
	'low carb': ['bread', 'pasta', 'potato', 'rice', 'corn', 'oatmeal', 'beans', 'lentils', 'milk', 'sugar'],
	'kosher': ['pork', 'shrimp', 'crayfish', 'crab', 'lobster', 'clams', 'scallops', 'oysters', 'mussels'],
	'halal': ['alcohol', 'vanilla extract', 'pork'],
	'hindu': ['beef']
}

# Generating a dictionary of foods common to different cuisine types
cuisine_dictionary = {
	'italian': {'proteins': ['beef', 'pork', 'chicken', 'fish'], 'vegetables': ['eggplant', 'celery', 'broccoli rabe', 'broccolini', 'arugula', 'artichokes', 'fennel', 'mushrooms', 'tomato', 'onion'], 'spices': ['thyme', 'basil', 'oregano', 'sage', 'rosemary', 'garlic'], 'binders': ['bread crumbs', 'egg']},
	'south asian': {'proteins': ['chicken', 'turkey', 'lamb', 'lentils', 'chickpeas'], 'vegetables': ['cauliflower', 'potato', 'jackfruit', 'cabbage', 'chili pepper', 'eggplant', 'onion', 'sweet potato', 'turnip'], 'spices': ['turmeric', 'cardamom', 'chili', 'ginger', 'garlic', 'cumin', 'coriander', 'cloves', 'red chili powder', 'mustard seed', 'fenugreek', 'saffron'], 'binders': ['rice', 'psyllium husks']}
}