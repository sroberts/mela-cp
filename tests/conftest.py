"""
Fixtures for mela-cp tests.

Provides shared test fixtures including a test database with sample recipes.
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path


@pytest.fixture
def test_db_path(tmp_path):
    """
    Create a temporary test database with sample recipes.
    
    Returns:
        Path to the test database file.
    """
    db_path = tmp_path / "test_mela.sqlite"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create the ZRECIPE table (based on typical Mela database schema)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ZRECIPE (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            text TEXT,
            date TEXT,
            link TEXT,
            categories TEXT
        )
    """)
    
    # Insert sample recipes
    sample_recipes = [
        (
            "Chocolate Chip Cookies",
            """**Ingredients:**
- 2 1/4 cups all-purpose flour
- 1 tsp baking soda
- 1 cup butter, softened
- 2 large eggs
- 2 cups chocolate chips

**Instructions:**
1. Preheat oven to 375°F (190°C).
2. Combine flour and baking soda.
3. Beat butter and sugars until creamy.
4. Add eggs and vanilla.
5. Gradually blend in flour mixture.
6. Stir in chocolate chips.
7. Bake 9-11 minutes.""",
            "2024-01-15",
            "https://example.com/cookies",
            "Dessert,Baking"
        ),
        (
            "Classic Spaghetti Carbonara",
            """**Ingredients:**
- 400g spaghetti
- 200g pancetta or guanciale, diced
- 4 large eggs
- 100g Pecorino Romano cheese, grated
- Black pepper to taste

**Instructions:**
1. Cook spaghetti in salted boiling water.
2. Fry pancetta until crispy.
3. Beat eggs with grated cheese.
4. Mix hot pasta with pancetta.
5. Add egg mixture quickly.
6. Serve immediately.""",
            "2024-02-10",
            "https://example.com/carbonara",
            "Pasta,Italian,Main Dish"
        ),
        (
            "Simple Green Salad",
            """**Ingredients:**
- 6 cups mixed greens
- 1 cucumber, sliced
- 1 cup cherry tomatoes
- 3 tbsp olive oil
- 1 tbsp balsamic vinegar

**Instructions:**
1. Wash and dry greens.
2. Combine greens, cucumber, tomatoes.
3. Whisk together oil, vinegar.
4. Toss and serve.""",
            "2024-03-05",
            "https://example.com/salad",
            "Salad,Side Dish,Vegetarian"
        )
    ]
    
    cursor.executemany("""
        INSERT INTO ZRECIPE (title, text, date, link, categories)
        VALUES (?, ?, ?, ?, ?)
    """, sample_recipes)
    
    conn.commit()
    conn.close()
    
    return db_path


@pytest.fixture
def empty_db_path(tmp_path):
    """
    Create an empty test database with no recipes.
    
    Returns:
        Path to the empty test database file.
    """
    db_path = tmp_path / "empty_mela.sqlite"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create the ZRECIPE table but don't insert any data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ZRECIPE (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            text TEXT,
            date TEXT,
            link TEXT,
            categories TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    
    return db_path
