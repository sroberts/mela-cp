"""
Database module for reading Mela recipes.

Mela stores recipes in a SQLite database. This module provides
functions to read and query recipes from the database.
"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, List, Dict, Any


class MelaDatabase:
    """Interface to the Mela recipe database."""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the Mela database connection.
        
        Args:
            db_path: Path to the Mela database file. If None, uses default location.
        """
        if db_path is None:
            # Default Mela database location on macOS
            default_path = Path.home() / "Library" / "Group Containers" / "XXXXXXXX.com.mela.app" / "mela.sqlite"
            # Try to find the actual container directory
            group_containers = Path.home() / "Library" / "Group Containers"
            if group_containers.exists():
                for container in group_containers.iterdir():
                    if "mela" in container.name.lower():
                        potential_db = container / "mela.sqlite"
                        if potential_db.exists():
                            db_path = str(potential_db)
                            break
            
            if db_path is None:
                db_path = str(default_path)
        
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Mela database not found at {self.db_path}")
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def list_recipes(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all recipes in the database.
        
        Args:
            limit: Maximum number of recipes to return.
            
        Returns:
            List of recipe dictionaries with basic information.
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                """
                SELECT id, title, text, date, link 
                FROM ZRECIPE 
                WHERE title IS NOT NULL
                ORDER BY date DESC
                LIMIT ?
                """,
                (limit,)
            )
            recipes = []
            for row in cursor:
                recipes.append({
                    "id": row["id"],
                    "title": row["title"],
                    "text": row["text"],
                    "date": row["date"],
                    "link": row["link"]
                })
            return recipes
        finally:
            conn.close()
    
    def get_recipe(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific recipe by ID.
        
        Args:
            recipe_id: The recipe ID.
            
        Returns:
            Recipe dictionary or None if not found.
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                """
                SELECT * FROM ZRECIPE WHERE id = ?
                """,
                (recipe_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            
            return dict(row)
        finally:
            conn.close()
    
    def search_recipes(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search recipes by title or content.
        
        Args:
            query: Search query string.
            limit: Maximum number of results to return.
            
        Returns:
            List of matching recipes.
        """
        conn = self._get_connection()
        try:
            search_pattern = f"%{query}%"
            cursor = conn.execute(
                """
                SELECT id, title, text, date, link 
                FROM ZRECIPE 
                WHERE title LIKE ? OR text LIKE ?
                ORDER BY date DESC
                LIMIT ?
                """,
                (search_pattern, search_pattern, limit)
            )
            recipes = []
            for row in cursor:
                recipes.append({
                    "id": row["id"],
                    "title": row["title"],
                    "text": row["text"],
                    "date": row["date"],
                    "link": row["link"]
                })
            return recipes
        finally:
            conn.close()
    
    def get_categories(self) -> List[str]:
        """
        Get all recipe categories.
        
        Returns:
            List of category names.
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                """
                SELECT DISTINCT categories FROM ZRECIPE 
                WHERE categories IS NOT NULL AND categories != ''
                """
            )
            categories = set()
            for row in cursor:
                if row["categories"]:
                    # Categories might be stored as comma-separated or JSON
                    try:
                        cats = json.loads(row["categories"])
                        if isinstance(cats, list):
                            categories.update(cats)
                        else:
                            categories.add(str(cats))
                    except (json.JSONDecodeError, TypeError):
                        # Try splitting by comma
                        cat_str = row["categories"]
                        if "," in cat_str:
                            categories.update([c.strip() for c in cat_str.split(",")])
                        else:
                            categories.add(cat_str)
            return sorted(list(categories))
        finally:
            conn.close()
