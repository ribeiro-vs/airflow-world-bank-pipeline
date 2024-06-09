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
    created_at timestamp,
    updated_at timestamp
);
-- Gdp metrics table creation
CREATE TABLE IF NOT EXISTS world_bank_data.gdp (
    country_id varchar(2),
    "year" int4 NULL,
    value numeric NULL,
    created_at timestamp,
    updated_at timestamp
);