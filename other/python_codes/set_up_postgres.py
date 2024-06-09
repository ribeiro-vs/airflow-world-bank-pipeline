import psycopg2

# Function to connect to the database and set up tables, schema, and timezone
def connect_and_query():
    try:
        # Connection settings
        conn = psycopg2.connect(
            dbname="app_db",
            user="app_user",
            password="app_password",
            host="localhost",  
            port="5433"        
        )
        
        # Cursor creation
        cur = conn.cursor()
        
        # Query execution
        cur.execute(""" 
            -- Setting timezone to UTC
            SET TIMEZONE='UTC';

            -- Schema creation
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'world_bank_data') THEN
                    CREATE SCHEMA world_bank_data AUTHORIZATION app_user;
                END IF;
            END
            $$;

            -- Country table creation
            CREATE TABLE IF NOT EXISTS world_bank_data.country (
                id varchar(2) NULL,
                "name" varchar(30) NULL,
                iso3_code varchar(3) null,
                create_at timestamp,
                updated_at timestamp
            );

            -- Gdp metrics table creation
            CREATE TABLE IF NOT EXISTS world_bank_data.gdp (
                country_id varchar(2),
                "year" int4 NULL,
                value numeric NULL,
                create_at timestamp,
                updated_at timestamp
            ); 
        """)

        # Commit the changes
        conn.commit()

        # Checking if the tables exist to verify execution
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'world_bank_data';
        """)

        tables = cur.fetchall()

        print("Tables created/existing in 'world_bank_data' schema:", [table[0] for table in tables])
        
        # Closing cursor and connection
        cur.close()
        conn.close()
        print("SQL file executed successfully.")
    except Exception as e:
        print("An error occurred:", e)
 
connect_and_query()