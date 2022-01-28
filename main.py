from selenium import webdriver
from data_manager import DataManager
from dotenv import dotenv_values

config = dotenv_values(".env")
chrome_driver_path = config.get('DRIVER_PATH')

data_manager = DataManager()
sheet_data = data_manager.get_company_data()

driver = webdriver.Chrome(executable_path=chrome_driver_path)

for row in sheet_data:
    driver.get("https://tools.usps.com/zip-code-lookup.htm?byaddress")
    company = driver.find_element_by_name("tCompany")
    company.send_keys(row["company"])
    addresses = driver.find_element_by_name("tAddress")
    addresses.send_keys((row["street"]))
    city = driver.find_element_by_name("tCity")
    city.send_keys((row["city"]))
    state = driver.find_element_by_name("tState")
    state.send_keys(row["st"])
    zip_code = driver.find_element_by_name("tZip-byaddress")
    zip_code.send_keys(row["zipCode"])
    find = driver.find_element_by_id("zip-by-address")
    find.click()

    row["message"] = ""
    if not driver.find_element_by_id("search-address-again").is_displayed():
        row["message"] = "Invalid"

data_manager.destination_data = sheet_data
data_manager.update_error_message()
