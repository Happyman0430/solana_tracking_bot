# import tkinter as tk
# from tkinter import messagebox
# import requests

# # Function to fetch data from the API
# def fetch_data():
#     token_address = token_entry.get()
#     if not token_address:
#         messagebox.showerror("Error", "Please enter a token address!")
#         return
    
#     url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
#     try:
#         response = requests.get(url)
#         data = response.json()
#         # Extract the first pair's data
#         pair = data.get("pairs", [{}])[0]
#         if not pair:
#             messagebox.showerror("Error", "No data found for this token!")
#             return
        
#         # Update GUI with API data
#         marketcap_now_var.set(pair["marketCap"])
#         liquidity_now_var.set(pair["liquidity"]["usd"])
#         volume_now_var.set(pair["volume"]["m5"])
#         buy_volume_var.set(pair["txns"]["m5"]["buys"])
#         sell_volume_var.set(pair["txns"]["m5"]["sells"])
#         trxs_difference_var.set(pair["txns"]["m5"]["buys"]/pair["txns"]["m5"]["sells"])

#     except Exception as e:
#         messagebox.showerror("Error", f"An error occurred: {e}")

# # Create main window
# root = tk.Tk()
# root.title("Token Data Viewer")
# root.geometry("600x400")

# # Token input form
# tk.Label(root, text="Input Token:").grid(row=1, column=0, pady=10 )
# token_entry = tk.Entry(root, width=40)
# token_entry.grid(row=1, column=1, pady=10)
# run_button = tk.Button(root, text="Run", command=fetch_data)
# run_button.grid(row=1, column=2, padx=10)

# # Labels and fields for displaying data
# tk.Label(root, text="Marketcap ATH").grid(row=2, column=0, padx=10, pady=10)
# marketcap_ATH_var = tk.StringVar()
# tk.Entry(root, textvariable=marketcap_ATH_var, state="readonly").grid(row=3, column=0, pady=10)

# tk.Label(root, text="Liquidity ATH").grid(row=2, column=1, padx=10, pady=10)
# Liquidity_ATH_var = tk.StringVar()
# tk.Entry(root, textvariable=Liquidity_ATH_var, state="readonly").grid(row=3, column=1, pady=10)

# tk.Label(root, text="5 minutes volume ATH").grid(row=2, column=2, padx=10, pady=10)
# min_volume_ATH_var = tk.StringVar()
# tk.Entry(root, textvariable=min_volume_ATH_var, state="readonly").grid(row=3, column=2, pady=10)

# tk.Label(root, text="Marketcap Now").grid(row=4, column=0, padx=10, pady=10)
# marketcap_now_var = tk.StringVar()
# tk.Entry(root, textvariable=marketcap_now_var, state="readonly").grid(row=5, column=0, pady=10)

# tk.Label(root, text="Liquidity Now").grid(row=4, column=1, padx=10, pady=10)
# liquidity_now_var = tk.StringVar()
# tk.Entry(root, textvariable=liquidity_now_var, state="readonly").grid(row=5, column=1, pady=10)

# tk.Label(root, text="5 Minutes Volume Now").grid(row=4, column=2, padx=10, pady=10)
# volume_now_var = tk.StringVar()
# tk.Entry(root, textvariable=volume_now_var, state="readonly").grid(row=5, column=2, pady=10)

# tk.Label(root, text="Difference %").grid(row=6, column=0, padx=10, pady=10)
# marketcap_difference_var = tk.StringVar()
# tk.Entry(root, textvariable=marketcap_difference_var, state="readonly").grid(row=7, column=0, pady=10)

# tk.Label(root, text="Difference %").grid(row=6, column=1, padx=10, pady=10)
# liquidity_difference_var = tk.StringVar()
# tk.Entry(root, textvariable=liquidity_difference_var, state="readonly").grid(row=7, column=1, pady=10)

# tk.Label(root, text="Difference %").grid(row=6, column=2, padx=10, pady=10)
# volume_difference_var = tk.StringVar()
# tk.Entry(root, textvariable=volume_difference_var, state="readonly").grid(row=7, column=2, pady=10)

# tk.Label(root, text="5 Minutes Buy Volume").grid(row=8, column=0, padx=10, pady=10)
# buy_volume_var = tk.StringVar()
# tk.Entry(root, textvariable=buy_volume_var, state="readonly").grid(row=9, column=0, pady=10)

# tk.Label(root, text="5 Minutes Sell Volume").grid(row=8, column=1, padx=10, pady=10)
# sell_volume_var = tk.StringVar()
# tk.Entry(root, textvariable=sell_volume_var, state="readonly").grid(row=9, column=1, pady=10)

# tk.Label(root, text="Difference %").grid(row=10, column=0, pady=10)
# trxs_difference_var = tk.StringVar()
# tk.Entry(root, textvariable=trxs_difference_var, state="readonly").grid(row=11, column=0, pady=10)
# # Run the main loop
# root.mainloop()




import tkinter as tk
from tkinter import messagebox
import requests
import re
from CloudflareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage, ChromiumOptions
from selenium.webdriver.common.by import By
import time


def parse_numeric_value(value_str):
    # Regular expression to capture the number and optional suffix
    match = re.match(r"^\$?([\d,.]+)([MK]?)$", value_str.strip())
    if not match:
        raise ValueError(f"Invalid input format: {value_str}")
    
    # Extract number and suffix
    number, suffix = match.groups()
    number = float(number.replace(',', ''))
    
    # Handle suffix
    if suffix == 'M':  # Millions
        number *= 1_000_000
    elif suffix == 'K':  # Thousands
        number *= 1_000
    
    return number


def find_max(arr):
    max_value = arr[0]
    for num in arr:
        if num > max_value:
            max_value = num
    return max_value
# Function to fetch data from the API
def fetch_data():
    token_address = token_entry.get()
    if not token_address:
        messagebox.showerror("Error", "Please enter a token address!")
        return
    
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    try:
         response = requests.get(url)
         data = response.json()
         # Extract the first pair's data
         pair = data.get("pairs", [{}])[0]
         if not pair:
             messagebox.showerror("Error", "No data found for this token!")
             return
         
         
         website_url = pair["url"]
         browser_path = "/usr/bin/google-chrome"
         options = ChromiumOptions()
         options.set_paths(browser_path=browser_path)
         arguments = [
             
             "-no-first-run", "-force-color-profile=srgb", "-metrics-recording-only",
             "-password-store=basic", "-use-mock-keychain", "-export-tagged-pdf",
             "-no-default-browser-check", "-disable-background-mode",
             "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
             "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
             "-deny-permission-prompts", "-disable-gpu", "-accept-lang=en-US",]
         
         for argument in arguments:
             options.set_argument(argument)
         driver = ChromiumPage(addr_or_opts=options)
         driver.get(website_url)
         cf_bypasser = CloudflareBypasser(driver)
         cf_bypasser.bypass()
         
        #  click the 5 minutes
         button = driver.ele('css:.chakra-tabs__tab.custom-1rlow8l:nth-of-type(1)', timeout=10)
         print(button.text)
         time.sleep(1)
         button.click()
         time.sleep(4)
            
         
         # Select all elements with the specified class
         elements1 = driver.eles('css:.chakra-stack.custom-gh4bym')
         elements2 = driver.eles('css:chakra-stack custom-1vsnzom')
         # Ensure there are at least two elements, then get the text of the second one
         if len(elements1) >= 2:
             text1 = elements1[1].ele('css:span:nth-of-type(2)', timeout=10).text
             print(f"Text of the second element: {text1}")
             buy_volume_var.set(text1)
         else:
             print("Less than two elements found with the specified class.")
         if len(elements2) >= 2:
             text2 = elements2[1].ele('css:span:nth-of-type(2)', timeout=10).text
             sell_volume_var.set(text2)
             print(f"Text of the second element: {text2}")
         else:
             print("Less than two elements found with the specified class.")
         
         driver.quit()
         
         
         # Update GUI with API data
         marketcap_now_var.set(pair["marketCap"])
         liquidity_now_var.set(pair["liquidity"]["usd"])
         volume_now_var.set(pair["volume"]["m5"])
         
       
         # buy_volume_var.set(pair["txns"]["m5"]["buys"])
         # sell_volume_var.set(pair["txns"]["m5"]["sells"])
         trxs_difference_var.set(parse_numeric_value(text1)/parse_numeric_value(text2))
         
        #  marketcapATH = [] 
        #  liquidityATH = [] 
        #  volume5ATH = []   
        #  duration=60
        #  while(duration):
        #     response = requests.get(url)
           
        #     if response.status_code == 200:  # Ensure the response is successful
        #        data = response.json()
        #        pair = data.get("pairs", [{}])[0]  # Get the first pair or an empty dic
        #  # Append data to lists
        #        marketcapATH.append(pair.get("marketCap", 0))  # Default to 0 if key is missing
        #        liquidityATH.append(pair.get("liquidity", {}).get("usd", 0))
        #        volume5ATH.append(pair.get("volume", {}).get("m5", 0))
               
        #        marketcap_ATH_var = find_max(marketcapATH)
        #        Liquidity_ATH_var = find_max(liquidityATH)
        #        min_volume_ATH_var = find_max(volume5ATH)
        #        duration= -15
               
        #     else:
        #        print("Failed to fetch data:", response.status_code)
        #        break  # Exit loop on failure

    except Exception as e:
        messagebox.showerror("Error", "There is no change of data. please click run button again")

# Create main window
root = tk.Tk()
root.title("Token Data Viewer")
root.geometry("600x400")

# Token input form
tk.Label(root, text="Input Token:").grid(row=1, column=0, pady=10 )
token_entry = tk.Entry(root, width=40)
token_entry.grid(row=1, column=1, pady=10)
run_button = tk.Button(root, text="Run", command=fetch_data)
run_button.grid(row=1, column=2, padx=10)

# Labels and fields for displaying data
tk.Label(root, text="Marketcap ATH").grid(row=2, column=0, padx=10, pady=10)
marketcap_ATH_var = tk.StringVar()
tk.Entry(root, textvariable=marketcap_ATH_var, state="readonly").grid(row=3, column=0, pady=10)

tk.Label(root, text="Liquidity ATH").grid(row=2, column=1, padx=10, pady=10)
Liquidity_ATH_var = tk.StringVar()
tk.Entry(root, textvariable=Liquidity_ATH_var, state="readonly").grid(row=3, column=1, pady=10)

tk.Label(root, text="5 minutes volume ATH").grid(row=2, column=2, padx=10, pady=10)
min_volume_ATH_var = tk.StringVar()
tk.Entry(root, textvariable=min_volume_ATH_var, state="readonly").grid(row=3, column=2, pady=10)

tk.Label(root, text="Marketcap Now").grid(row=4, column=0, padx=10, pady=10)
marketcap_now_var = tk.StringVar()
tk.Entry(root, textvariable=marketcap_now_var, state="readonly").grid(row=5, column=0, pady=10)

tk.Label(root, text="Liquidity Now").grid(row=4, column=1, padx=10, pady=10)
liquidity_now_var = tk.StringVar()
tk.Entry(root, textvariable=liquidity_now_var, state="readonly").grid(row=5, column=1, pady=10)

tk.Label(root, text="5 Minutes Volume Now").grid(row=4, column=2, padx=10, pady=10)
volume_now_var = tk.StringVar()
tk.Entry(root, textvariable=volume_now_var, state="readonly").grid(row=5, column=2, pady=10)

tk.Label(root, text="Difference %").grid(row=6, column=0, padx=10, pady=10)
marketcap_difference_var = tk.StringVar()
tk.Entry(root, textvariable=marketcap_difference_var, state="readonly").grid(row=7, column=0, pady=10)

tk.Label(root, text="Difference %").grid(row=6, column=1, padx=10, pady=10)
liquidity_difference_var = tk.StringVar()
tk.Entry(root, textvariable=liquidity_difference_var, state="readonly").grid(row=7, column=1, pady=10)

tk.Label(root, text="Difference %").grid(row=6, column=2, padx=10, pady=10)
volume_difference_var = tk.StringVar()
tk.Entry(root, textvariable=volume_difference_var, state="readonly").grid(row=7, column=2, pady=10)

tk.Label(root, text="5 Minutes Buy Volume").grid(row=8, column=0, padx=10, pady=10)
buy_volume_var = tk.StringVar()
tk.Entry(root, textvariable=buy_volume_var, state="readonly").grid(row=9, column=0, pady=10)

tk.Label(root, text="5 Minutes Sell Volume").grid(row=8, column=1, padx=10, pady=10)
sell_volume_var = tk.StringVar()
tk.Entry(root, textvariable=sell_volume_var, state="readonly").grid(row=9, column=1, pady=10)

tk.Label(root, text="Difference %").grid(row=10, column=0, pady=10)
trxs_difference_var = tk.StringVar()
tk.Entry(root, textvariable=trxs_difference_var, state="readonly").grid(row=11, column=0, pady=10)
# Run the main loop
root.mainloop()






