"""
utils.py — Shared utility functions for FoodScan AI PRO.
"""

HARMFUL_KEYWORDS = [
    "palm oil","hydrogenated","partially hydrogenated",
    "high fructose corn syrup","hfcs","monosodium glutamate","msg",
    "sodium nitrate","sodium nitrite","bha","bht","tbhq",
    "artificial color","artificial flavour","artificial flavor",
    "red 40","yellow 5","yellow 6","blue 1","blue 2",
    "potassium bromate","acesulfame","saccharin","aspartame",
    "carrageenan","propyl gallate","sodium benzoate","potassium sorbate","trans fat",
]

SAFE_POSITIVE_KEYWORDS = [
    "whole grain","oats","quinoa","brown rice","flaxseed",
    "almonds","walnuts","olive oil","sunflower oil",
    "spinach","kale","broccoli","carrot",
    "blueberry","strawberry","apple",
    "lentils","chickpeas","black beans","greek yogurt","skim milk",
]

FOOD_NUTRITION_DB = {
    "pizza":           {"calories":266,"fat":10,"sugar":3.6,"protein":11,"sodium":598,"carbohydrates":33},
    "burger":          {"calories":295,"fat":14,"sugar":7,  "protein":17,"sodium":396,"carbohydrates":24},
    "hamburger":       {"calories":295,"fat":14,"sugar":7,  "protein":17,"sodium":396,"carbohydrates":24},
    "cheeseburger":    {"calories":303,"fat":13,"sugar":6.5,"protein":15,"sodium":690,"carbohydrates":26},
    "hot dog":         {"calories":242,"fat":14,"sugar":4,  "protein":10,"sodium":670,"carbohydrates":18},
    "salad":           {"calories":15, "fat":0.2,"sugar":1.5,"protein":1.3,"sodium":10,"carbohydrates":2.9},
    "caesar salad":    {"calories":90, "fat":7,  "sugar":1.5,"protein":4, "sodium":280,"carbohydrates":5},
    "french fries":    {"calories":312,"fat":15,"sugar":0.3,"protein":3.4,"sodium":210,"carbohydrates":41},
    "pasta":           {"calories":131,"fat":1.1,"sugar":0.6,"protein":5, "sodium":1,  "carbohydrates":25},
    "spaghetti":       {"calories":131,"fat":1.1,"sugar":0.6,"protein":5, "sodium":1,  "carbohydrates":25},
    "sushi":           {"calories":143,"fat":3.6,"sugar":5,  "protein":9, "sodium":428,"carbohydrates":21},
    "steak":           {"calories":271,"fat":19, "sugar":0,  "protein":26,"sodium":55, "carbohydrates":0},
    "grilled chicken": {"calories":165,"fat":3.6,"sugar":0,  "protein":31,"sodium":74, "carbohydrates":0},
    "fried chicken":   {"calories":320,"fat":21, "sugar":0.5,"protein":28,"sodium":560,"carbohydrates":12},
    "grilled salmon":  {"calories":208,"fat":13, "sugar":0,  "protein":20,"sodium":59, "carbohydrates":0},
    "cake":            {"calories":347,"fat":15, "sugar":39, "protein":4, "sodium":299,"carbohydrates":50},
    "birthday cake":   {"calories":347,"fat":15, "sugar":39, "protein":4, "sodium":299,"carbohydrates":50},
    "chocolate cake":  {"calories":371,"fat":17, "sugar":40, "protein":5, "sodium":282,"carbohydrates":50},
    "ice cream":       {"calories":207,"fat":11, "sugar":21, "protein":3.5,"sodium":80,"carbohydrates":24},
    "waffle":          {"calories":291,"fat":14, "sugar":5,  "protein":8, "sodium":617,"carbohydrates":33},
    "pancake":         {"calories":227,"fat":10, "sugar":6,  "protein":6, "sodium":416,"carbohydrates":28},
    "croissant":       {"calories":406,"fat":21, "sugar":11, "protein":8, "sodium":375,"carbohydrates":45},
    "bagel":           {"calories":245,"fat":1.5,"sugar":5,  "protein":10,"sodium":443,"carbohydrates":48},
    "sandwich":        {"calories":200,"fat":6,  "sugar":3,  "protein":12,"sodium":380,"carbohydrates":28},
    "soup":            {"calories":50, "fat":1.5,"sugar":3,  "protein":3, "sodium":430,"carbohydrates":8},
    "tomato soup":     {"calories":53, "fat":1.7,"sugar":5,  "protein":2, "sodium":448,"carbohydrates":9},
    "burrito":         {"calories":206,"fat":8,  "sugar":1.5,"protein":9, "sodium":478,"carbohydrates":26},
    "taco":            {"calories":216,"fat":10, "sugar":2,  "protein":10,"sodium":405,"carbohydrates":21},
    "apple pie":       {"calories":237,"fat":11, "sugar":13, "protein":2, "sodium":169,"carbohydrates":34},
    "pretzel":         {"calories":380,"fat":3,  "sugar":1.5,"protein":10,"sodium":1614,"carbohydrates":78},
    "mashed potato":   {"calories":113,"fat":4.2,"sugar":1.2,"protein":2, "sodium":370,"carbohydrates":17},
    "fried rice":      {"calories":163,"fat":2.7,"sugar":0.8,"protein":3.5,"sodium":298,"carbohydrates":29},
    "banana":          {"calories":89, "fat":0.3,"sugar":12, "protein":1.1,"sodium":1,  "carbohydrates":23},
    "broccoli":        {"calories":34, "fat":0.4,"sugar":1.7,"protein":2.8,"sodium":33, "carbohydrates":7},
    "smoothie":        {"calories":80, "fat":0.5,"sugar":14, "protein":2,  "sodium":30, "carbohydrates":18},
    "coffee":          {"calories":2,  "fat":0,  "sugar":0,  "protein":0.3,"sodium":4,  "carbohydrates":0},
    "omelette":        {"calories":154,"fat":11, "sugar":1,  "protein":11, "sodium":342,"carbohydrates":1.6},
    "fruit bowl":      {"calories":65, "fat":0.3,"sugar":13, "protein":1.2,"sodium":3,  "carbohydrates":16},
}

# Default ingredients for common foods (shown when API returns no ingredient list)
DEFAULT_INGREDIENTS = {
    "pizza": "Wheat flour, tomato sauce, mozzarella cheese, olive oil, yeast, salt, basil, oregano",
    "burger": "Beef patty, lettuce, tomato, onion, pickles, burger bun, ketchup, mustard, mayonnaise",
    "hamburger": "Beef patty, lettuce, tomato, onion, pickles, burger bun, ketchup, mustard",
    "cheeseburger": "Beef patty, cheddar cheese, lettuce, tomato, onion, pickles, burger bun, ketchup",
    "hot dog": "Pork & beef sausage, bun, mustard, ketchup, onion, relish",
    "french fries": "Potatoes, vegetable oil (sunflower), salt",
    "salad": "Mixed greens, tomato, cucumber, carrot, olive oil, lemon juice, salt, pepper",
    "caesar salad": "Romaine lettuce, croutons, parmesan cheese, caesar dressing (egg yolk, anchovies, garlic, lemon)",
    "pasta": "Durum wheat semolina, water, eggs. Sauce: tomatoes, olive oil, garlic, basil",
    "spaghetti": "Durum wheat semolina, water, eggs, tomato sauce, garlic, olive oil, parmesan",
    "sushi": "Short-grain rice, rice vinegar, nori, raw salmon/tuna/shrimp, soy sauce, wasabi, ginger",
    "steak": "Beef (sirloin/ribeye), salt, black pepper, garlic, butter, rosemary",
    "grilled chicken": "Chicken breast, olive oil, garlic, lemon, rosemary, thyme, salt, pepper",
    "fried chicken": "Chicken, flour, breadcrumbs, eggs, buttermilk, salt, paprika, garlic powder, vegetable oil",
    "grilled salmon": "Atlantic salmon, lemon, dill, olive oil, garlic, salt, black pepper",
    "cake": "All-purpose flour, sugar, butter, eggs, milk, baking powder, vanilla extract",
    "ice cream": "Cream, skim milk, sugar, egg yolks, vanilla extract, stabilizers",
    "waffle": "All-purpose flour, milk, eggs, butter, sugar, baking powder, vanilla extract",
    "pancake": "All-purpose flour, milk, egg, butter, sugar, baking powder, salt",
    "croissant": "Wheat flour, butter, milk, yeast, sugar, salt, eggs",
    "sandwich": "Bread, lettuce, tomato, cheese, ham or turkey, mustard, mayonnaise",
    "soup": "Water, vegetables (carrot, celery, onion), broth, salt, pepper, herbs",
    "burrito": "Flour tortilla, rice, black beans, grilled chicken, salsa, sour cream, cheese, guacamole",
    "taco": "Corn tortilla, seasoned beef or chicken, lettuce, tomato, cheese, salsa, sour cream",
    "omelette": "Eggs, milk, butter, salt, pepper. Optional: cheese, mushrooms, bell pepper, onion",
    "banana": "100% banana (natural fruit)",
    "broccoli": "100% broccoli florets (fresh or steamed)",
    "smoothie": "Banana, mixed berries, spinach, almond milk, honey, chia seeds",
    "coffee": "Coffee beans (arabica/robusta), water",
    "fruit bowl": "Strawberries, blueberries, banana, kiwi, orange segments, grapes",
    "fried rice": "Cooked rice, eggs, soy sauce, sesame oil, garlic, ginger, spring onion, peas, carrot",
}

# ── Local fallback product DB ────────────────────────────────────────────────────
LOCAL_PRODUCT_DB = {
    "maggi":      {"calories":357,"fat":14,"sugar":1,   "protein":9, "sodium":980,"carbohydrates":48,
                   "ingredients":"Wheat flour, palm oil, salt, monosodium glutamate, artificial flavors, preservatives, soy sauce powder"},
    "oreo":       {"calories":471,"fat":20,"sugar":40,  "protein":5, "sodium":480,"carbohydrates":71,
                   "ingredients":"Sugar, palm oil, enriched flour (wheat), cocoa powder, high fructose corn syrup, artificial colors, soy lecithin"},
    "lays":       {"calories":536,"fat":34,"sugar":1,   "protein":6, "sodium":490,"carbohydrates":53,
                   "ingredients":"Potatoes, vegetable oil (sunflower), salt, artificial flavors"},
    "lay's":      {"calories":536,"fat":34,"sugar":1,   "protein":6, "sodium":490,"carbohydrates":53,
                   "ingredients":"Potatoes, vegetable oil (sunflower), salt, artificial flavors"},
    "coca cola":  {"calories":42, "fat":0, "sugar":10.6,"protein":0, "sodium":10, "carbohydrates":10.6,
                   "ingredients":"Carbonated water, high fructose corn syrup, caramel color, phosphoric acid, natural flavors, caffeine"},
    "coke":       {"calories":42, "fat":0, "sugar":10.6,"protein":0, "sodium":10, "carbohydrates":10.6,
                   "ingredients":"Carbonated water, high fructose corn syrup, caramel color, phosphoric acid, natural flavors, caffeine"},
    "pepsi":      {"calories":41, "fat":0, "sugar":11,  "protein":0, "sodium":11, "carbohydrates":11,
                   "ingredients":"Carbonated water, high fructose corn syrup, caramel color, phosphoric acid, natural flavors, caffeine"},
    "kitkat":     {"calories":518,"fat":27,"sugar":48,  "protein":6, "sodium":100,"carbohydrates":62,
                   "ingredients":"Sugar, wheat flour, cocoa butter, skimmed milk powder, cocoa mass, vegetable fat, palm oil, artificial flavors"},
    "cadbury":    {"calories":535,"fat":30,"sugar":56,  "protein":7, "sodium":83, "carbohydrates":59,
                   "ingredients":"Sugar, cocoa butter, cocoa mass, skimmed milk powder, anhydrous milk fat, vegetable fat (palm), emulsifiers (soy lecithin)"},
    "pringles":   {"calories":536,"fat":34,"sugar":2,   "protein":4, "sodium":487,"carbohydrates":57,
                   "ingredients":"Dried potatoes, vegetable oil (sunflower, corn), rice flour, wheat starch, maltodextrin, salt, artificial flavors"},
    "kurkure":    {"calories":507,"fat":24,"sugar":3,   "protein":7, "sodium":895,"carbohydrates":63,
                   "ingredients":"Corn meal, edible vegetable oil, rice meal, gram meal, seasoning (salt, spices, monosodium glutamate, artificial colors)"},
    "bournvita":  {"calories":389,"fat":4, "sugar":67,  "protein":7, "sodium":127,"carbohydrates":85,
                   "ingredients":"Sugar, cocoa powder, wheat flour, malt extract, milk solids, vitamins & minerals, artificial flavors"},
    "parle g":    {"calories":462,"fat":13,"sugar":16,  "protein":7, "sodium":250,"carbohydrates":75,
                   "ingredients":"Wheat flour, sugar, partially hydrogenated edible vegetable oil, invert syrup, milk solids, salt, leavening agents"},
    "hide & seek":{"calories":485,"fat":21,"sugar":28,  "protein":6, "sodium":320,"carbohydrates":68,
                   "ingredients":"Refined wheat flour, sugar, vegetable fat, cocoa solids, butter, salt, baking powder, artificial vanilla flavor"},
    "britannia":  {"calories":462,"fat":15,"sugar":18,  "protein":8, "sodium":280,"carbohydrates":72,
                   "ingredients":"Wheat flour, sugar, vegetable oil, milk solids, salt, baking soda, artificial flavor"},
    "mcdonald":   {"calories":295,"fat":14,"sugar":7,   "protein":17,"sodium":396,"carbohydrates":24,
                   "ingredients":"Beef patty, lettuce, tomato, onion, pickles, burger bun, ketchup, mustard, mayonnaise"},
    "dominos":    {"calories":266,"fat":10,"sugar":3.6, "protein":11,"sodium":598,"carbohydrates":33,
                   "ingredients":"Wheat flour, tomato sauce, mozzarella cheese, olive oil, yeast, salt, herbs"},
    "subway":     {"calories":200,"fat":6, "sugar":3,   "protein":12,"sodium":380,"carbohydrates":28,
                   "ingredients":"Bread (wheat flour, yeast), lettuce, tomato, cucumber, cheese, turkey, olive oil, vinegar"},
    "nutella":    {"calories":530,"fat":31,"sugar":57,  "protein":6, "sodium":41, "carbohydrates":58,
                   "ingredients":"Sugar, palm oil, hazelnuts (13%), skimmed milk powder, cocoa solids (7.4%), lecithin, vanillin"},
    "amul butter":{"calories":720,"fat":80,"sugar":0.5, "protein":0.8,"sodium":630,"carbohydrates":0.8,
                   "ingredients":"Pasteurized cream (from cow's milk), common salt, permitted natural color (annatto)"},
    "dettol":     {"calories":0,  "fat":0, "sugar":0,   "protein":0, "sodium":0,  "carbohydrates":0,
                   "ingredients":"Not a food product"},
}

DEFAULT_NUTRITION = {"calories":200,"fat":8,"sugar":6,"protein":7,"sodium":300,"carbohydrates":25}


def get_estimated_nutrition(food_name: str) -> dict:
    key = food_name.lower().strip()
    if key in FOOD_NUTRITION_DB:
        return dict(FOOD_NUTRITION_DB[key])
    for db_key, vals in FOOD_NUTRITION_DB.items():
        if db_key in key or key in db_key:
            return dict(vals)
    return dict(DEFAULT_NUTRITION)


def get_default_ingredients(food_name: str) -> str:
    """Return a realistic ingredient list for common foods."""
    key = food_name.lower().strip()
    if key in DEFAULT_INGREDIENTS:
        return DEFAULT_INGREDIENTS[key]
    for k, v in DEFAULT_INGREDIENTS.items():
        if k in key or key in k:
            return v
    return ""


def get_local_product_fallback(name: str) -> dict | None:
    """Check local product DB for common packaged foods."""
    key = name.lower().strip()
    if key in LOCAL_PRODUCT_DB:
        return dict(LOCAL_PRODUCT_DB[key])
    for db_key, vals in LOCAL_PRODUCT_DB.items():
        if db_key in key or key in db_key:
            return dict(vals)
    return None


def analyze_ingredients(ingredients: str) -> tuple[list[str], list[str]]:
    if not ingredients:
        return [], []
    lower = ingredients.lower()
    harmful = [kw.title() for kw in HARMFUL_KEYWORDS if kw in lower]
    safe = [kw.title() for kw in SAFE_POSITIVE_KEYWORDS if kw in lower]
    return harmful, safe
