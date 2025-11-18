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

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer that avoids externally managed environment issues.

1. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone this repository:
```bash
git clone https://github.com/sroberts/mela-cp.git
cd mela-cp
```

3. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On macOS/Linux
# Or on Windows: .venv\Scripts\activate
```

4. Install the package:
```bash
uv pip install -e .
```

### Using pip

If you prefer to use pip:

1. Clone this repository:
```bash
git clone https://github.com/sroberts/mela-cp.git
cd mela-cp
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# Or on Windows: .venv\Scripts\activate
```

3. Install the package:
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

**Important**: Since the package is installed in a virtual environment, you need to use the full path to the Python interpreter from your virtual environment.

#### Option 1: Using Python module (Recommended)

Replace `/path/to/mela-cp` with the actual path to your cloned repository:

```json
{
  "mcpServers": {
    "mela": {
      "command": "/path/to/mela-cp/.venv/bin/python",
      "args": ["-m", "mela_cp.server"]
    }
  }
}
```

For example, if you cloned to `~/projects/mela-cp`:
```json
{
  "mcpServers": {
    "mela": {
      "command": "/Users/sroberts/projects/mela-cp/.venv/bin/python",
      "args": ["-m", "mela_cp.server"]
    }
  }
}
```

#### Option 2: Using the mela-cp command directly

Find the full path to mela-cp in your virtual environment:
```bash
cd /path/to/mela-cp
source .venv/bin/activate
which mela-cp
```

Then use that full path in the configuration:
```json
{
  "mcpServers": {
    "mela": {
      "command": "/path/to/mela-cp/.venv/bin/mela-cp"
    }
  }
}
```

If you need to specify a custom database path:

```json
{
  "mcpServers": {
    "mela": {
      "command": "/path/to/mela-cp/.venv/bin/python",
      "args": ["-m", "mela_cp.server"],
      "env": {
        "MELA_DB_PATH": "/path/to/your/mela.sqlite"
      }
    }
  }
}
```

## Starting the Server

The MCP server is designed to run automatically when called by Claude Desktop, but you can also start it manually for testing:

### Via Claude Desktop (Recommended)

Once configured in Claude Desktop (see Configuration section above), the server starts automatically when you interact with Claude. Simply restart Claude Desktop after adding the configuration, and the server will be available.

### Manual Start (For Testing)

To start the server manually:

```bash
mela-cp
```

Or with a custom database path:

```bash
MELA_DB_PATH=/path/to/your/mela.sqlite mela-cp
```

The server runs in stdio mode and waits for MCP protocol messages. You'll see no output unless there's an error - this is normal behavior. Press `Ctrl+C` to stop the server.

**Note**: Manual testing requires sending MCP protocol messages via stdin. For regular use, it's recommended to use the server through Claude Desktop.

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

### Running Tests

Install test dependencies:

```bash
# Using uv (recommended)
uv pip install -e ".[test]"

# Or using pip
pip install -e ".[test]"
```

Run the test suite:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
# Using uv (recommended)
uv pip install pytest-cov
pytest tests/ --cov=src/mela_cp --cov-report=term-missing

# Or using pip
pip install pytest-cov
pytest tests/ --cov=src/mela_cp --cov-report=term-missing
```

The test suite includes:
- **36 tests** covering database operations and MCP server functionality
- Unit tests for all database methods (list, search, get, categories)
- Integration tests for all MCP tools
- Tests for error handling and edge cases

### Environment Variables

- `MELA_DB_PATH`: Path to the Mela SQLite database file (optional if using default location)

## License

See [LICENSE](LICENSE) file for details.

## Troubleshooting

### "spawn mela-cp ENOENT" Error in Claude Desktop

If Claude Desktop shows `spawn mela-cp ENOENT` error:

**Problem**: Claude Desktop cannot find the `mela-cp` command because it's installed in a virtual environment.

**Solution**: Update your Claude Desktop config to use the full path to Python in your virtual environment:

1. Find your project path (where you cloned mela-cp)
2. Update `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mela": {
      "command": "/full/path/to/mela-cp/.venv/bin/python",
      "args": ["-m", "mela_cp.server"]
    }
  }
}
```

For example:
```json
{
  "mcpServers": {
    "mela": {
      "command": "/Users/sroberts/projects/mela-cp/.venv/bin/python",
      "args": ["-m", "mela_cp.server"]
    }
  }
}
```

3. Restart Claude Desktop

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
   cd /path/to/mela-cp
   source .venv/bin/activate
   which mela-cp
   ```
2. Test the command manually:
   ```bash
   MELA_DB_PATH=/path/to/mela.sqlite python -m mela_cp.server
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
