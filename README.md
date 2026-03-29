# 🍽️ Chef's Table

A smart recipe web app built with Flask — search recipes, plan your meals, track calories, find recipes by ingredients, and rate dishes.

## 🚀 Live Demo
> Run locally: `python app.py` → open `http://127.0.0.1:5000`

---

## ✨ Features

| Feature | Description |
|---|---|
| 📅 Weekly Meal Planner | Plan meals for Mon–Sun with drag and add |
| 🔥 Calorie Budget Tracker | Set daily calorie goal, track progress with bar |
| 🥦 Ingredient Finder | Enter what's in your fridge, get matching recipes |
| ⭐ Ratings & Reviews | Rate recipes 1–5 stars and leave comments |
| 🏷️ Nutrition Label | FDA-style nutrition facts per recipe |
| 🔍 Live Search | Search recipes instantly with ingredients shown |
| 🌐 Google Web Search | Google CSE integrated for web recipe results |
| 📷 Image Detection | Upload food image to identify recipe |
| 🍛 Cuisine Filters | Filter by Indian, Italian, Asian, American and more |

---

## 🛠️ Tech Stack

- **Backend** — Python, Flask
- **Frontend** — HTML, CSS, Vanilla JavaScript
- **Search** — Google Custom Search Engine
- **Storage** — Flask Session

---

## ⚙️ Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open → `http://127.0.0.1:5000`

---

## 📁 Project Structure

```
hackathon1/
├── app.py                  # Flask app + all routes
├── requirements.txt        # Dependencies
├── templates/
│   ├── index.html          # Landing page
│   ├── dashboard.html      # Home with live search + filters
│   ├── veg.html            # All recipes
│   ├── recipe_detail.html  # Recipe + nutrition + reviews
│   ├── meal_planner.html   # Weekly meal planner
│   ├── ingredient_finder.html  # Fridge finder
│   ├── search_results.html # Search + Google CSE results
│   ├── detect.html         # Image detection
│   ├── login.html
│   └── register.html
└── uploads/                # Uploaded images
```

---

## 📸 Pages

- `/` — Landing page
- `/dashboard` — Home with search and cuisine filters
- `/veg` — All vegetarian recipes
- `/recipe/<id>` — Recipe detail with nutrition label and reviews
- `/meal-planner` — Weekly meal planner with calorie tracker
- `/ingredient-finder` — Find recipes by ingredients you have
- `/search?q=` — Search results with Google web results
- `/detect` — Upload image to detect recipe

---

## 👨‍💻 Built By

**Rahulm09-coder** — Hackathon 2025
