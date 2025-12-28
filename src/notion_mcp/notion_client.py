"""Notion API client helpers for creating pages in databases."""

from datetime import datetime
from typing import Any, Dict, Optional
from notion_client import Client


def create_calendar_page(
    client: Client,
    database_id: str,
    title: str,
    date: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new page in the Notion calendar database.
    
    Args:
        client: Notion client instance
        database_id: Calendar database ID
        title: Event title
        date: Date in ISO format (YYYY-MM-DD) or ISO datetime
        description: Optional event description
    
    Returns:
        Created page data from Notion API
    """
    properties: Dict[str, Any] = {
        "이름": {
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "Date": {
            "date": {
                "start": date
            }
        }
    }
    
    # Add description if provided
    children = []
    if description:
        # Split description by newlines to create separate paragraph blocks
        for line in description.split("\n"):
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": line
                            }
                        }
                    ]
                }
            })
    
    page_data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    
    if children:
        page_data["children"] = children
    
    return client.pages.create(**page_data)


def create_list_page(
    client: Client,
    database_id: str,
    title: str,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new page in the Notion list database.
    
    Args:
        client: Notion client instance
        database_id: List database ID
        title: Task/item title
        status: Optional status (e.g., "Not Started", "In Progress", "Done")
        priority: Optional priority (e.g., "High", "Medium", "Low")
        description: Optional item description
    
    Returns:
        Created page data from Notion API
    """
    properties: Dict[str, Any] = {
        "이름": {
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": title
                    }
                }
            ]
        }
    }
    
    # Status and properties do not exist in the current database schema
    # Logic commented out to prevent API errors
    # if status:
    #     properties["Status"] = {
    #         "status": {
    #             "name": status
    #         }
    #     }
    
    # if priority:
    #     properties["Priority"] = {
    #         "select": {
    #             "name": priority
    #         }
    #     }
    
    # Add description as page content if provided
    children = []
    if description:
        # Split description by newlines to create separate paragraph blocks
        for line in description.split("\n"):
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": line
                            }
                        }
                    ]
                }
            })
    
    page_data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    
    if children:
        page_data["children"] = children
    
    return client.pages.create(**page_data)
