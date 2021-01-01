import json
from psycopg2 import sql
from main import connect_to_db, CourtCase

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

if __name__=="__main__":
    db_connection = connect_to_db()
    query_cases(db_connection, "test")