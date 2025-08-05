# scanapp/option_scan.py
import requests
import os
import json

def scan_options(symbols, query_date, expiration_date, delta_target, option_type="put", api_key=""):
    """
    Scan options for given symbols and return results, total premium, and collateral.

    Parameters:
    - symbols: list of symbol strings
    - query_date: YYYY-MM-DD string
    - expiration_date: YYYY-MM-DD string
    - delta_target: float (e.g., -0.20)
    - option_type: "put" or "call"
    - api_key: Alpha Vantage API key (optional). If empty, will read from environment.
    """
    # Get API key from env if not passed
    if not api_key:
        api_key = os.environ.get("ALPHA_VANTAGE_API_KEY", "")
        if not api_key:
            raise ValueError(
                "API key not provided and ALPHA_VANTAGE_API_KEY not found in environment."
            )

    summary_rows = []

    for symbol in symbols:
        print(f"\n--- {symbol} ---")
        url = (
            f"https://www.alphavantage.co/query?"
            f"function=HISTORICAL_OPTIONS&symbol={symbol}&date={query_date}"
            f"&entitlement=delayed&apikey={api_key}"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
            options_data = response.json()
            contracts = options_data.get("data", [])

            # Filter by expiration, type, delta, and bid/ask presence
            filtered_options = [
                option
                for option in contracts
                if option.get("expiration") == str(expiration_date)
                and option.get("type") == option_type
                and option.get("delta") is not None
                and float(option["delta"]) <= delta_target
                and option.get("bid") is not None
                and option.get("ask") is not None
            ]

            best_option = max(filtered_options, key=lambda o: float(o["delta"]), default=None)

            if best_option:
                bid = float(best_option["bid"])
                ask = float(best_option["ask"])
                strike = float(best_option["strike"])
                premium = round(((bid + ask) / 2) * 100, 2)

                summary_rows.append({
                    "Symbol": symbol,
                    "Strike": strike,
                    "Expiration": best_option["expiration"],
                    "Delta": best_option["delta"],
                    "Premium": premium,
                    "Error": ""
                })
            else:
                summary_rows.append({
                    "Symbol": symbol,
                    "Strike": 0,
                    "Expiration": "",
                    "Delta": "",
                    "Premium": 0,
                    "Error": "No matching option found"
                })

        except requests.exceptions.RequestException as e:
            summary_rows.append({
                "Symbol": symbol,
                "Strike": 0,
                "Expiration": "",
                "Delta": "",
                "Premium": 0,
                "Error": f"Request failed: {e}"
            })

    total_premium = round(sum(row["Premium"] for row in summary_rows), 2)
    total_collateral = round(sum(row["Strike"] for row in summary_rows) * 100, 2)

    return summary_rows, total_premium, total_collateral
