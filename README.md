# mela-cp

A local MCP (Model Context Protocol) server for accessing Mela recipes from Claude and other AI assistants.

## Overview

Mela is a popular recipe manager app for macOS and iOS. This MCP server allows you to query and access your Mela recipes directly from Claude Desktop, making it easy to search for recipes, get cooking instructions, and explore your recipe collection through natural conversation.

## Features

- **List Recipes**: Browse all your recipes with titles and metadata
- **Search Recipes**: Find recipes by title or content
- **Get Recipe Details**: Retrieve full recipe information including ingredients and instructions
- **Browse Categories**: Explore recipes by category

## Installation

1. Clone this repository:
```bash
git clone https://github.com/sroberts/mela-cp.git
cd mela-cp
```

2. Install the package:
```bash
pip install -e .
```

## Configuration

### Finding Your Mela Database

Mela stores recipes in a SQLite database. The default location on macOS is typically:
```
~/Library/Group Containers/[app-id].com.mela.app/mela.sqlite
```

The server will automatically try to locate your Mela database in the Group Containers directory. If it can't find it automatically, you can specify the path using the `MELA_DB_PATH` environment variable.

### Configure Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mela": {
      "command": "mela-cp"
    }
  }
}
```

If you need to specify a custom database path:

```json
{
  "mcpServers": {
    "mela": {
      "command": "mela-cp",
      "env": {
        "MELA_DB_PATH": "/path/to/your/mela.sqlite"
      }
    }
  }
}
```

## Usage

Once configured, you can interact with your Mela recipes through Claude Desktop:

- "Show me all my recipes"
- "Find recipes with chicken"
- "Get the recipe for chocolate chip cookies"
- "What categories do I have?"

## Available Tools

The server exposes the following tools to Claude:

- `list_recipes`: List all recipes (with optional limit)
- `search_recipes`: Search recipes by query string
- `get_recipe`: Get detailed information for a specific recipe by ID
- `get_categories`: List all recipe categories

## Development

### Running Locally

```bash
python -m mela_cp.server
```

### Environment Variables

- `MELA_DB_PATH`: Path to the Mela SQLite database file (optional if using default location)

## License

See [LICENSE](LICENSE) file for details.

## Troubleshooting

### Database Not Found

If you get an error about the database not being found:

1. Check that Mela is installed on your system
2. Verify the database path by looking in:
   ```bash
   ls ~/Library/Group\ Containers/*/mela.sqlite
   ```
3. Set the `MELA_DB_PATH` environment variable to the correct path in your Claude Desktop config

### Server Not Starting

If the MCP server doesn't start:

1. Verify the installation:
   ```bash
   which mela-cp
   ```
2. Test the command manually:
   ```bash
   MELA_DB_PATH=/path/to/mela.sqlite mela-cp
   ```
3. Check Claude Desktop logs for error messages

### No Recipes Showing

If recipes aren't showing up:

1. Verify your database has recipes:
   ```bash
   sqlite3 /path/to/mela.sqlite "SELECT COUNT(*) FROM ZRECIPE"
   ```
2. Check that the table schema matches what's expected
3. Look for any error messages in Claude Desktop

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
