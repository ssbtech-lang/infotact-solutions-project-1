import streamlit as st
from converter import convert_currency, get_all_currencies

def streamlit_app():
    api_key = "3028551a2fd5c87440a51801"

    # Fetch all currencies
    try:
        currencies = get_all_currencies(api_key)
        currency_list = [f"{code} - {name}" for code, name in currencies.items()]
    except Exception as e:
        st.error(f"Failed to fetch currencies: {str(e)}")
        return

    # Function to extract the currency code from the dropdown selection
    def extract_code(selection):
        return selection.split(" - ")[0]

    st.title("Currency Converter")

    amount = st.number_input("Enter Amount", min_value=0.0, step=0.01)
    from_currency = st.selectbox("From Currency", options=currency_list)
    to_currency = st.selectbox("To Currency", options=currency_list)

    if st.button("Convert"):
        try:
            from_currency_code = extract_code(from_currency)
            to_currency_code = extract_code(to_currency)
            result = convert_currency(amount, from_currency_code, to_currency_code, api_key)
            st.success(f"Converted Amount: {result:.2f} {to_currency_code}")
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    streamlit_app()


