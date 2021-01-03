import os
import json
import psycopg2


DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


def connect_to_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD)
    return conn


class CourtCase():
    def __init__(self, court_date, hearing_type, case_id, landlord, county=None):
        self.court_date = court_date
        self.hearing_type = hearing_type
        self.case_id = case_id
        self.landlord = landlord
        self.county = county

    def to_dict(self):
        court_case_dict = {
            "court_date": self.court_date.isoformat(timespec="minutes"),
            "hearing_type": self.hearing_type,
            "case_id": self.case_id,
            "landlord": self.landlord
        }
        return court_case_dict

    def get_landlord_id(self):
        conn = connect_to_db()
        cursor = conn.cursor()

        sql_query = "SELECT id FROM court_cases.landlord WHERE name = %s;"
        cursor.execute(sql_query, (self.landlord,))
        rows = cursor.fetchall()
        if not rows:
            sql_query = "INSERT INTO court_cases.landlord (name) VALUES (%s) ;"
            cursor.execute(sql_query, (self.landlord,))
            conn.commit()
            sql_query = "SELECT id FROM court_cases.landlord WHERE name = %s;"
            cursor.execute(sql_query, (self.landlord,))
            rows = cursor.fetchall()
        self.landlord_id = rows[0][0]
        cursor.close()
        conn.close()
        return self

    def to_db_tuple(self):
        return (self.landlord_id, self.court_date, self.hearing_type, self.case_id, self.county)

    def to_json(self):
        return json.dumps(self.to_dict())
