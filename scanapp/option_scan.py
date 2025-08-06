# scanapp/option_scan.py
import os
import requests

def _get_prev_close(symbol: str) -> float | None:
    """GLOBAL_QUOTE: previous close (15-min delayed context)."""
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY", "")
    if not api_key:
        raise ValueError("ALPHA_VANTAGE_API_KEY not found in environment.")
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&entitlement=delayed&apikey={api_key}"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        print(f"data {data}")
        quote = data.get("Global Quote - DATA DELAYED BY 15 MINUTES", {})
        prev_close_str = quote.get("05. price")
        return float(prev_close_str) if prev_close_str is not None else None
    except Exception:
        return None

def _get_daily_latest_close(symbol: str) -> float | None:
    """TIME_SERIES_DAILY: latest trading day close."""
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY", "")
    if not api_key:
        raise ValueError("ALPHA_VANTAGE_API_KEY not found in environment.")
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}"
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        ts = data.get("Time Series (Daily)")
        if not ts:
            return None
        latest_date = next(iter(ts))  # first key is latest trading day
        close_str = ts[latest_date].get("4. close")
        return float(close_str) if close_str is not None else None
    except Exception:
        return None

def scan_options(symbols, query_date, expiration_date, delta_target, option_type):
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY", "")
    if not api_key:
        raise ValueError("ALPHA_VANTAGE_API_KEY not found in environment.")

    summary_rows = []

    for symbol in symbols:
        # --- quotes
        prev_close = _get_prev_close(symbol)            # from GLOBAL_QUOTE (15m delayed context)
        daily_close = _get_daily_latest_close(symbol)   # from TIME_SERIES_DAILY (latest daily close)

        # --- options (HISTORICAL_OPTIONS)
        opt_url = (
            f"https://www.alphavantage.co/query?"
            f"function=HISTORICAL_OPTIONS&symbol={symbol}&date={query_date}"
            f"&entitlement=delayed&apikey={api_key}"
        )

        try:
            resp = requests.get(opt_url, timeout=20)
            resp.raise_for_status()
            options_data = resp.json()
            contracts = options_data.get("data", [])

            filtered = [
                o for o in contracts
                if o.get("expiration") == str(expiration_date)
                and o.get("type") == option_type
                and o.get("delta") is not None
                and float(o["delta"]) <= float(delta_target)
                and o.get("bid") is not None
                and o.get("ask") is not None
            ]

            best = max(filtered, key=lambda o: float(o["delta"]), default=None)

            if best:
                bid = float(best["bid"])
                ask = float(best["ask"])
                strike = float(best["strike"])
                premium = round(((bid + ask) / 2) * 100, 2)
                collateral = round(strike * 100, 2)

                summary_rows.append({
                    "Symbol": symbol,
                    "Strike": strike,
                    "PrevClose": prev_close,      # from GLOBAL_QUOTE
                    "DailyClose": daily_close,    # from TIME_SERIES_DAILY
                    "Expiration": best["expiration"],
                    "Delta": best["delta"],
                    "Premium": premium,
                    "Collateral": collateral,
                })
            else:
                summary_rows.append({
                    "Symbol": symbol,
                    "Strike": 0.0,
                    "PrevClose": prev_close,
                    "DailyClose": daily_close,
                    "Expiration": "",
                    "Delta": "",
                    "Premium": 0.0,
                    "Collateral": 0.0,
                })

        except requests.exceptions.RequestException:
            summary_rows.append({
                "Symbol": symbol,
                "Strike": 0.0,
                "PrevClose": prev_close,
                "DailyClose": daily_close,
                "Expiration": "",
                "Delta": "",
                "Premium": 0.0,
                "Collateral": 0.0,
            })

    total_premium = round(sum(row["Premium"] for row in summary_rows), 2)
    total_collateral = round(sum(row["Strike"] for row in summary_rows) * 100, 2)
    return summary_rows, total_premium, total_collateral


