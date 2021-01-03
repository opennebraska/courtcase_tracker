import pytz
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from main import connect_to_db, CourtCase

def insert_cases(cases):
    query = "INSERT INTO court_cases.court_case (landlord_id, court_date, hearing_type, case_id, county) " \
            "VALUES (%s, %s, %s, %s, %s)"

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.executemany(query, cases)
        conn.commit()
    except Exception as e:
        print('Error:', e)
    finally:
        cursor.close()
        conn.close()


def get_cases(county, date):
    url = 'https://www.nebraska.gov/courts/calendar/index.cgi'
    myobj = {
        'court': 'C',
        'countyC': county,
        'countyD': '',
        'selectRadio': 'date',
        'searchField': date,
        'submitButton': 'Submit'
    }

    response = requests.post(url, data=myobj)
    content = str(response.content, "utf-8")

    soup = BeautifulSoup(content, features="html.parser")
    table_rows = soup.find_all('tr')
    court_cases = [row.find_all("td") for row in table_rows
                   if len(row.find_all("td")) == 6 and row.find_all("td")[0].get_text()]

    eviction_cases = []
    for court_case in court_cases:
        case_name, court_date, time, hearing_type, caption, case_id = [col.get_text().strip() for col in court_case]
        if "Restitution" in hearing_type:
            landlord = caption.split("v.")[0].strip()
            local = pytz.timezone("America/Chicago")
            localdatetime = datetime.strptime(f"{court_date}T{time}", "%m/%d/%YT%I:%M%p")
            utc_dt = local.localize(localdatetime, is_dst=None).astimezone(pytz.utc)
            eviction_cases.append(CourtCase(utc_dt, hearing_type, case_id, landlord, county).get_landlord_id().to_db_tuple())
    return eviction_cases

if __name__ == '__main__':
    cases = get_cases('Douglas', '01/15/2021')
    insert_cases(cases)