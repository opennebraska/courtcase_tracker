import pytz
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def update_db(conn, table_rows):
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    for table_row in table_rows[3:]:
        try:
            cname, date, time, hearing_type, caption, case_id = [c.get_text().strip() for c in table_row.find_all("td")]

            if "Restitution" in hearing_type:
                landlord = caption.split("v.")[0].strip()

                local = pytz.timezone("America/Chicago")
                localdatetime = datetime.strptime(f"{date}T{time}", "%m/%d/%YT%I:%M%p")
                local_dt = local.localize(localdatetime, is_dst=None)
                utc_dt = local_dt.astimezone(pytz.utc)

                cursor.execute("INSERT INTO court_cases.court_case (person_id, court_date, hearing_type, case_id, caption) VALUES (%s, %s, %s, %s, %s)", ('1', utc_dt, hearing_type, case_id, landlord))
        except Exception:
            continue

    conn.commit()

def get_data(date):
    url = 'https://www.nebraska.gov/courts/calendar/index.cgi'
    myobj = {
        'court': 'C',
        'countyC': 'Douglas',
        'countyD': '',
        'selectRadio': 'date',
        'searchField': date,
        'submitButton': 'Submit'
    }

    response = requests.post(url, data=myobj)
    content = str(response.content, "utf-8")

    soup = BeautifulSoup(content, features="html.parser")
    table_rows = soup.find_all('tr')
    return table_rows

if __name__ == '__main__':
    table_rows = get_data('01/05/2021')
    #from main import connect_to_db
    #update_db(connect_to_db(), table_rows)