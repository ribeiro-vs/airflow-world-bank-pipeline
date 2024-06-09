import requests
import logging

logger = logging.getLogger('airflow.task')

# Utilization a class for the current and probably future api extractions control and organization
class APIExtractor():
    def fetch_gdp_data(self):
        all_data = []
        page = 1
        while True:
            url = f"https://api.worldbank.org/v2/country/ARG;BOL;BRA;CHL;COL;ECU;GUY;PRY;PER;SUR;URY;VEN/indicator/NY.GDP.MKTP.CD?format=json&page={page}&per_page=50"
            response = requests.get(url)
            data = response.json()
            if not data[1]:
                break
            all_data.extend(data[1])
            page += 1
        logger.info('fetch_gdp_data from APIExtractor: GDP Data successfully fetched.')
        return all_data