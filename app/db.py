"""
Module: db.py
Author: [Your Name]
Purpose: Database connectivity via HBO-ICT.cloud REST API

Description:
This module contains database query execution function that communicates via
HTTP requests with the HBO-ICT.cloud API. All queries (SELECT, INSERT, UPDATE)
go through this function.

Dependencies:
  - requests (HTTP library)
  - Flask current_app (config access)
  - HBO-ICT.cloud API (external service)

Configuration (from Flask app config):
  - API_URL: Base URL of HBO-ICT.cloud API
  - API_KEY: Authorization bearer token
  - DATABASE: Database name/identifier
"""

import requests
from flask import current_app 


def execute_query(query, values=None):
    """
    Execute SQL query via HBO-ICT.cloud API.
    
    Function: Wrapper to execute remote database queries to
    external HBO-ICT.cloud REST API.
    
    Parameters:
      query (str): SQL query string
                   May contain parameter placeholders: ?
                   Example: "SELECT * FROM leerling WHERE id = ?"
      
      values (tuple|list|None): Query parameter values
                                Optional, default=None
                                Example: (1, 2, 3) for ? placeholders
    
    Return:
      - JSON response from API server (dict or list)
      - Depends on query type:
        * SELECT: Returns list of dict rows
        * INSERT/UPDATE/DELETE: Returns status/result dict
    
    Raises:
      - requests.Timeout: If API doesn't respond within 10 seconds
      - requests.ConnectionError: If API is unreachable
      - json.JSONDecodeError: If API doesn't return valid JSON
    
    Flow:
      1. Get API credentials from Flask current_app.config
      2. Build HTTP request body with query + values + database
      3. POST request to API with Authorization header
      4. Parse JSON response
      5. Return data to caller
    
    Example usage:
      >>> leerlingen = execute_query("SELECT * FROM leerling")
      >>> [{"id": 1, "naam": "Jan", "klas": "6A"}, ...]
      
      >>> # With parameters:
      >>> docent = execute_query(
      ...     "SELECT * FROM docent WHERE username = ?",
      ...     ("jdoe",)
      ... )
      >>> [{"id": 1, "username": "jdoe", ...}]
      
      >>> # Insert:
      >>> execute_query(
      ...     "INSERT INTO leerling (naam, klas) VALUES (?, ?)",
      ...     ("Anne", "6B")
      ... )
    
    Security notes:
      - Query parameters via 'values' parameter (prevents SQL injection)
      - API key stored in Flask config (never hardcoded)
      - HTTPS via requests library (secure transport)
      - 10 second timeout prevents hanging requests
    
    Performance:
      - Network latency ~100-500ms typical for HBO-ICT.cloud
      - Parallel queries not supported (sync/blocking API)
    """
    # === STEP 1: Get API credentials from Flask config ===
    url = current_app.config["API_URL"]
    url += "/db"
    api_key = current_app.config["API_KEY"]
    database = current_app.config["DATABASE"]

    # === STEP 2: Make HTTP POST request ===
    x = requests.post(
        url=url,
        # Request body with query, parameters, database
        json={
            "query": query,
            "values": values,
            "database": database
        },
        # Authorization header with API key
        headers={"Authorization": f"Bearer {api_key}"},
        # Timeout prevent hanging requests
        timeout=10,
    )
    
    # === STEP 3: Parse and return JSON response ===
    return x.json()

 
