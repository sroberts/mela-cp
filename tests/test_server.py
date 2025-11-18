"""
Tests for the MCP server implementation.

Tests server initialization, tool registration, and tool handlers.
"""

import pytest
from mela_cp.server import app, call_tool, list_tools
from mela_cp.database import MelaDatabase
from mela_cp import server


class TestServerInitialization:
    """Tests for server initialization."""
    
    def test_server_exists(self):
        """Test that the server app is created."""
        assert app is not None
        assert app.name == "mela-cp"
    
    def test_server_name(self):
        """Test that the server has the correct name."""
        assert app.name == "mela-cp"


class TestListTools:
    """Tests for listing available tools."""
    
    @pytest.mark.asyncio
    async def test_list_tools_returns_four_tools(self):
        """Test that four tools are registered."""
        tools = await list_tools()
        
        assert len(tools) == 4
    
    @pytest.mark.asyncio
    async def test_list_tools_includes_required_tools(self):
        """Test that all required tools are present."""
        tools = await list_tools()
        tool_names = [tool.name for tool in tools]
        
        assert "list_recipes" in tool_names
        assert "get_recipe" in tool_names
        assert "search_recipes" in tool_names
        assert "get_categories" in tool_names
    
    @pytest.mark.asyncio
    async def test_tools_have_descriptions(self):
        """Test that all tools have descriptions."""
        tools = await list_tools()
        
        for tool in tools:
            assert tool.description is not None
            assert len(tool.description) > 0
    
    @pytest.mark.asyncio
    async def test_tools_have_input_schemas(self):
        """Test that all tools have input schemas."""
        tools = await list_tools()
        
        for tool in tools:
            assert tool.inputSchema is not None
            assert "type" in tool.inputSchema


class TestCallToolListRecipes:
    """Tests for the list_recipes tool."""
    
    @pytest.mark.asyncio
    async def test_list_recipes_without_db(self):
        """Test list_recipes when database is not initialized."""
        # Save current db state
        original_db = server.db
        server.db = None
        
        try:
            result = await call_tool("list_recipes", {})
            
            assert len(result) == 1
            assert "Error" in result[0].text
            assert "database not initialized" in result[0].text
        finally:
            # Restore original state
            server.db = original_db
    
    @pytest.mark.asyncio
    async def test_list_recipes_with_db(self, test_db_path):
        """Test list_recipes with a valid database."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(test_db_path))
        
        try:
            result = await call_tool("list_recipes", {"limit": 10})
            
            assert len(result) == 1
            assert "recipe" in result[0].text.lower()
            assert "Found 3 recipe(s)" in result[0].text
        finally:
            # Restore original state
            server.db = original_db
    
    @pytest.mark.asyncio
    async def test_list_recipes_respects_limit(self, test_db_path):
        """Test that list_recipes respects the limit parameter."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(test_db_path))
        
        try:
            result = await call_tool("list_recipes", {"limit": 2})
            
            # Should only show 2 recipes in the output
            assert len(result) == 1
            # Count occurrences of "(ID:" which appears once per recipe
            id_count = result[0].text.count("(ID:")
            assert id_count == 2
        finally:
            # Restore original state
            server.db = original_db


class TestCallToolGetRecipe:
    """Tests for the get_recipe tool."""
    
    @pytest.mark.asyncio
    async def test_get_recipe_without_recipe_id(self, test_db_path):
        """Test get_recipe without providing recipe_id."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(test_db_path))
        
        try:
            result = await call_tool("get_recipe", {})
            
            assert len(result) == 1
            assert "Error" in result[0].text
            assert "recipe_id is required" in result[0].text
        finally:
            # Restore original state
            server.db = original_db
    
    @pytest.mark.asyncio
    async def test_get_recipe_with_valid_id(self, test_db_path):
        """Test get_recipe with a valid recipe ID."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(test_db_path))
        
        try:
            result = await call_tool("get_recipe", {"recipe_id": 1})
            
            assert len(result) == 1
            assert "Chocolate Chip Cookies" in result[0].text
            assert "Ingredients" in result[0].text
        finally:
            # Restore original state
            server.db = original_db
    
    @pytest.mark.asyncio
    async def test_get_recipe_with_invalid_id(self, test_db_path):
        """Test get_recipe with a nonexistent recipe ID."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(test_db_path))
        
        try:
            result = await call_tool("get_recipe", {"recipe_id": 999})
            
            assert len(result) == 1
            assert "not found" in result[0].text
        finally:
            # Restore original state
            server.db = original_db


class TestCallToolSearchRecipes:
    """Tests for the search_recipes tool."""
    
    @pytest.mark.asyncio
    async def test_search_recipes_without_query(self, test_db_path):
        """Test search_recipes without providing a query."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(test_db_path))
        
        try:
            result = await call_tool("search_recipes", {})
            
            assert len(result) == 1
            assert "Error" in result[0].text
            assert "query is required" in result[0].text
        finally:
            # Restore original state
            server.db = original_db
    
    @pytest.mark.asyncio
    async def test_search_recipes_with_query(self, test_db_path):
        """Test search_recipes with a valid query."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(test_db_path))
        
        try:
            result = await call_tool("search_recipes", {"query": "pasta"})
            
            assert len(result) == 1
            assert "Carbonara" in result[0].text
            assert "matching 'pasta'" in result[0].text
        finally:
            # Restore original state
            server.db = original_db
    
    @pytest.mark.asyncio
    async def test_search_recipes_no_results(self, test_db_path):
        """Test search_recipes with no matching results."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(test_db_path))
        
        try:
            result = await call_tool("search_recipes", {"query": "nonexistent"})
            
            assert len(result) == 1
            assert "No recipes found" in result[0].text
        finally:
            # Restore original state
            server.db = original_db


class TestCallToolGetCategories:
    """Tests for the get_categories tool."""
    
    @pytest.mark.asyncio
    async def test_get_categories_with_db(self, test_db_path):
        """Test get_categories with a valid database."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(test_db_path))
        
        try:
            result = await call_tool("get_categories", {})
            
            assert len(result) == 1
            assert "categor" in result[0].text.lower()
            assert "Dessert" in result[0].text
            assert "Pasta" in result[0].text
        finally:
            # Restore original state
            server.db = original_db
    
    @pytest.mark.asyncio
    async def test_get_categories_empty_db(self, empty_db_path):
        """Test get_categories with an empty database."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(empty_db_path))
        
        try:
            result = await call_tool("get_categories", {})
            
            assert len(result) == 1
            assert "No categories found" in result[0].text
        finally:
            # Restore original state
            server.db = original_db


class TestCallToolUnknown:
    """Tests for unknown tool calls."""
    
    @pytest.mark.asyncio
    async def test_unknown_tool(self, test_db_path):
        """Test calling an unknown tool."""
        # Save current db state
        original_db = server.db
        server.db = MelaDatabase(str(test_db_path))
        
        try:
            result = await call_tool("unknown_tool", {})
            
            assert len(result) == 1
            assert "Unknown tool" in result[0].text
        finally:
            # Restore original state
            server.db = original_db
