# import streamlit as st
# import mysql.connector
# from datetime import datetime
# import re
# from converter import convert_currency, get_all_currencies

# # Database connection function
# def create_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="Davps@2011",
#         database="currencywizard",
#         port=3307
#     )

# # Utility functions for email and password validation
# def is_valid_email(email):
#     email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     return re.match(email_pattern, email) is not None

# def is_valid_password(password):
#     if len(password) < 8:
#         return False
#     if not re.search(r"[A-Z]", password):
#         return False
#     if not re.search(r"[a-z]", password):
#         return False
#     if not re.search(r"\d", password):
#         return False
#     if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
#         return False
#     return True

# # Login and registration functions
# def login_user(username, password):
#     conn = create_connection()
#     cursor = conn.cursor(dictionary=True)
#     try:
#         cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
#         user = cursor.fetchone()
#         if user:
#             cursor.execute("UPDATE users SET last_login = %s WHERE user_id = %s", (datetime.now(), user['user_id']))
#             conn.commit()
#             return user
#         return None
#     finally:
#         cursor.close()
#         conn.close()

# def register_user(username, email, password, full_name):
#     if not is_valid_password(password):
#         return False, "Password must meet the requirements."
    
#     conn = create_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute("INSERT INTO users (username, email, password, full_name) VALUES (%s, %s, %s, %s)", 
#                        (username, email, password, full_name))
#         conn.commit()
#         return True, "Registration successful!"
#     except mysql.connector.Error as err:
#         if err.errno == 1062:  # Duplicate entry
#             return False, "Username or email already exists."
#         return False, f"An error occurred: {str(err)}"
#     finally:
#         cursor.close()
#         conn.close()

# # Currency converter application
# def currency_converter_app():
#     st.title("Currency Converter")
    
#     try:
#         currencies = get_all_currencies()
#         currency_list = [f"{code} - {name}" for code, name in currencies.items()]
#     except Exception as e:
#         st.error(f"Failed to fetch currencies: {str(e)}")
#         return

#     # Function to extract the currency code from the dropdown selection
#     def extract_code(selection):
#         return selection.split(" - ")[0]

#     amount = st.number_input("Enter Amount", min_value=0.0, step=0.01)
#     from_currency = st.selectbox("From Currency", options=currency_list)
#     to_currency = st.selectbox("To Currency", options=currency_list)

#     if st.button("Convert"):
#         try:
#             from_currency_code = extract_code(from_currency)
#             to_currency_code = extract_code(to_currency)
#             result = convert_currency(amount, from_currency_code, to_currency_code)
#             st.success(f"Converted Amount: {result:.2f} {to_currency_code}")
#         except Exception as e:
#             st.error(str(e))

# # Main Streamlit application
# def main():
#     st.set_page_config(page_title="CurrencyWizard", page_icon="💱", layout="centered")

#     # Manage navigation between login and converter pages
#     if 'page' not in st.session_state:
#         st.session_state['page'] = 'login'

#     if 'user' in st.session_state and st.session_state['page'] == 'converter':
#         currency_converter_app()  # Navigate to the currency converter app
#         return

#     # Login/Sign-up page
#     st.title("🌍 CurrencyWizard")
#     st.markdown("##### Your Ultimate Currency Conversion Companion")

#     tab1, tab2 = st.tabs(["Login", "Sign Up"])

#     # Login tab
#     with tab1:
#         st.markdown("### Login to Your Account")
#         with st.form("login_form"):
#             login_username = st.text_input("Username")
#             login_password = st.text_input("Password", type="password")
#             login_button = st.form_submit_button("Login")
        
#         if login_button:
#             if not login_username or not login_password:
#                 st.error("Please fill in all fields.")
#             else:
#                 user = login_user(login_username, login_password)
#                 if user:
#                     st.success(f"Welcome, {user['full_name']}!")
#                     st.session_state['user'] = user
#                     st.session_state['page'] = 'converter'
#                     st.experimental_rerun()
#                 else:
#                     st.error("Invalid username or password.")

#     # Sign-up tab
#     with tab2:
#         st.markdown("### Create a New Account")
#         with st.form("register_form"):
#             reg_username = st.text_input("Username")
#             reg_email = st.text_input("Email")
#             reg_full_name = st.text_input("Full Name")
#             reg_password = st.text_input("Password", type="password")
#             reg_confirm_password = st.text_input("Confirm Password", type="password")
#             register_button = st.form_submit_button("Sign Up")
        
#         if register_button:
#             if not all([reg_username, reg_email, reg_full_name, reg_password, reg_confirm_password]):
#                 st.error("Please fill in all fields.")
#             elif reg_password != reg_confirm_password:
#                 st.error("Passwords do not match.")
#             else:
#                 success, message = register_user(reg_username, reg_email, reg_password, reg_full_name)
#                 if success:
#                     st.success(message)
#                     st.info("You can now log in.")
#                 else:
#                     st.error(message)

# if __name__ == "__main__":
#     main()







import streamlit as st
import mysql.connector
from datetime import datetime
import re
import yfinance as yf
from converter import convert_currency, get_all_currencies

# Database connection function
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Davps@2011",
        database="currencywizard",
        port=3307
    )

# Utility functions for email and password validation
def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# Login and registration functions
def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            cursor.execute("UPDATE users SET last_login = %s WHERE user_id = %s", (datetime.now(), user['user_id']))
            conn.commit()
            return user
        return None
    finally:
        cursor.close()
        conn.close()

def register_user(username, email, password, full_name):
    if not is_valid_password(password):
        return False, "Password must meet the requirements."
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password, full_name) VALUES (%s, %s, %s, %s)", (username, email, password, full_name))
        conn.commit()
        return True, "Registration successful!"
    except mysql.connector.Error as err:
        if err.errno == 1062:  # Duplicate entry
            return False, "Username or email already exists."
        return False, f"An error occurred: {str(err)}"
    finally:
        cursor.close()
        conn.close()

# Currency converter application
def currency_converter_app():
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
    if st.button("Visualize"):
        try:
            from_currency_code = extract_code(from_currency)
            to_currency_code = extract_code(to_currency)
            ticker = yf.Ticker(f"{from_currency_code}{to_currency_code}=X")
            data = ticker.history(period="1y")
            st.line_chart(data['Close'])
        except Exception as e:
            st.error(str(e))

# Main Streamlit application
def main():
    st.set_page_config(page_title="CurrencyWizard", page_icon="💱", layout="centered")
    # Manage navigation between login and converter pages
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if 'user' in st.session_state and st.session_state['page'] == 'converter':
        currency_converter_app()
        # Navigate to the currency converter app
        return

    # Login/Sign-up page
    st.title("🌍 CurrencyWizard")
    st.markdown("##### Your Ultimate Currency Conversion Companion")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # Login tab
    with tab1:
        st.markdown("### Login to Your Account")
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

        if login_button:
            if not login_username or not login_password:
                st.error("Please fill in all fields.")
            else:
                user = login_user(login_username, login_password)
                if user:
                    st.success(f"Welcome, {user['full_name']}!")
                    st.session_state['user'] = user
                    st.session_state['page'] = 'converter'
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password.")

    # Sign-up tab
    with tab2:
        st.markdown("### Create a New Account")
        with st.form("register_form"):
            reg_username = st.text_input("Username")
            reg_email = st.text_input("Email")
            reg_full_name = st.text_input("Full Name")
            reg_password = st.text_input("Password", type="password")
            reg_confirm_password = st.text_input("Confirm Password", type="password")
            register_button = st.form_submit_button("Sign Up")

        if register_button:
            if not all([reg_username, reg_email, reg_full_name, reg_password, reg_confirm_password]):
                st.error("Please fill in all fields.")
            elif reg_password != reg_confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = register_user(reg_username, reg_email, reg_password, reg_full_name)
                if success:
                    st.success(message)
                    st.info("You can now log in.")
                else:
                    st.error(message)

if __name__ == "__main__":
    main()






