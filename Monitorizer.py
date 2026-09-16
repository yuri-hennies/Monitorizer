#Selenium for browser automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

#python's date tools
from datetime import datetime

today = datetime.today().strftime("%d/%m/%Y")

#Tkinter for dialog boxes
import tkinter as tk
from tkinter import ttk

options=Options()
#options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

#LOGIN PLAT
driver.get("https://backoffice.prod.qflash.com.br/login")

email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
email.send_keys("email")

password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
password.send_keys("password")

login_button = WebDriverWait(driver, 10).until(
	EC.element_to_be_clickable(
		(By.XPATH, "//button[@type='submit' and text()='Entrar']")
		)
	)
login_button.click()

WebDriverWait(driver, 10).until(
	EC.element_to_be_clickable(
		(By.XPATH, "//button[text()='QConsignado']")
		)
	)


#LOGIN FROMTIS
driver.get("https://sistema02.finvestdigital.com.br/login")

FROMTIS_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "j_username")))
FROMTIS_login.send_keys("login")

FROMTIS_pass = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "j_password")))
FROMTIS_pass.send_keys("password")

FROMTIS_button = WebDriverWait(driver, 10).until(
	EC.element_to_be_clickable(
		(By.XPATH, "//button[@type='submit' and text()=' Entrar']")
		)
	)
FROMTIS_button.click()

WebDriverWait(driver, 10).until(
	EC.element_to_be_clickable(
		(By.XPATH, "//*[@id='liquidacaoMenu']")
		)
	)

#LOGIN QCERTIFICA
driver.get("https://portal.qcertifica.com.br/Authentication/Login.aspx")

QCERT_login = WebDriverWait(driver, 10).until(
	EC.presence_of_element_located(
		(By.NAME, "ctl00$body$txtUsuario")
		)
	)
QCERT_login.send_keys("login")

QCERT_pass = WebDriverWait(driver, 10).until(
	EC.presence_of_element_located(
		(By.NAME, "ctl00$body$txtSenha")
		)
	)
QCERT_pass.send_keys("password")

QCERT_button = WebDriverWait(driver, 10).until(
	EC.element_to_be_clickable(
		(By.XPATH, "//*[@id='ctl00_body_btnEntrar']")
		)
	)
QCERT_button.click()


try:

	already_connected = WebDriverWait(driver, 10).until(
		EC.visibility_of_element_located(
			(By.XPATH, "//*[@id='ctl00_body_btnSimUsuarioLogado']")
			)
		)
	already_connected.click()

except TimeoutException:

	print("Nope")

WebDriverWait(driver, "10").until(
	EC.presence_of_element_located(
		(By.XPATH, "//*[@id='ctl00_logo']")
		)
	)

def get_table_data(selected_date):

	driver.get("https://backoffice.prod.qflash.com.br/borderos-fornecedor")

	table = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, "table.items-center")
			)
		)
	table = table.text

	dropdown = WebDriverWait(driver, "10").until(
		EC.element_to_be_clickable(
			(By.CLASS_NAME, "css-19bb58m")
			)
		)
	dropdown.click()

	dropdown_input = WebDriverWait(driver, "10").until(
	    EC.element_to_be_clickable(
	        (By.ID, "react-select-3-input")
	    )
	)
	dropdown_input.send_keys("BSB")
	dropdown_input.send_keys(Keys.ENTER)

	criado_de = WebDriverWait(driver, "10").until(
		EC.element_to_be_clickable(
			(By.ID, "criado_de")
			)
		)
	criado_de.click()
	criado_de.send_keys(selected_date)

	criado_ate = WebDriverWait(driver, "10").until(
		EC.element_to_be_clickable(
			(By.ID, "criado_ate")
			)
		)
	criado_ate.click()
	criado_ate.send_keys(selected_date)

	filtrar_button = WebDriverWait(driver, 10).until(
	EC.element_to_be_clickable(
		(By.XPATH, "//*[@id='__next']/div/div[3]/div[1]/div/div[1]/div/div[2]/form/div[2]/div/button")
		)
	)
	filtrar_button.click()

	WebDriverWait(driver, 10).until(
		lambda driver:
			driver.find_element(By.CSS_SELECTOR, "table.items-center").text != table)


	table = WebDriverWait(driver, 10).until(
	EC.presence_of_element_located((By.CSS_SELECTOR, "table.items-center")
		)
	)

	thead = table.find_elements(By.TAG_NAME, "th")
	head_row = []

	for head in thead:
		head_row.append(head.text)

	tbody = table.find_element(By.TAG_NAME, "tbody")
	rows = tbody.find_elements(By.TAG_NAME, "tr")

	table_data = []
	table_data.append(head_row)


	for row in rows:
			cells = row.find_elements(By.TAG_NAME, "td")

			row_data = []

			for cell in cells:
				row_data.append(cell.text)

			table_data.append(row_data)


	columns_to_keep = [0, 5, 6, 9, 10, 12]
	filtered_columns = []

	for row in table_data:
		new_row = []

		for column_index in columns_to_keep:
			new_row.append(row[column_index])

		filtered_columns.append(new_row)

	target_date = datetime.strptime(selected_date, "%d/%m/%Y").date()

	final_data = [filtered_columns[0]]

	for row in filtered_columns[1:]:

		row_date = datetime.strptime(row[0], "%d/%m/%Y %H:%M").date()

		if row_date == target_date:
			final_data.append(row)

	#organizes in alphabetical order
	header = final_data[0]
	rows = final_data[1:]

	rows.sort(key=lambda row: row[1])

	final_data = [header] + rows

	return final_data

plat_final_data = get_table_data(today)

def get_FROMTIS_data(selected_date):

	driver.get("https://sistema02.finvestdigital.com.br/financeiro/liquidacao")

	dropdown = WebDriverWait(driver, "10").until(
	    EC.element_to_be_clickable(
	        (By.XPATH, "//*[@id='fundoSelecionado_chzn']/a")
	    )
	)
	dropdown.click()
	
	dropdown_input = WebDriverWait(driver, "10").until(
		EC.element_to_be_clickable(
			(By.XPATH, "//*[@id='fundoSelecionado_chzn']/div/div/input")
			)
		)
	dropdown_input.send_keys("BSB")
	dropdown_input.send_keys(Keys.ENTER)

	situacao = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable(
			(By.XPATH, "//*[@id='situacaoSelecionado_chzn']/a/abbr")
			)
		)
	situacao.click()

	date = WebDriverWait(driver, "10").until(
		EC.element_to_be_clickable(
			(By.ID, "data")
			)
		)
	date.send_keys(selected_date)

	escape = WebDriverWait(driver, "10").until(
		EC.element_to_be_clickable(
			(By.ID, "span_portal_top")
			)
		)
	escape.click()


	button = WebDriverWait(driver, "10").until(
		EC.element_to_be_clickable(
			(By.ID, "pesquisa")
			)
		)
	button.click()

	table = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")
			)
		)
	tbody = table.find_element(By.TAG_NAME, "tbody")
	rows = tbody.find_elements(By.TAG_NAME, "tr")

	table_data = []

	for row in rows:
			cells = row.find_elements(By.TAG_NAME, "td")

			row_data = []

			for cell in cells:
				row_data.append(cell.text)

			table_data.append(row_data)

	columns_to_keep = [3, 5, 6]
	filtered_data = []

	for row in table_data:
		new_row = []

		for column_index in columns_to_keep:
			new_row.append(row[column_index])

		filtered_data.append(new_row)

	return filtered_data

fromtis_final_data = get_FROMTIS_data(today)

def join_plat_fromtis(table_1, table_2):

	table_1[0].append("FROMTIS")

	for row_1 in table_1[1:]:

		name_1 = row_1[1].upper()

		if "&" in name_1:
			name_1 = name_1.replace("&", "E")

		value_1 = row_1[3]
		reject_1 = row_1[5].upper()

		information = ""

		for row_2 in table_2:

			name_2 = row_2[0].upper()
			value_2 = row_2[1]

			if name_2 in name_1 and value_1 == value_2 and "REJEITADO" not in reject_1:

				information = row_2[2]

				break

		row_1.append(information)

	return table_1

final_data = join_plat_fromtis(plat_final_data, fromtis_final_data)

print(final_data)

def get_QCERT_data(selected_date):

	driver.get("https://portal.qcertifica.com.br/DigitalSignature/FAS903.aspx")

	'''
	login_screen = driver.find_element(By.NAME, "ctl00$body$txtUsuario")


	if login_screen:

		try:

			QCERT_login = WebDriverWait(driver, 2).until(
				EC.presence_of_element_located(
					(By.NAME, "ctl00$body$txtUsuario")
					)
				)
			QCERT_login.send_keys("12774451760")

			QCERT_pass = WebDriverWait(driver, 1).until(
				EC.presence_of_element_located(
					(By.NAME, "ctl00$body$txtSenha")
					)
				)
			QCERT_pass.send_keys("Borisfaisca1@")

			QCERT_button = WebDriverWait(driver, 1).until(
				EC.element_to_be_clickable(
					(By.XPATH, "//*[@id='ctl00_body_btnEntrar']")
					)
				)
			QCERT_button.click()

			try:

				already_connected = WebDriverWait(driver, 2).until(
					EC.visibility_of_element_located(
						(By.XPATH, "//*[@id='ctl00_body_btnSimUsuarioLogado']")
						)
					)
				already_connected.click()

			except TimeoutException:

				print("Nope")

		except TimeoutException:

				print("Nope")
	'''

	documento_de = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located(
			(By.XPATH, "//*[@id='ctl00_cphContext_tabManager_PV0_UC0_frvDocument_txbReceiveFrom_dateInput']")
			)
		)
	documento_de.send_keys(selected_date)

	documento_ate = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located(
			(By.XPATH, "//*[@id='ctl00_cphContext_tabManager_PV0_UC0_frvDocument_txbReceiveTo_dateInput']")
			)
		)
	documento_ate.send_keys(selected_date)

get_QCERT_data(today)

root = tk.Tk()
root.title("Monitorizer")
root.geometry("1000x500")

main_frame = ttk.Frame(root)
main_frame.pack(
	fill="both",
	expand=True,
	padx=25,
	pady=25
	)

date_frame = ttk.Frame(main_frame)
date_frame.pack(
	fill="x",
	pady=(0, 10)
	)

date_label = ttk.Label(
	date_frame,
	text="Date:"
	)
date_label.pack(
	side="left"
	)

date_entry = ttk.Entry(
	date_frame,
	width=15
	)
date_entry.pack(
	side="left",
	padx=(10, 0)
	)

date_entry.insert(0, today)

def test_date():

    selected_date = date_entry.get()

    print(selected_date)

test_button = ttk.Button(
	date_frame,
	text="test",
	command=test_date
	)
test_button.pack(
	side="left",
	padx=10
	)

table_frame = ttk.Frame(main_frame)
table_frame.pack(
	side="left",
	fill="both",
	expand=True,
	padx=10,
	pady=10
	)

table = ttk.Treeview(table_frame, columns=final_data[0], show="headings")

for col in final_data[0]:
	table.heading(col, text = col)
	table.column(col, width=150)

for row in final_data[1:]:
	table.insert("", "end", values=row)

table.pack(fill="both", expand=True)

def update_table(new_data):
	for item in table.get_children():
		table.delete(item)

	for row in new_data[1:]:
		table.insert("", "end", values=row)

def refresh_data():
	selected_date = date_entry.get()
	new_data = get_table_data(selected_date)
	update_table(new_data)



button_frame = ttk.Frame(main_frame)
button_frame.pack(
	side="right",
	fill="y",
	padx=(0, 10),
	pady=10
	)

def button2():
	print("Button 2 pressed")


btn1 = tk.Button(button_frame, text="Atualizar", command=refresh_data)
btn1.pack(fill="x", pady=5)

btn2 = tk.Button(button_frame, text="Button 2", command=button2)
btn2.pack(fill="x", pady=5)
root.mainloop()


driver.quit()

