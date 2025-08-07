# scanapp/common.py

import os

def get_alpha_vantage_api_key() -> str:
    """Get Alpha Vantage API key from environment or raise an error."""
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY", "")
    if not api_key:
        raise ValueError("ALPHA_VANTAGE_API_KEY not found in environment.")
    return api_key
