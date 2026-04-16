from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'chef_table_secret_key_2024'

# Nutrition data per recipe (protein, carbs, fat, fiber in grams)
NUTRITION = {
    1: {'protein': 6, 'carbs': 12, 'fat': 8, 'fiber': 3},
    2: {'protein': 12, 'carbs': 35, 'fat': 10, 'fiber': 2},
    3: {'protein': 6, 'carbs': 52, 'fat': 22, 'fiber': 2},
    4: {'protein': 8, 'carbs': 38, 'fat': 5, 'fiber': 4},
    5: {'protein': 18, 'carbs': 14, 'fat': 24, 'fiber': 3},
    6: {'protein': 12, 'carbs': 40, 'fat': 10, 'fiber': 6},
    7: {'protein': 11, 'carbs': 28, 'fat': 3, 'fiber': 8},
    8: {'protein': 15, 'carbs': 42, 'fat': 14, 'fiber': 5},
}

# In-memory ratings store: {recipe_id: [list of ratings]}
RATINGS = {r['id']: [] for r in []}

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ratings store initialized after RECIPES
# Recipe data with calories and ingredients
RECIPES = [
    {
        'id': 1, 
        'name': 'Caesar Salad', 
        'category': 'Salad', 
        'emoji': '🥗', 
        'description': 'Crisp romaine lettuce with caesar dressing, croutons and parmesan.',
        'cuisine': 'Italian', 
        'rating': 4.5,
        'calories': 150,
        'ingredients': ['Romaine Lettuce', 'Caesar Dressing', 'Croutons', 'Parmesan Cheese', 'Lemon Juice'],
        'keywords': ['salad', 'caesar', 'lettuce', 'veg']
    },
    {
        'id': 2, 
        'name': 'Margherita Pizza', 
        'category': 'Italian', 
        'emoji': '🍕', 
        'description': 'Classic wood-fired pizza with tomato sauce, fresh mozzarella and basil.',
        'cuisine': 'Italian', 
        'rating': 4.6,
        'calories': 285,
        'ingredients': ['Pizza Dough', 'Tomato Sauce', 'Fresh Mozzarella', 'Basil', 'Olive Oil'],
        'keywords': ['pizza', 'margherita', 'italian', 'mozzarella']
    },
    {
        'id': 3, 
        'name': 'Chocolate Lava Cake', 
        'category': 'Dessert', 
        'emoji': '🍫', 
        'description': 'Warm chocolate cake with a gooey molten center, served with ice cream.',
        'cuisine': 'French', 
        'rating': 4.9,
        'calories': 420,
        'ingredients': ['Dark Chocolate', 'Butter', 'Eggs', 'Sugar', 'Flour', 'Vanilla Extract'],
        'keywords': ['cake', 'chocolate', 'dessert', 'lava']
    },
    {
        'id': 4, 
        'name': 'Veg Noodles', 
        'category': 'Asian', 
        'emoji': '🍜', 
        'description': 'Stir-fried noodles with fresh vegetables, soy sauce and sesame oil.',
        'cuisine': 'Asian', 
        'rating': 4.4,
        'calories': 220,
        'ingredients': ['Noodles', 'Broccoli', 'Carrots', 'Bell Peppers', 'Soy Sauce', 'Sesame Oil'],
        'keywords': ['noodles', 'asian', 'veg', 'stir-fry']
    },
    {
        'id': 5, 
        'name': 'Paneer Butter Masala', 
        'category': 'Indian', 
        'emoji': '🥘', 
        'description': 'Soft paneer cubes in a rich, creamy tomato-based butter sauce.',
        'cuisine': 'Indian', 
        'rating': 4.7,
        'calories': 380,
        'ingredients': ['Paneer', 'Tomato Sauce', 'Butter', 'Cream', 'Onions', 'Spices', 'Ginger-Garlic'],
        'keywords': ['paneer', 'indian', 'butter', 'masala', 'curry']
    },
    {
        'id': 6, 
        'name': 'Falafel Wrap', 
        'category': 'Middle Eastern', 
        'emoji': '🧆', 
        'description': 'Crispy falafel with hummus, fresh veggies and tahini in a warm wrap.',
        'cuisine': 'Middle Eastern', 
        'rating': 4.5,
        'calories': 310,
        'ingredients': ['Chickpeas', 'Tahini', 'Hummus', 'Lettuce', 'Tomato', 'Wrap Bread', 'Spices'],
        'keywords': ['falafel', 'wrap', 'middle eastern', 'veg']
    },
    {
        'id': 7, 
        'name': 'Dal Tadka', 
        'category': 'Indian', 
        'emoji': '🍲', 
        'description': 'Yellow lentils tempered with cumin, garlic and aromatic Indian spices.',
        'cuisine': 'Indian', 
        'rating': 4.6,
        'calories': 180,
        'ingredients': ['Yellow Lentils', 'Cumin', 'Garlic', 'Ginger', 'Onions', 'Tomato', 'spices'],
        'keywords': ['dal', 'lentils', 'indian', 'soup']
    },
    {
        'id': 8, 
        'name': 'Veggie Burger', 
        'category': 'American', 
        'emoji': '🥙', 
        'description': 'Juicy plant-based patty with lettuce, tomato, cheese and special sauce.',
        'cuisine': 'American', 
        'rating': 4.3,
        'calories': 350,
        'ingredients': ['Plant-based Patty', 'Burger Bun', 'Lettuce', 'Tomato', 'Cheese', 'Special Sauce', 'Onion'],
        'keywords': ['burger', 'veg', 'plant-based', 'american']
    },
]

# Initialize ratings store
RATINGS = {r['id']: [] for r in RECIPES}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_recipe_by_image(filename):
    """Simple recipe matching based on filename/upload"""
    filename_lower = filename.lower()
    for recipe in RECIPES:
        for keyword in recipe['keywords']:
            if keyword.lower() in filename_lower:
                return recipe
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', recipes=RECIPES)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/veg')
def veg():
    return render_template('veg.html', recipes=RECIPES)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    results = []
    if query:
        # Save to search history
        history = session.get('search_history', [])
        if query not in history:
            history.insert(0, query)
        session['search_history'] = history[:20]
        results = [recipe for recipe in RECIPES if
                   query in recipe['name'].lower() or
                   query in recipe['description'].lower() or
                   query in recipe['category'].lower() or
                   query in recipe['cuisine'].lower()]
    return render_template('search_results.html', query=query, results=results)

@app.route('/profile')
def profile():
    history = session.get('search_history', [])
    return render_template('profile.html', history=history)

@app.route('/profile/update', methods=['POST'])
def profile_update():
    session['profile_name'] = request.form.get('name', 'Chef')
    session['profile_email'] = request.form.get('email', '')
    session['profile_bio'] = request.form.get('bio', '')
    return redirect(url_for('profile'))

@app.route('/profile/settings', methods=['POST'])
def profile_settings():
    session['setting_notifications'] = 'notifications' in request.form
    session['setting_calorie_goal'] = request.form.get('calorie_goal', '1500')
    session['setting_cuisine'] = request.form.get('cuisine', 'All')
    return redirect(url_for('profile'))

@app.route('/profile/clear-history', methods=['POST'])
def clear_history():
    session['search_history'] = []
    return redirect(url_for('profile'))

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        # Handle file upload
        if 'image' not in request.files:
            return render_template('detect.html', error='No image provided')
        
        file = request.files['image']
        if file.filename == '':
            return render_template('detect.html', error='No file selected')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Find matching recipe
            recipe = find_recipe_by_image(filename)
            
            if recipe:
                return render_template('detect.html', recipe=recipe, detected=True, image_path=filepath)
            else:
                return render_template('detect.html', error='Recipe not identified. Try a different image.')
        else:
            return render_template('detect.html', error='Invalid file format. Please use PNG, JPG, JPEG, or GIF.')
    
    return render_template('detect.html')

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = next((r for r in RECIPES if r['id'] == recipe_id), None)
    if recipe:
        nutrition = NUTRITION.get(recipe_id, {})
        reviews = RATINGS.get(recipe_id, [])
        avg_rating = round(sum(r['stars'] for r in reviews) / len(reviews), 1) if reviews else recipe['rating']
        return render_template('recipe_detail.html', recipe=recipe, nutrition=nutrition, reviews=reviews, avg_rating=avg_rating)
    return redirect(url_for('veg'))

# --- Feature 1: Meal Planner ---
@app.route('/meal-planner')
def meal_planner():
    plan = session.get('meal_plan', {day: [] for day in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']})
    return render_template('meal_planner.html', recipes=RECIPES, plan=plan)

@app.route('/meal-planner/add', methods=['POST'])
def add_to_plan():
    day = request.form.get('day')
    recipe_id = int(request.form.get('recipe_id'))
    plan = session.get('meal_plan', {d: [] for d in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']})
    recipe = next((r for r in RECIPES if r['id'] == recipe_id), None)
    if recipe and day in plan:
        # avoid duplicates
        if recipe_id not in [r['id'] for r in plan[day]]:
            plan[day].append({'id': recipe['id'], 'name': recipe['name'], 'emoji': recipe['emoji'], 'calories': recipe['calories']})
    session['meal_plan'] = plan
    return redirect(url_for('meal_planner'))

@app.route('/meal-planner/remove', methods=['POST'])
def remove_from_plan():
    day = request.form.get('day')
    recipe_id = int(request.form.get('recipe_id'))
    plan = session.get('meal_plan', {})
    if day in plan:
        plan[day] = [r for r in plan[day] if r['id'] != recipe_id]
    session['meal_plan'] = plan
    return redirect(url_for('meal_planner'))

@app.route('/meal-planner/clear', methods=['POST'])
def clear_plan():
    session['meal_plan'] = {d: [] for d in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']}
    return redirect(url_for('meal_planner'))

# --- Feature 3: Ingredient Finder ---
@app.route('/ingredient-finder', methods=['GET', 'POST'])
def ingredient_finder():
    results = []
    user_ingredients = request.form.get('ingredients', '') or request.args.get('ingredients', '')
    if user_ingredients:
        user_list = [i.strip().lower() for i in user_ingredients.split(',') if i.strip()]
        for recipe in RECIPES:
            ing_status = []
            match_count = 0
            for ing in recipe['ingredients']:
                ing_lower = ing.lower()
                # match if any user word appears anywhere in ingredient or vice versa
                is_match = any(
                    u in ing_lower or ing_lower in u or
                    any(word in ing_lower for word in u.split())
                    for u in user_list
                )
                ing_status.append({'name': ing, 'matched': is_match})
                if is_match:
                    match_count += 1
            if match_count > 0:
                results.append({
                    'recipe': recipe,
                    'match_count': match_count,
                    'total': len(recipe['ingredients']),
                    'ing_status': ing_status
                })
        results.sort(key=lambda x: x['match_count'], reverse=True)
    return render_template('ingredient_finder.html', results=results, user_ingredients=user_ingredients)

# --- Feature 4: Ratings & Reviews ---
@app.route('/recipe/<int:recipe_id>/rate', methods=['POST'])
def rate_recipe(recipe_id):
    stars = int(request.form.get('stars', 0))
    comment = request.form.get('comment', '').strip()
    if 1 <= stars <= 5 and recipe_id in RATINGS:
        RATINGS[recipe_id].append({'stars': stars, 'comment': comment, 'date': datetime.now().strftime('%b %d, %Y')})
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

if __name__ == '__main__':
    app.run(debug=True)
