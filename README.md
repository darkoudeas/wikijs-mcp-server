# 📚 WikiJS MCP Server

**Connect Claude to your Wiki.js documentation!** 

This tool lets Claude read and update your Wiki.js pages directly. Think of it as giving Claude access to your team's knowledge base - perfect for keeping documentation up-to-date or finding information quickly.

## 🎯 What This Does

Once installed, you can ask Claude to:
- 🔍 **Search** your wiki for specific topics
- 📖 **Read** documentation pages
- ✏️ **Update** existing pages with new information
- 📝 **Create** new documentation
- 🗂️ **Organize** pages by moving them around
- 🗑️ **Delete** outdated pages

## 🚀 Installation Guide

### Prerequisites
Before starting, make sure you have:
- ✅ **Git** installed ([Download here](https://git-scm.com/downloads))
- ✅ **Python 3.8 or newer** ([Download here](https://www.python.org/downloads/))
- ✅ **Claude Code** installed ([Get it here](https://claude.ai/code))
- ✅ **Access to a Wiki.js site** (with an API key - we'll show you how to get one!)

### Step 1: Download the Code

Open your terminal (Command Prompt on Windows, Terminal on Mac) and run:

```bash
git clone https://github.com/your-username/wikijs-mcp.git
cd wikijs-mcp
```

💡 **Tip**: If you get a "command not found" error, make sure Git is installed!

### Step 2: Get Your Wiki.js API Key

1. **Log into your Wiki.js site** as an administrator
2. Navigate to **Administration** (usually in the top menu)
3. Click on **API Access** in the left sidebar
4. If the API is disabled, click the toggle to **Enable** it
5. Click **"+ New API Key"**
6. Give it a name like "Claude Integration"
7. Select these permissions:
   - ✅ Read Pages
   - ✅ Write Pages
   - ✅ Manage Pages (if you want Claude to create/delete pages)
8. Click **Create** and **copy the API key** - you'll need it next!

⚠️ **Important**: Save this key somewhere safe - you won't be able to see it again!

### Step 3: Configure Your Connection

1. **Create the configuration file**:
   ```bash
   cp .env.example .env
   ```

2. **Open the `.env` file** in any text editor (Notepad, TextEdit, VS Code, etc.)

3. **Replace the example values** with your actual information:
   ```env
   WIKIJS_URL=https://your-wiki-site.com
   WIKIJS_API_KEY=paste-your-api-key-here
   ```

   📌 **Example**:
   ```env
   WIKIJS_URL=https://docs.mycompany.com
   WIKIJS_API_KEY=ey1234567890abcdef...
   ```

### Step 4: Install Python Dependencies

Run this command to install what the tool needs:

```bash
pip install -e .
```

💡 **Troubleshooting**:
- If you get "pip: command not found", try `pip3` instead
- On Mac, you might need to use `python3 -m pip install -e .`

### Step 5: Test the Connection

Let's make sure everything works! Run:

```bash
python -m wikijs_mcp.server
```

You should see something like:
```
WikiJS MCP Server starting...
Connected to Wiki.js at https://your-wiki-site.com
Ready to accept connections!
```

Press `Ctrl+C` to stop it.

## 🎉 Using with Claude Code

The best part - **Claude Code will automatically detect this MCP server!** 

The repository includes a special `.mcp.json` file that Claude Code reads automatically. Just:

1. **Open Claude Code** in the `wikijs-mcp` folder
2. Claude will automatically have access to your Wiki.js!

### Try These Commands

Once connected, you can ask Claude things like:

```
"Search my wiki for information about deployment procedures"

"Read the page at /docs/getting-started"

"Update the troubleshooting guide with a new solution for login issues"

"Create a new page at /docs/api/webhooks with webhook documentation"
```

## 🔧 Manual Configuration (Advanced)

If you're using a different MCP client or need custom settings, here's the configuration:

### For Standard Installation
```json
{
  "mcpServers": {
    "wikijs": {
      "command": "python",
      "args": ["-m", "wikijs_mcp.server"],
      "env": {
        "WIKIJS_URL": "https://your-wiki-site.com",
        "WIKIJS_API_KEY": "your-api-key"
      }
    }
  }
}
```

### For Docker Users
```json
{
  "mcpServers": {
    "wikijs": {
      "command": "docker",
      "args": ["compose", "run", "--rm", "-T", "wikijs-mcp-server", "python3", "-m", "wikijs_mcp.server"],
      "cwd": "/path/to/wikijs-mcp"
    }
  }
}
```

## 🆘 Common Issues & Solutions

### "Connection refused" or "Cannot connect to Wiki.js"
- ✅ Check your `WIKIJS_URL` doesn't have a trailing slash
- ✅ Make sure your Wiki.js site is accessible from your computer
- ✅ Verify the API is enabled in Wiki.js admin panel

### "Authentication failed" or "Invalid API key"
- ✅ Double-check you copied the entire API key
- ✅ Make sure there are no extra spaces before/after the key
- ✅ Verify the API key has the right permissions

### "Module not found" errors
- ✅ Make sure you ran `pip install -e .` in the wikijs-mcp folder
- ✅ Try using `python3` instead of `python`

### Claude Code doesn't see the Wiki.js tools
- ✅ Make sure you're running Claude Code from the wikijs-mcp folder
- ✅ Check that the `.mcp.json` file exists
- ✅ Try restarting Claude Code

### `421 Misdirected Request` on `OPTIONS /mcp` (cloud/reverse proxy)
- ✅ Set `MCP_ENABLE_DNS_REBINDING_PROTECTION=false` to disable strict Host/Origin checks (recommended default behind ingress)
- ✅ Or keep protection enabled and set explicit values:
  - `MCP_ENABLE_DNS_REBINDING_PROTECTION=true`
  - `MCP_PUBLIC_HOST=your-public-hostname`
  - `MCP_ALLOWED_HOSTS=your-public-hostname,your-public-hostname:*`
  - `MCP_ALLOWED_ORIGINS=http://localhost:*,http://127.0.0.1:*` (add your real client origins as needed)
- ✅ Keep `HTTP_HOST=0.0.0.0` for container binding; use `MCP_PUBLIC_HOST` for external hostname

## 📚 Available Tools Reference

Here's what Claude can do once connected:

| Tool | What it does | Example |
|------|--------------|---------|
| 🔍 **wiki_search** | Find pages by title or content | "Search for 'authentication'" |
| 📖 **wiki_get_page** | Read a specific page | "Get page at path '/docs/api'" |
| 📋 **wiki_list_pages** | See all pages | "List all wiki pages" |
| 🌳 **wiki_get_tree** | View wiki structure | "Show wiki page tree" |
| ✏️ **wiki_create_page** | Make new pages | "Create page at '/guides/setup'" |
| 🔄 **wiki_update_page** | Edit existing pages | "Update page ID 123" |
| 🚚 **wiki_move_page** | Relocate pages | "Move page to '/archive/old'" |
| 🗑️ **wiki_delete_page** | Remove pages | "Delete page ID 456" |

## 🛠️ For Developers

### Running Tests
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=wikijs_mcp
```

### Code Quality
```bash
# Format code
black wikijs_mcp/ tests/

# Type checking
mypy wikijs_mcp/
```

## 📄 License

MIT License - feel free to use and modify!

## 💬 Need Help?

- Check the [Common Issues](#-common-issues--solutions) section above
- Look at the [Wiki.js documentation](https://docs.requarks.io/)
- Open an issue on GitHub if you're stuck!

---

**Happy documenting!** 🎉