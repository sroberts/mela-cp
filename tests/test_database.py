"""
Tests for the MelaDatabase class.

Tests database connection, recipe retrieval, search, and category parsing.
"""

import pytest
from pathlib import Path
from mela_cp.database import MelaDatabase


class TestMelaDatabaseInit:
    """Tests for MelaDatabase initialization."""
    
    def test_init_with_valid_path(self, test_db_path):
        """Test database initialization with a valid path."""
        db = MelaDatabase(str(test_db_path))
        assert db.db_path == test_db_path
    
    def test_init_with_nonexistent_path(self, tmp_path):
        """Test that initialization fails with a nonexistent path."""
        nonexistent_path = tmp_path / "nonexistent.sqlite"
        with pytest.raises(FileNotFoundError) as exc_info:
            MelaDatabase(str(nonexistent_path))
        assert "Mela database not found" in str(exc_info.value)


class TestListRecipes:
    """Tests for listing recipes."""
    
    def test_list_recipes_returns_all(self, test_db_path):
        """Test listing all recipes."""
        db = MelaDatabase(str(test_db_path))
        recipes = db.list_recipes()
        
        assert len(recipes) == 3
        assert all('id' in recipe for recipe in recipes)
        assert all('title' in recipe for recipe in recipes)
    
    def test_list_recipes_with_limit(self, test_db_path):
        """Test listing recipes with a limit."""
        db = MelaDatabase(str(test_db_path))
        recipes = db.list_recipes(limit=2)
        
        assert len(recipes) == 2
    
    def test_list_recipes_empty_database(self, empty_db_path):
        """Test listing recipes from an empty database."""
        db = MelaDatabase(str(empty_db_path))
        recipes = db.list_recipes()
        
        assert len(recipes) == 0
        assert recipes == []
    
    def test_list_recipes_ordered_by_date(self, test_db_path):
        """Test that recipes are ordered by date descending."""
        db = MelaDatabase(str(test_db_path))
        recipes = db.list_recipes()
        
        # The most recent should be first
        assert recipes[0]['title'] == "Simple Green Salad"
        assert recipes[0]['date'] == "2024-03-05"


class TestGetRecipe:
    """Tests for getting a single recipe."""
    
    def test_get_recipe_by_id(self, test_db_path):
        """Test retrieving a recipe by ID."""
        db = MelaDatabase(str(test_db_path))
        recipe = db.get_recipe(1)
        
        assert recipe is not None
        assert recipe['id'] == 1
        assert recipe['title'] == "Chocolate Chip Cookies"
        assert 'Ingredients' in recipe['text']
    
    def test_get_recipe_nonexistent_id(self, test_db_path):
        """Test retrieving a nonexistent recipe."""
        db = MelaDatabase(str(test_db_path))
        recipe = db.get_recipe(999)
        
        assert recipe is None
    
    def test_get_recipe_includes_all_fields(self, test_db_path):
        """Test that get_recipe returns all database fields."""
        db = MelaDatabase(str(test_db_path))
        recipe = db.get_recipe(1)
        
        assert 'id' in recipe
        assert 'title' in recipe
        assert 'text' in recipe
        assert 'date' in recipe
        assert 'link' in recipe
        assert 'categories' in recipe


class TestSearchRecipes:
    """Tests for searching recipes."""
    
    def test_search_by_title(self, test_db_path):
        """Test searching recipes by title."""
        db = MelaDatabase(str(test_db_path))
        results = db.search_recipes("Carbonara")
        
        assert len(results) == 1
        assert results[0]['title'] == "Classic Spaghetti Carbonara"
    
    def test_search_by_content(self, test_db_path):
        """Test searching recipes by content."""
        db = MelaDatabase(str(test_db_path))
        results = db.search_recipes("chocolate")
        
        assert len(results) == 1
        assert results[0]['title'] == "Chocolate Chip Cookies"
    
    def test_search_case_insensitive(self, test_db_path):
        """Test that search is case insensitive."""
        db = MelaDatabase(str(test_db_path))
        results_lower = db.search_recipes("pasta")
        results_upper = db.search_recipes("PASTA")
        
        assert len(results_lower) == len(results_upper)
        assert results_lower[0]['title'] == results_upper[0]['title']
    
    def test_search_no_results(self, test_db_path):
        """Test searching with no matching results."""
        db = MelaDatabase(str(test_db_path))
        results = db.search_recipes("nonexistent")
        
        assert len(results) == 0
        assert results == []
    
    def test_search_with_limit(self, test_db_path):
        """Test searching with a result limit."""
        db = MelaDatabase(str(test_db_path))
        results = db.search_recipes("cups", limit=1)
        
        assert len(results) <= 1


class TestGetCategories:
    """Tests for getting recipe categories."""
    
    def test_get_categories(self, test_db_path):
        """Test retrieving all categories."""
        db = MelaDatabase(str(test_db_path))
        categories = db.get_categories()
        
        assert len(categories) > 0
        assert "Dessert" in categories
        assert "Baking" in categories
        assert "Pasta" in categories
        assert "Italian" in categories
        assert "Main Dish" in categories
        assert "Salad" in categories
        assert "Side Dish" in categories
        assert "Vegetarian" in categories
    
    def test_categories_are_sorted(self, test_db_path):
        """Test that categories are returned sorted."""
        db = MelaDatabase(str(test_db_path))
        categories = db.get_categories()
        
        assert categories == sorted(categories)
    
    def test_categories_are_unique(self, test_db_path):
        """Test that categories are unique."""
        db = MelaDatabase(str(test_db_path))
        categories = db.get_categories()
        
        assert len(categories) == len(set(categories))
    
    def test_get_categories_empty_database(self, empty_db_path):
        """Test getting categories from an empty database."""
        db = MelaDatabase(str(empty_db_path))
        categories = db.get_categories()
        
        assert len(categories) == 0
        assert categories == []
