# 🍽️ Chef's Table REST API

A Flask-based REST API for recipe management with image detection capabilities.

## Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the API Server
```bash
python app.py
```

The API will run at `http://localhost:5000`

### 3. Access the Frontend
Open `index.html` in your browser to test all API endpoints

## API Endpoints

### 1. Get All Recipes
```
GET /api/recipes
```
Returns all available recipes with full details.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Caesar Salad",
    "emoji": "🥗",
    "description": "...",
    "category": "Salad",
    "cuisine": "Italian",
    "rating": 4.5,
    "calories": 150,
    "ingredients": [...],
    "keywords": [...]
  }
]
```

---

### 2. Get Single Recipe
```
GET /api/recipe/<id>
```
Returns a specific recipe by ID (1-8).

**Example:**
```
GET /api/recipe/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Caesar Salad",
  "emoji": "🥗",
  "description": "Crisp romaine lettuce with caesar dressing, croutons and parmesan.",
  "category": "Salad",
  "cuisine": "Italian",
  "rating": 4.5,
  "calories": 150,
  "ingredients": ["Romaine Lettuce", "Caesar Dressing", "Croutons", "Parmesan Cheese", "Lemon Juice"],
  "keywords": ["salad", "caesar", "lettuce", "veg"]
}
```

---

### 3. Search Recipes
```
GET /api/search?q=<query>
```
Search recipes by name, cuisine, category, or description.

**Example:**
```
GET /api/search?q=pizza
```

**Response:**
```json
{
  "query": "pizza",
  "results": [
    {
      "id": 2,
      "name": "Margherita Pizza",
      "emoji": "🍕",
      ...
    }
  ],
  "count": 1
}
```

---

### 4. Detect Recipe from Image
```
POST /api/detect
```
Upload an image to detect and identify the recipe.

**Request:**
```
Content-Type: multipart/form-data
- image: <image_file>
```

**Response (Success):**
```json
{
  "detected": true,
  "recipe": {
    "id": 2,
    "name": "Margherita Pizza",
    "emoji": "🍕",
    ...
  },
  "image_path": "uploads/filename.jpg"
}
```

**Response (Not Found):**
```json
{
  "detected": false,
  "error": "Recipe not identified. Try a different image."
}
```

---

### 5. Health Check
```
GET /api/health
```
Check if the API is running.

**Response:**
```json
{
  "status": "ok",
  "message": "Chef's Table API is running"
}
```

---

## Usage Examples

### Using cURL

#### Get all recipes
```bash
curl http://localhost:5000/api/recipes
```

#### Search for pizza
```bash
curl "http://localhost:5000/api/search?q=pizza"
```

#### Get recipe by ID
```bash
curl http://localhost:5000/api/recipe/1
```

#### Detect from image
```bash
curl -X POST -F "image=@path/to/image.jpg" http://localhost:5000/api/detect
```

### Using JavaScript/Fetch

```javascript
const API_URL = 'http://localhost:5000/api';

// Get all recipes
fetch(`${API_URL}/recipes`)
  .then(res => res.json())
  .then(data => console.log(data));

// Search recipes
fetch(`${API_URL}/search?q=pizza`)
  .then(res => res.json())
  .then(data => console.log(data));

// Detect from image
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch(`${API_URL}/detect`, {
  method: 'POST',
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## Project Structure

```
hackathon1/
├── app.py              # Flask REST API application
├── requirements.txt    # Python dependencies
├── index.html         # Web UI for testing API
├── templates/         # (Optional HTML templates)
└── uploads/          # Uploaded images directory
```

---

## Features

✅ **REST API** - Clean JSON endpoints  
✅ **CORS Enabled** - Works with any frontend framework  
✅ **Image Detection** - Upload images to identify recipes  
✅ **Search** - Full-text search across recipes  
✅ **Calorie Tracking** - Nutrition information included  
✅ **Recipe Details** - Ingredients and metadata  

---

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **API**: RESTful JSON
- **CORS**: Flask-CORS

---

## Next Steps

### Integrate with Frontend Frameworks:

**React:**
```javascript
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000/api'
});

// Usage
API.get('/recipes').then(res => console.log(res.data));
```

**Vue:**
```javascript
import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:5000/api'
});

// In component
this.api.get('/recipes').then(data => this.recipes = data);
```

**Angular:**
```typescript
import { HttpClient } from '@angular/common/http';

constructor(private http: HttpClient) {}

getRecipes() {
  return this.http.get('http://localhost:5000/api/recipes');
}
```

---

## License

MIT
