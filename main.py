import requests

API_URL = "https://api.frankfurter.app/latest"  # no API key needed

def convert(amount, from_code, to_code):
    params = {"amount": amount, "from": from_code, "to": to_code}
    r = requests.get(API_URL, params=params, timeout=10)
    r.raise_for_status()  # raises for 4xx/5xx
    data = r.json()
    if to_code not in data.get("rates", {}):
        raise ValueError("Unsupported currency code.")
    return data["rates"][to_code], data.get("date")

def main():
    # amount
    amt_raw = input("Amount: ").strip()
    try:
        amount = float(amt_raw)
        if amount < 0:
            print("Amount must be non-negative.")
            return
    except ValueError:
        print("Invalid amount. Use a number like 10.50")
        return

    from_code = input("From currency (e.g., USD): ").strip().upper()
    to_code   = input("To currency (e.g., EUR): ").strip().upper()

    try:
        converted, date = convert(amount, from_code, to_code)
        print(f"\n{amount} {from_code} -> {converted:.4f} {to_code} (rate date: {date})")
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code in (400, 422):
            print("Invalid currency code. Use ISO codes like USD, EUR, NGN.")
        else:
            print(f"HTTP error: {e}")
    except requests.exceptions.RequestException:
        print("Network error. Check your internet connection.")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
