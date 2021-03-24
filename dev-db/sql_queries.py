# DROP SCHEMA
court_cases_schema_drop = "DROP SCHEMA IF EXISTS court_cases"

# DROP TABLES

court_case_table_drop = "DROP TABLE IF EXISTS court_cases.court_case"
landlord_table_drop = "DROP TABLE IF EXISTS court_cases.landlord"

# CREATE SCHEMA
court_cases_schema_create = "CREATE SCHEMA IF NOT EXISTS court_cases"

# CREATE TABLES

court_case_table_create = "CREATE TABLE IF NOT EXISTS court_cases.court_case (landlord_id int NOT NULL, " \
                          "court_date timestamp, hearing_type text, case_id text, county text, " \
                          "PRIMARY KEY(case_id, court_date))"

landlord_table_create = "CREATE TABLE IF NOT EXISTS court_cases.landlord (id serial PRIMARY KEY, name text NOT NULL)"

# QUERY LISTS
create_schema_queries = [court_cases_schema_create]
create_table_queries = [court_case_table_create, landlord_table_create]
drop_table_queries = [court_case_table_drop, landlord_table_drop]
drop_schema_queries = [court_cases_schema_drop]