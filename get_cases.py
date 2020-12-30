import json
import psycopg2
from psycopg2 import sql
import os

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

class CourtCase():
    def __init__(self, case_row):
        self.court_date, self.hearing_type, self.case_id, self.caption, self.person_name = case_row
    def to_dict(self):
        court_case_dict = {
            "court_date": self.court_date.isoformat(timespec="minutes"),
            "hearing_type": self.hearing_type,
            "case_id": self.case_id,
            "caption": self.caption,
            "person_name": self.person_name
        }
        return court_case_dict
    def to_json(self):
        return json.dumps(self.to_dict())

def connect_to_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD)
    return conn

def query_cases(db_conn, name):
    cur = db_conn.cursor()
    cases_query = sql.SQL("select {fields} from {field1} c inner join {field2} p on p.id = c.person_id where p.name = {search_name};").format(
        fields=sql.SQL(",").join([
            sql.Identifier("c", "court_date"),
            sql.Identifier("c", "hearing_type"),
            sql.Identifier("c", "case_id"),
            sql.Identifier("c", "caption"),
            sql.Identifier("p", "name")
            ]),
        field1=sql.Identifier("court_cases", "court_case"),
        field2=sql.Identifier("court_cases", "person"),
        search_name=sql.Placeholder()
        )
    cur.execute(cases_query, (name,))
    rows = cur.fetchall()
    cur.close()
    response_list = []
    for row in rows:
        case = CourtCase(row)
        response_list.append(case.to_dict())
    return json.dumps(response_list)