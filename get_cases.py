import json
from psycopg2 import sql
from main import connect_to_db, CourtCase


def query_cases(landlord=None, start_date=None, end_date=None):
    conn = connect_to_db()
    cursor = conn.cursor()

    if landlord:
        sql_query = "select {fields} from {field1} c inner join {field2} p on p.id = c.landlord_id where p.name = {search_name};"
    else:
        sql_query = "select {fields} from {field1} c inner join {field2} p on p.id = c.landlord_id;"

    cases_query = sql.SQL(sql_query).format(
        fields=sql.SQL(",").join([
            sql.Identifier("c", "court_date"),
            sql.Identifier("c", "hearing_type"),
            sql.Identifier("c", "case_id"),
            sql.Identifier("p", "name")
            ]),
        field1=sql.Identifier("court_cases", "court_case"),
        field2=sql.Identifier("court_cases", "landlord"),
        search_name=sql.Placeholder()
        )

    cursor.execute(cases_query, (landlord,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    response_list = []
    for row in rows:
        court_date, hearing_type, case_id, landlord_name = row
        response_list.append(CourtCase(court_date, hearing_type, case_id, landlord_name).to_dict())

    return json.dumps(response_list)


if __name__=="__main__":
    cases = query_cases()
    print(cases)