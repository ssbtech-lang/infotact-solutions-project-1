# import requests

# API_KEY = "3028551a2fd5c87440a51801"

# def get_exchange_rate(from_currency, to_currency, api_key=API_KEY):
#     url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         if 'conversion_rates' in data and to_currency in data['conversion_rates']:
#             return data['conversion_rates'][to_currency]
#         else:
#             raise ValueError(f"Exchange rate not found for {from_currency} to {to_currency}.")
#     except requests.exceptions.RequestException as e:
#         raise ValueError(f"Error fetching exchange rates: {str(e)}")

# def convert_currency(amount, from_currency, to_currency, api_key=API_KEY):
#     rate = get_exchange_rate(from_currency, to_currency, api_key)
#     return round(amount * rate, 2)

# def get_all_currencies(api_key=API_KEY):
#     url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         if 'supported_codes' in data:
#             return {code[0]: code[1] for code in data['supported_codes']}
#         else:
#             raise ValueError("Error fetching currencies.")
#     except requests.exceptions.RequestException as e:
#         raise ValueError(f"Error fetching currency codes: {str(e)}")






import requests
import yfinance as yf
import matplotlib.pyplot as plt

API_KEY = "3028551a2fd5c87440a51801"

def get_exchange_rate(from_currency, to_currency, api_key=API_KEY):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'conversion_rates' in data and to_currency in data['conversion_rates']:
            return data['conversion_rates'][to_currency]
        else:
            raise ValueError(f"Exchange rate not found for {from_currency} to {to_currency}.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching exchange rates: {str(e)}")

def convert_currency(amount, from_currency, to_currency, api_key=API_KEY):
    rate = get_exchange_rate(from_currency, to_currency, api_key)
    return round(amount * rate, 2)

def get_all_currencies(api_key=API_KEY):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'supported_codes' in data:
            return {code[0]: code[1] for code in data['supported_codes']}
        else:
            raise ValueError("Error fetching currencies.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching currency codes: {str(e)}")

def visualize_exchange_rates(from_currency, to_currency):
    ticker = yf.Ticker(f"{from_currency}{to_currency}=X")
    data = ticker.history(period='1y')
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Close'], label=f"{from_currency}/{to_currency}")
    plt.xlabel('Date')
    plt.ylabel('Exchange Rate')
    plt.title('Exchange Rates')
    plt.legend()
    plt.show()




