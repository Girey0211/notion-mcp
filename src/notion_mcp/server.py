"""Notion MCP Server - Main server implementation."""

import os
from typing import Any
from dotenv import load_dotenv
from notion_client import Client
from fastmcp import FastMCP

from .notion_client import create_calendar_page, create_list_page


# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Notion MCP Server")

# Get environment variables
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_CALENDAR_DB_ID = os.getenv("NOTION_CALENDAR_DB_ID")
NOTION_LIST_DB_ID = os.getenv("NOTION_LIST_DB_ID")

# Initialize Notion client
if not NOTION_API_TOKEN:
    raise ValueError("NOTION_API_TOKEN environment variable is required")

notion = Client(auth=NOTION_API_TOKEN)


@mcp.tool()
def add_calendar_event(
    title: str,
    date: str,
    description: str = ""
) -> str:
    """
    Add a new event to the Notion calendar database.
    
    Args:
        title: Event title/name
        date: Event date in ISO format (YYYY-MM-DD) or ISO datetime (YYYY-MM-DDTHH:MM:SS)
        description: Optional event description
    
    Returns:
        Success message with the created page URL
    """
    if not NOTION_CALENDAR_DB_ID:
        return "Error: NOTION_CALENDAR_DB_ID environment variable is not set"
    
    try:
        result = create_calendar_page(
            client=notion,
            database_id=NOTION_CALENDAR_DB_ID,
            title=title,
            date=date,
            description=description if description else None
        )
        
        page_url = result.get("url", "N/A")
        return f"✅ Calendar event '{title}' created successfully!\nURL: {page_url}"
    
    except Exception as e:
        return f"❌ Failed to create calendar event: {str(e)}"


@mcp.tool()
def add_list_item(
    title: str,
    status: str = "Not Started",
    priority: str = "Medium",
    description: str = ""
) -> str:
    """
    Add a new item to the Notion list database.
    
    Args:
        title: Task/item title
        status: Task status (e.g., "Not Started", "In Progress", "Done")
        priority: Task priority (e.g., "High", "Medium", "Low")
        description: Optional item description
    
    Returns:
        Success message with the created page URL
    """
    if not NOTION_LIST_DB_ID:
        return "Error: NOTION_LIST_DB_ID environment variable is not set"
    
    try:
        result = create_list_page(
            client=notion,
            database_id=NOTION_LIST_DB_ID,
            title=title,
            status=status if status else None,
            priority=priority if priority else None,
            description=description if description else None
        )
        
        page_url = result.get("url", "N/A")
        return f"✅ List item '{title}' created successfully!\nURL: {page_url}"
    
    except Exception as e:
        return f"❌ Failed to create list item: {str(e)}"


def main():
    """Run the MCP server."""
    # Run the server with STDIO transport (for Claude Desktop integration)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
