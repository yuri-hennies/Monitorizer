from cryptography.fernet import Fernet
import os
import json
import tkinter as tk

KEY_FILE = "secret.key"
CREDENTIALS_FILE = "credentials.dat"
WEBSITES = [
    "Plataforma:",
    "Fromtis:",
    "QCertifica:"
]

def get_key():
	if not os.path.exists(KEY_FILE):
		key = Fernet.generate_key()

		with open(KEY_FILE, "wb") as file:
			file.write(key)

		return key

	with open(KEY_FILE, "rb") as file:
		return file.read()

key = get_key()
cipher = Fernet(key)

def load_credentials():
	with open(CREDENTIALS_FILE, "rb") as file:
		encrypted = file.read()

	decrypted = cipher.decrypt(encrypted)

	credentials = json.loads(decrypted.decode())

	return credentials

def save_credentials(website, username, password):
	
	if os.path.exists(CREDENTIALS_FILE):
		credentials = load_credentials()
	else:
		credentials = {}

	credentials[website] = {
		"username": username,
		"password": password
	}

	data = json.dumps(credentials).encode()

	encrypted = cipher.encrypt(data)

	with open(CREDENTIALS_FILE, "wb") as file:
		file.write(encrypted)

def credentials_exist():
	return os.path.exists(CREDENTIALS_FILE)

def credential_window():
	window = tk.Tk()
	window.title("Monitorizer Credentials")

	main_frame = tk.Frame(window, padx=20, pady=20)
	main_frame.pack()

	tk.Label(main_frame, text="Monitorizer Credentials", font=("Arial", 16, "bold")).pack()

	tk.Label(main_frame, text="Enter your credentials to continue:").pack(pady=(0, 0))

	result = None

	entries = {}

	if credentials_exist():
		saved_credentials = load_credentials()
	else:
		saved_credentials = {}

	for website in WEBSITES:

		tk.Label(window, text=website).pack()

		username_entry = tk.Entry(window)
		username_entry.pack()

		password_entry = tk.Entry(window, show="*")
		password_entry.pack()

		if website in saved_credentials:
			username_entry.insert(0, saved_credentials[website]["username"])
			password_entry.insert(0, saved_credentials[website]["password"])

		entries[website] = {
			"username": username_entry,
			"password": password_entry
		}

	def continue_credentials():

			nonlocal result

			result = load_credentials()

			window.destroy()

	def save_new_credentials():

		nonlocal result

		for website in WEBSITES:

			username = entries[website]["username"].get()
			password = entries[website]["password"].get()

			save_credentials(website, username, password)

			credentials = load_credentials()

		result = load_credentials()

		window.destroy()

	tk.Button(window, text="Continue with these credentials", command=continue_credentials).pack()

	tk.Button(window, text="Save new credentials", command=save_new_credentials).pack()

	window.mainloop()

	return result

credentials = credential_window()

print(credentials)