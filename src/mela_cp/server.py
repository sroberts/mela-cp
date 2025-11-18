"""
MCP Server for Mela recipes.

This server implements the Model Context Protocol to expose Mela recipes
to Claude and other AI assistants.
"""

import asyncio
import os
from typing import Any, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .database import MelaDatabase


# Initialize the MCP server
app = Server("mela-cp")

# Global database instance
db: Optional[MelaDatabase] = None


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools for interacting with Mela recipes.
    
    Returns:
        List of available tools.
    """
    return [
        Tool(
            name="list_recipes",
            description="List all recipes from Mela. Returns a list of recipes with their titles, IDs, and basic information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of recipes to return (default: 100)",
                        "default": 100
                    }
                }
            }
        ),
        Tool(
            name="get_recipe",
            description="Get detailed information about a specific recipe by ID. Returns the full recipe including ingredients, instructions, and metadata.",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipe_id": {
                        "type": "number",
                        "description": "The ID of the recipe to retrieve",
                    }
                },
                "required": ["recipe_id"]
            }
        ),
        Tool(
            name="search_recipes",
            description="Search for recipes by title or content. Returns matching recipes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to match against recipe titles and content"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results to return (default: 50)",
                        "default": 50
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_categories",
            description="Get all recipe categories available in Mela. Returns a list of category names.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool calls from the MCP client.
    
    Args:
        name: Name of the tool to call.
        arguments: Tool arguments.
        
    Returns:
        List of content items representing the tool's response.
    """
    global db
    
    if db is None:
        return [TextContent(
            type="text",
            text="Error: Mela database not initialized. Please check the database path configuration."
        )]
    
    try:
        if name == "list_recipes":
            limit = arguments.get("limit", 100)
            recipes = db.list_recipes(limit=limit)
            
            # Format recipes as a readable list
            if not recipes:
                return [TextContent(
                    type="text",
                    text="No recipes found in the Mela database."
                )]
            
            result = f"Found {len(recipes)} recipe(s):\n\n"
            for recipe in recipes:
                result += f"**{recipe['title']}** (ID: {recipe['id']})\n"
                if recipe.get('date'):
                    result += f"  Date: {recipe['date']}\n"
                if recipe.get('link'):
                    result += f"  Source: {recipe['link']}\n"
                result += "\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "get_recipe":
            recipe_id = arguments.get("recipe_id")
            if recipe_id is None:
                return [TextContent(
                    type="text",
                    text="Error: recipe_id is required"
                )]
            
            recipe = db.get_recipe(int(recipe_id))
            if recipe is None:
                return [TextContent(
                    type="text",
                    text=f"Recipe with ID {recipe_id} not found."
                )]
            
            # Format recipe details
            result = f"# {recipe.get('title', 'Untitled Recipe')}\n\n"
            
            if recipe.get('link'):
                result += f"**Source:** {recipe['link']}\n\n"
            
            if recipe.get('date'):
                result += f"**Date:** {recipe['date']}\n\n"
            
            if recipe.get('text'):
                result += f"{recipe['text']}\n\n"
            
            # Add other available fields
            for key, value in recipe.items():
                if key not in ['id', 'title', 'text', 'date', 'link'] and value:
                    result += f"**{key}:** {value}\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "search_recipes":
            query = arguments.get("query")
            if not query:
                return [TextContent(
                    type="text",
                    text="Error: query is required"
                )]
            
            limit = arguments.get("limit", 50)
            recipes = db.search_recipes(query, limit=limit)
            
            if not recipes:
                return [TextContent(
                    type="text",
                    text=f"No recipes found matching '{query}'."
                )]
            
            result = f"Found {len(recipes)} recipe(s) matching '{query}':\n\n"
            for recipe in recipes:
                result += f"**{recipe['title']}** (ID: {recipe['id']})\n"
                if recipe.get('date'):
                    result += f"  Date: {recipe['date']}\n"
                if recipe.get('link'):
                    result += f"  Source: {recipe['link']}\n"
                result += "\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "get_categories":
            categories = db.get_categories()
            
            if not categories:
                return [TextContent(
                    type="text",
                    text="No categories found in the Mela database."
                )]
            
            result = f"Found {len(categories)} categor{'y' if len(categories) == 1 else 'ies'}:\n\n"
            for category in categories:
                result += f"- {category}\n"
            
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]


async def run_server():
    """Run the MCP server."""
    global db
    
    # Initialize the database
    db_path = os.environ.get("MELA_DB_PATH")
    try:
        db = MelaDatabase(db_path)
    except FileNotFoundError as e:
        print(f"Warning: {e}", flush=True)
        print("Set MELA_DB_PATH environment variable to specify the database location.", flush=True)
        # Continue anyway to allow the server to start
        db = None
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def main():
    """Main entry point for the server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
