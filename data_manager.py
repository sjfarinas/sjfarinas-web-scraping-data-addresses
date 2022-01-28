import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config.get('TOKEN')
SHEET_ENDPOINT = config.get('SHEET_ENDPOINT')

sheet_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_company_data(self):
        return requests.get(url=SHEET_ENDPOINT, headers=sheet_headers).json()["sheet1"]

    def update_error_message(self):
        for company in self.destination_data:
            new_data = {
                "sheet1": {
                    "message": company["message"]
                }
            }
            response = requests.put(
                url=f"{SHEET_ENDPOINT}/{company['id']}",
                json=new_data,
                headers=sheet_headers
            )
            print(response.text)