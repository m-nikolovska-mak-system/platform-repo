#!/usr/bin/env python3
"""
Update Confluence Database with workflow documentation links.
"""
import requests
import json
import sys
import os

# Environment variables
CONFLUENCE_BASE = os.getenv("CONFLUENCE_BASE")
CONFLUENCE_USER = os.getenv("CONFLUENCE_USER")
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
DB_PAGE_ID = os.getenv("CONFLUENCE_DB_PAGE_ID")


def validate_environment():
    """Check all required environment variables are set."""
    missing = []
    if not CONFLUENCE_BASE:
        missing.append("CONFLUENCE_BASE")
    if not CONFLUENCE_USER:
        missing.append("CONFLUENCE_USER")
    if not CONFLUENCE_TOKEN:
        missing.append("CONFLUENCE_API_TOKEN")
    if not DB_PAGE_ID:
        missing.append("CONFLUENCE_DB_PAGE_ID")
    
    if missing:
        print(f"❌ Error: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)


def get_database_definition():
    """Fetch database field definitions from Confluence."""
    url = f"{CONFLUENCE_BASE}/api/v2/pages/{DB_PAGE_ID}"
    
    try:
        print(f"🔍 Fetching database definition from: {url}")
        res = requests.get(url, auth=(CONFLUENCE_USER, CONFLUENCE_TOKEN), timeout=30)
        res.raise_for_status()
        
        db = res.json().get("database", {})
        fields = db.get("fields", [])
        
        if not fields:
            print("⚠️  Warning: No database fields found. Make sure this is a database page.")
        
        return fields
    
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error fetching database definition: {e}")
        print(f"Response: {e.response.text if e.response else 'No response'}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        sys.exit(1)


def get_database_rows():
    """Fetch all rows from the database."""
    url = f"{CONFLUENCE_BASE}/api/v2/pages/{DB_PAGE_ID}/database/rows"
    
    try:
        print(f"📋 Fetching database rows from: {url}")
        res = requests.get(url, auth=(CONFLUENCE_USER, CONFLUENCE_TOKEN), timeout=30)
        res.raise_for_status()
        
        rows = res.json().get("results", [])
        print(f"✅ Found {len(rows)} existing rows")
        return rows
    
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error fetching rows: {e}")
        print(f"Response: {e.response.text if e.response else 'No response'}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        sys.exit(1)


def add_or_update_row(workflow_name, readme_page_id):
    """Add or update a row in the Confluence database."""
    
    # Validate page ID
    if not readme_page_id or readme_page_id == "null":
        print(f"❌ Error: Invalid page ID '{readme_page_id}' for workflow '{workflow_name}'")
        sys.exit(1)
    
    print(f"\n📝 Processing: {workflow_name} -> Page ID: {readme_page_id}")
    
    # Get field definitions
    fields = get_database_definition()
    
    # Find the field IDs for our columns
    workflow_field = None
    readme_field = None
    
    for f in fields:
        print(f"  - Found field: '{f.get('name')}' (ID: {f.get('id')})")
        if f.get("name") == "Workflow Name":
            workflow_field = f.get("id")
        elif f.get("name") == "README Page":
            readme_field = f.get("id")
    
    if not workflow_field or not readme_field:
        print(f"❌ Error: Required database columns not found!")
        print(f"   - 'Workflow Name' field: {'✅ Found' if workflow_field else '❌ Missing'}")
        print(f"   - 'README Page' field: {'✅ Found' if readme_field else '❌ Missing'}")
        print(f"\n💡 Make sure your Confluence database has columns named exactly:")
        print(f"   1. 'Workflow Name' (Text type)")
        print(f"   2. 'README Page' (Page type)")
        sys.exit(1)
    
    print(f"✅ Field IDs found: Workflow={workflow_field}, README={readme_field}")
    
    # Get existing rows
    rows = get_database_rows()
    
    # ----- UPDATE if row exists -----
    for row in rows:
        props = row.get("properties", {})
        existing_name = props.get(workflow_field, {}).get("value")
        
        if existing_name == workflow_name:
            row_id = row["id"]
            url = f"{CONFLUENCE_BASE}/api/v2/database/rows/{row_id}"
            
            payload = {
                "properties": {
                    workflow_field: {"value": workflow_name},
                    readme_field: {"value": [{"id": readme_page_id}]}
                }
            }
            
            try:
                print(f"🔄 Updating existing row (ID: {row_id})...")
                res = requests.put(
                    url, 
                    auth=(CONFLUENCE_USER, CONFLUENCE_TOKEN), 
                    json=payload,
                    timeout=30
                )
                res.raise_for_status()
                print(f"✅ Updated existing row for '{workflow_name}'")
                return
            
            except requests.exceptions.HTTPError as e:
                print(f"❌ HTTP Error updating row: {e}")
                print(f"Response: {e.response.text if e.response else 'No response'}")
                sys.exit(1)
            except requests.exceptions.RequestException as e:
                print(f"❌ Network error: {e}")
                sys.exit(1)
    
    # ----- INSERT new row if not found -----
    url = f"{CONFLUENCE_BASE}/api/v2/pages/{DB_PAGE_ID}/database/rows"
    
    payload = {
        "properties": {
            workflow_field: {"value": workflow_name},
            readme_field: {"value": [{"id": readme_page_id}]}
        }
    }
    
    try:
        print(f"➕ Creating new row for '{workflow_name}'...")
        res = requests.post(
            url, 
            auth=(CONFLUENCE_USER, CONFLUENCE_TOKEN), 
            json=payload,
            timeout=30
        )
        res.raise_for_status()
        print(f"✅ Inserted new row for '{workflow_name}'")
    
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error creating row: {e}")
        print(f"Response: {e.response.text if e.response else 'No response'}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Confluence Database Updater")
    print("=" * 60)
    
    # Validate arguments
    if len(sys.argv) != 3:
        print(f"❌ Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        print(f"Usage: {sys.argv[0]} <workflow_name> <readme_page_id>")
        sys.exit(1)
    
    workflow_name = sys.argv[1]
    readme_page_id = sys.argv[2]
    
    # Validate environment
    validate_environment()
    
    # Process the update
    add_or_update_row(workflow_name, readme_page_id)
    
    print("\n" + "=" * 60)
    print("✅ Script completed successfully!")
    print("=" * 60)
