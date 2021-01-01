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
    def __init__(self, case_row):
        self.court_date, self.hearing_type, self.case_id, self.caption, self.person_name = case_row
    def to_dict(self):
        court_case_dict = {
            "court_date": self.court_date.isoformat(timespec="minutes"),
            "hearing_type": self.hearing_type,
            "case_id": self.case_id,
            "landlord": self.caption
        }
        return court_case_dict
    def to_json(self):
        return json.dumps(self.to_dict())
