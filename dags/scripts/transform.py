import logging

logger = logging.getLogger('airflow.task')

# Transformantion functions
def transform_gdp_country_data(response,**kwargs):
    data = response
    # Extracting relevant information and removing duplicates when necessary
    unique_data = {}
    for item in data:
        country_id = item["country"]["id"]
        if country_id not in unique_data:
            unique_data[country_id] = {
                "country_id": country_id,
                "country_value": item["country"]["value"],
                "iso3_code": item["countryiso3code"]
            } 
    country_data_list = list(unique_data.values()) 
    logger.info('transform_gdp_country_data from transform: Data successfully generated')
    return country_data_list

def transform_gdp_metrics_data(response,**kwargs):
    data = response

    gpd_data_list = [{
        "country_id": item["country"]["id"],
        "year": item["date"],
        "value": item["value"]
    } for item in data]
    logger.info('transform_gdp_metrics_data from transform: Data successfully generated')
    return gpd_data_list