# import tkinter as tk
# from tkinter import ttk, messagebox
# from converter import convert_currency, get_all_currencies

# def run_tkinter_gui():
#     api_key = "3028551a2fd5c87440a51801"

#     # Fetch all currencies
#     try:
#         currencies = get_all_currencies(api_key)
#         currency_list = [f"{code} - {name}" for code, name in currencies.items()]
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to fetch currencies: {str(e)}")
#         return

#     # Function to extract the currency code from the dropdown selection
#     def extract_code(selection):
#         return selection.split(" - ")[0]

#     # Function to handle conversion
#     def convert():
#         try:
#             amount = float(amount_entry.get())
#             from_currency = extract_code(from_currency_var.get())
#             to_currency = extract_code(to_currency_var.get())
#             result = convert_currency(amount, from_currency, to_currency, api_key)
#             result_label.config(text=f"Converted Amount: {result:.2f} {to_currency}")
#         except Exception as e:
#             messagebox.showerror("Error", str(e))

#     # Tkinter window
#     window = tk.Tk()
#     window.title("Currency Converter")

#     tk.Label(window, text="Amount:").grid(row=0, column=0)
#     amount_entry = tk.Entry(window)
#     amount_entry.grid(row=0, column=1)

#     tk.Label(window, text="From Currency:").grid(row=1, column=0)
#     from_currency_var = tk.StringVar(value=currency_list[0])
#     from_currency_dropdown = ttk.Combobox(window, textvariable=from_currency_var, values=currency_list, state="readonly")
#     from_currency_dropdown.grid(row=1, column=1)

#     tk.Label(window, text="To Currency:").grid(row=2, column=0)
#     to_currency_var = tk.StringVar(value=currency_list[1])
#     to_currency_dropdown = ttk.Combobox(window, textvariable=to_currency_var, values=currency_list, state="readonly")
#     to_currency_dropdown.grid(row=2, column=1)

#     tk.Button(window, text="Convert", command=convert).grid(row=3, column=0, columnspan=2)

#     result_label = tk.Label(window, text="Converted Amount: ")
#     result_label.grid(row=4, column=0, columnspan=2)

#     window.mainloop()

# if __name__ == "__main__":
#     run_tkinter_gui()







import tkinter as tk
from tkinter import ttk, messagebox
from converter import convert_currency, get_all_currencies
import yfinance as yf
import matplotlib.pyplot as plt

def run_tkinter_gui():
    api_key = "3028551a2fd5c87440a51801"
    # Fetch all currencies
    try:
        currencies = get_all_currencies(api_key)
        currency_list = [f"{code} - {name}" for code, name in currencies.items()]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch currencies: {str(e)}")
        return

    # Function to extract the currency code from the dropdown selection
    def extract_code(selection):
        return selection.split(" - ")[0]

    # Function to handle conversion
    def convert():
        try:
            amount = float(amount_entry.get())
            from_currency = extract_code(from_currency_var.get())
            to_currency = extract_code(to_currency_var.get())
            result = convert_currency(amount, from_currency, to_currency, api_key)
            result_label.config(text=f"Converted Amount: {result:.2f} {to_currency}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Function to visualize historical exchange rates
    def visualize():
        try:
            from_currency = extract_code(from_currency_var.get())
            to_currency = extract_code(to_currency_var.get())
            ticker = yf.Ticker(f"{from_currency}{to_currency}=X")
            data = ticker.history(period="1y")
            plt.figure(figsize=(10, 6))
            plt.plot(data.index, data['Close'])
            plt.xlabel('Date')
            plt.ylabel('Exchange Rate')
            plt.title(f"Historical Exchange Rate: {from_currency}/{to_currency}")
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Tkinter window
    window = tk.Tk()
    window.title("Currency Converter")

    tk.Label(window, text="Amount:").grid(row=0, column=0)
    amount_entry = tk.Entry(window)
    amount_entry.grid(row=0, column=1)

    tk.Label(window, text="From Currency:").grid(row=1, column=0)
    from_currency_var = tk.StringVar(value=currency_list[0])
    from_currency_dropdown = ttk.Combobox(window, textvariable=from_currency_var, values=currency_list, state="readonly")
    from_currency_dropdown.grid(row=1, column=1)

    tk.Label(window, text="To Currency:").grid(row=2, column=0)
    to_currency_var = tk.StringVar(value=currency_list[1])
    to_currency_dropdown = ttk.Combobox(window, textvariable=to_currency_var, values=currency_list, state="readonly")
    to_currency_dropdown.grid(row=2, column=1)

    button_frame = tk.Frame(window)
    button_frame.grid(row=3, column=0, columnspan=2)

    tk.Button(button_frame, text="Convert", command=convert).pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(button_frame, text="Visualize", command=visualize).pack(side=tk.LEFT, fill=tk.X, expand=True)

    result_label = tk.Label(window, text="Converted Amount: ")
    result_label.grid(row=4, column=0, columnspan=2)

    window.mainloop()

if __name__ == "__main__":
    run_tkinter_gui()
