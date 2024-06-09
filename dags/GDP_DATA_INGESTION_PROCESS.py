from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.extract import APIExtractor
from scripts.transform import transform_gdp_country_data, transform_gdp_metrics_data
from scripts.load import SQLExecutor

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 7),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'GDP_DATA_INGESTION_PROCESS',
    default_args=default_args,
    description='A DAG to ingest GDP data periodically',
    schedule_interval='0 3 * * *',
)

def get_gdp_data(**kwargs):
    extractor = APIExtractor()
    gdp_data = extractor.fetch_gdp_data()
    country_load = transform_gdp_country_data(gdp_data)
    gdp_load = transform_gdp_metrics_data(gdp_data)
    data_load = [country_load, gdp_load]
    kwargs['ti'].xcom_push(key='data_load', value=data_load)

def load_gdp_data(**kwargs):
    ti = kwargs['ti']
    data_load = ti.xcom_pull(key='data_load', task_ids='gdp_data_extract')

    country_query = "INSERT INTO world_bank_data.country (id, name, iso3_code, created_at, updated_at) VALUES (%s, %s, %s, now(), now());"
    gdp_query = "INSERT INTO world_bank_data.gdp (country_id, year, value, created_at, updated_at) VALUES (%s, %s, %s, now(), now());"
    
    with SQLExecutor(conn_id='postgress_local_connection') as db_manager:
        db_manager.query("TRUNCATE world_bank_data.country,world_bank_data.gdp;")
        for each in data_load[0]: 
            db_manager.load_data_entries_to_db(country_query, (each['country_id'],each['country_value'],each['iso3_code']))
        for each in data_load[1]:
            db_manager.load_data_entries_to_db(gdp_query, (each['country_id'], each['year'], each['value']))

GDP_DATA_EXTRACT = PythonOperator(
    task_id='gdp_data_extract',
    python_callable=get_gdp_data,
    dag=dag,
)

GDP_DATA_LOAD = PythonOperator(
    task_id='gdp_data_load',
    python_callable=load_gdp_data,
    provide_context=True,
    dag=dag,
)

GDP_DATA_EXTRACT >> GDP_DATA_LOAD