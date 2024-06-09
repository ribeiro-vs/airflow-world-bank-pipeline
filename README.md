# GDP Data Ingestion Pipeline - Airflow Project

## Project Description
This Airflow project contains a data ingestion pipeline that extracts GDP data of South American countries from the World Bank API and loads it into a PostgreSQL database.

In the project folder `other/sql/scripts`, you'll find the SQL queries used to generate the database tables and schemas. Additionally, there's a query that generates a pivoted report with GDP information of the last 5 years for each country present in the database tables.

## Project Requirements
- Docker installed on your machine
- Python 3.11
- Git installed and set up
- A SQL client of your choice (DBeaver recommended)
- A code editor of your choice (VSCode recommended, though not mandatory)

## How to Run the Project
### 0. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

### 1. Activate the containers:
- Open Docker
- Open your terminal and navigate to the folder containing the `docker-compose.yaml` file
- Initiate the services with the command docker-compose up -d

### 2. Test Airflow and check it's connections
- Open your browser and go to the Airflow URL: `localhost:9090` (default port is 8080, but this project uses port 9090; you can change the port in the `docker-compose.yaml` file if needed)
- Log in with username and password: `airflow`
- Navigate to Admin > Connections and add the following Conn Id if it is not there: `postgress_local_connection`. These are the necessary field values:
<div align="left">

| Field               | Value                    |
|---------------------|--------------------------|
| **Connection Id**   | postgress_local_connection |
| **Connection Type** | Postgres                 |
| **Host**            | host.docker.internal     |
| **Database**        | postgres                 |
| **Login**           | app_user                 |
| **Password**        | app_password             |
| **Port**            | 5433                     |

</div>

### 3. Configure the database tables
- To configure the database, you need to execute the SQL query located at `airflow_project/other/sql_scripts/tables_and_schema_ddl.sql` using a SQL client like DBeaver. You can always refer to the `docker-compose.yaml` file to check the database credentials.


Below there's a quick guide on how to do it using DBeaver: 

### DBeaver - Setting up the schema and tables

#### Installation and Opening DBeaver
1. Download and install DBeaver from [here](https://dbeaver.io/download/).
2. Open DBeaver after installation.

#### Establishing a Connection
1. Click the plug icon or select **Database > New Connection** to set up a new Postgres connection.
2. In the connection settings dialog, input the following details:

   | Field         | Value         |
   |---------------|---------------|
   | **Host**      | localhost     |
   | **Port**      | 5433          |
   | **Database**  | postgres      |
   | **Username**  | app_user      |
   | **Password**  | app_password  |

3. Click **Finish** to establish the connection.

#### Executing SQL Scripts
1. Once connected, right-click the database icon and select **SQL Editor > Open SQL Script**.
2. Copy and paste the queries from the DDL file present in `airflow_project/other/sql_scripts/tables_and_schema_ddl.sql`.
3. Execute the queries one by one to set up your schema and tables.

#### Troubleshooting Tips
- If you encounter issues, first check the error messages for hints on what might be wrong.
- Ensure that your database service in `docker-compose.yaml` is active and running.
- Verify that all credentials and connection settings are correct and match those of the `docker-compose.yaml` file.

## Project Overview

### Services used in the `docker-compose.yaml` file
To implement the services, I used the official template of Airflow 2.9.1 (stable version) available at [Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/2.9.1/docker-compose.yaml). More information can be found [here](https://airflow.apache.org/docs/apache-airflow/2.9.1/).

The only change made to the template was the addition of a separate PostgreSQL database. This ensures we do not use the same PostgreSQL server that Airflow uses, preventing interference between Airflow and our separate solution (the database to store World Bank data), providing more safety and scalability.

Here is the code line where the separate database server is added:

```yaml
# Separate database server for future interactions
  app_db:
    image: postgres:13
    environment:
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: app_password
      POSTGRES_DB: app_db
    ports:
      - "5433:5432"
    volumes:
      - app-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "app_user"]
      interval: 10s
      retries: 5
      start_period: 5s
    restart: always

volumes:
  postgres-db-volume:
  app-db-volume:
```

### Database and tables configuration
The database is configured with its timezone set to UTC by default, a specific schema for the data we'll work on, and control columns such as `created_at` and `updated_at` to check the datetime information of data input and modifications.

### 2. Custom python modules
The project is designed for scalability and code reusability, utilizing object-oriented programming concepts.

A directory is created to store three modules: extract, transform, and load. The names aim to clearly convey the purpose of each module.

- `extract` contains functions and classes for data extraction.
- `transform` contains functions and classes for data transformation.
- `load` contains functions and classes for data loading.

## Contact
If you have any questions or suggestions about the project, feel free to reach out.

- **Name:** Vinicius RIbeiro
- **Email:** [ribeiro.vr20@gmail.com](mailto:ribeiro.vr20@gmail.com)
- **LinkedIn:** [vinicius-ribeiro1](https://www.linkedin.com/in/vinicius-ribeiro1/)
- **GitHub:** [Personal Account](https://github.com/ribeiro-vs), [Work Account](https://github.com/viniciusribeir0)