import tkinter as tk
from tkinter import ttk
import threading
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
import socket
import webbrowser

def open_browser():
    proxy_ip = entry_ip.get()
    proxy_port = entry_port.get()
    target_url = entry_url.get()

    message_label.config(text="Waiting, please wait...", fg="green")

    browser_thread = threading.Thread(target=open_browser_thread, args=(proxy_ip, proxy_port, target_url))
    browser_thread.start()

def open_browser_thread(proxy_ip, proxy_port, target_url):
    try:
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False, proxy={"server": f"{proxy_ip}:{proxy_port}"})
            context = browser.new_context()
            page = context.new_page()

            page.goto(target_url, timeout=60000)

            # Check if the page has loaded successfully
            if page.title():
                hide_message()
            else:
                raise Exception("Page did not load successfully")

            # Ignore initial browser and page closure
            while True:
                pass

    except Exception as e:
        print(f"Error {e}")
        show_error_message(e)

def hide_message():
    message_label.config(text="")

def show_error_message(error_message):
    message_label.config(text=f"Use another proxy. Error: {error_message}", fg="red")

def get_my_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    ip_data = response.json()
    my_ip = ip_data.get("ip")

    ip_label.config(text=f"Your Public IP: {my_ip}")

    root.after(5000, hide_ip_label)

def hide_ip_label():
    ip_label.config(text="")

def start_check():
    proxies = input_proxy.get("1.0", "end-1c").split("\n")
    total_proxies = len(proxies)
    completed_count = 0
    results_text.delete("1.0", "end")

    for proxy in proxies:
        ip, port = proxy.split(":")
        result = check_proxy(ip, port)
        if result:
            results_text.insert("end", f"{ip}:{port} working.\n", "green")
        else:
            results_text.insert("end", f"{ip}:{port} not working.\n", "red")


        completed_count += 1
        remaining_count = total_proxies - completed_count
        update_status(f"Completed: {completed_count}/{total_proxies} - Remaining: {remaining_count}")

def check_proxy(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ip, int(port)))
        s.close()
        return True
    except:
        return False

def update_status(status_text):
    status_label.config(text=status_text)
    status_label.update_idletasks()

def open_telegram():
    webbrowser.open("https://t.me/dontgivetheup")

root = tk.Tk()
root.title("Proxy Information")

# Set main window width and height
window_width = 500
window_height = 330
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width/2) - (window_width/2)
y_coordinate = (screen_height/2) - (window_height/2)
root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")
root.resizable(False, False)

# Create frame for side panel
side_panel_frame = tk.Frame(root, bg="lightgray", width=300)
side_panel_frame.pack_propagate(False)
side_panel_frame.pack(side="left", fill="both")

# Add label for proxy input
input_label = tk.Label(side_panel_frame, text="Enter proxies (IP:Port):", bg="lightgray")
input_label.pack()

# Add scrolled text field for proxy input
input_proxy = tk.Text(side_panel_frame, height=5)
input_proxy.pack()

# Add button to start checking proxies
check_button = tk.Button(side_panel_frame, text="Start Checking", command=start_check)
check_button.pack()

# Add label for results
results_label = tk.Label(side_panel_frame, text="Results:", bg="lightgray")
results_label.pack()

# Add scrolled text field for results
results_text = tk.Text(side_panel_frame, height=7.5)
results_text.pack()

# Add label for status
status_label = tk.Label(root, text="")
status_label.pack()

# Add labels and entry fields for proxy information
tk.Label(root, text="Proxy IP Address:").pack()
entry_ip = tk.Entry(root)
entry_ip.pack()

tk.Label(root, text="Proxy Port Number:").pack()
entry_port = tk.Entry(root)
entry_port.pack()

tk.Label(root, text="Website to Visit:").pack()
entry_url = tk.Entry(root)
entry_url.pack()

# Add button to open browser
btn_open_browser = tk.Button(root, text="Open Browser", command=open_browser)
btn_open_browser.pack()

# Add button to get public IP
btn_get_my_ip = ttk.Button(root, text="Get My IP", command=get_my_ip)
btn_get_my_ip.pack()

# Add message label
message_label = tk.Label(root, text="", fg="green")
message_label.pack()

# Add IP label
ip_label = tk.Label(root, text="")
ip_label.pack()

# Create frame to contain Telegram label
telegram_frame = tk.Frame(root, bg=root.cget('bg'), height=20)  
telegram_frame.pack(side=tk.RIGHT, padx=10, pady=(0, 10)) 

# Add Telegram link inside the frame
telegram_label = tk.Label(telegram_frame, text="Telegram", fg="blue", cursor="hand2")
telegram_label.pack(anchor=tk.SE)  

# Bind the function to open Telegram to the label
telegram_label.bind("<Button-1>", lambda event: open_telegram())

# Create text tags for color formatting
results_text.tag_configure("green", foreground="green")
results_text.tag_configure("red", foreground="red")

# Set horizontal space between the check button and the proxy input field
check_button.pack(pady=5)

root.mainloop()

