SELECT
    country.id,
    country.name,
    country.iso3_code,
    SUM(CASE WHEN gdp.year = 2019 THEN gdp.value / 1e9 ELSE 0 END) AS "2019",
    SUM(CASE WHEN gdp.year = 2020 THEN gdp.value / 1e9 ELSE 0 END) AS "2020",
    SUM(CASE WHEN gdp.year = 2021 THEN gdp.value / 1e9 ELSE 0 END) AS "2021",
    SUM(CASE WHEN gdp.year = 2022 THEN gdp.value / 1e9 ELSE 0 END) AS "2022",
    SUM(CASE WHEN gdp.year = 2023 THEN gdp.value / 1e9 ELSE 0 END) AS "2023"
FROM
    world_bank_data.country
JOIN
    world_bank_data.gdp ON country.id = gdp.country_id
GROUP BY
    country.id, country.name, country.iso3_code
ORDER BY
    country.name;