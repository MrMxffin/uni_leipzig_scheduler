# almaweb_client.py
import re
import requests
import datetime
from bs4 import BeautifulSoup


def format_schedule(schedule_entries):
    formatted_schedule = "📅 Stundenplan für die kommende Woche:\n\n"
    for entry in schedule_entries:
        formatted_schedule += f"📆 {entry['date']}:\n"
        formatted_schedule += f"- 📚 Kurs: {entry['course_name']}\n"
        formatted_schedule += f"  👨‍🏫 Dozent: {entry['lecturer']}\n"
        formatted_schedule += f"  ⏰ Zeit: {entry['time']}\n"
        formatted_schedule += f"  🏫 Raum: {entry['room']}\n\n"
    return formatted_schedule


def _parse_schedule(html):
    soup = BeautifulSoup(html, 'html.parser')
    schedule_data = []
    date = None  # Initialize date variable to store the current date
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols:
            # Check if the first column contains header information
            if 'Kursnr.' in cols[0].text.strip() or 'Veranstaltung' in cols[0].text.strip():
                continue  # Skip header rows
            # Check if it's a date row
            elif 'tbhead' in cols[0].get('class', []):
                date = cols[0].text.strip()
            else:
                course_number = cols[0].text.strip()
                course_name = cols[1].text.strip()
                lecturer = cols[2].text.strip()
                time = cols[3].text.strip()
                room = cols[4].text.strip()
                schedule_data.append({
                    "date": date,
                    "course_number": course_number,
                    "course_name": course_name,
                    "lecturer": lecturer,
                    "time": time,
                    "room": room
                })
    return schedule_data


def _extract_session_id(refresh_header):
    if refresh_header:
        url_match = re.search(r'-N(\d+)', refresh_header)
        if url_match:
            session_id = url_match.group(1)
            return session_id
    raise ValueError("Session ID not found in headers")


class AlmaWebClient:

    def __init__(self,username,password):
        self.base_url = "https://almaweb.uni-leipzig.de"
        self.username = username
        self.password = password
        self.session_id = None
        self.cookies = {}

    def login(self):
        login_url = f"{self.base_url}/scripts/mgrqispi.dll"
        params = {
            "usrname": self.username,
            "pass": self.password,
            "APPNAME": "CampusNet",
            "PRGNAME": "LOGINCHECK",
            "ARGUMENTS": "clino,usrname,pass,menuno,menu_type,browser,platform",
            "clino": "000000000000001",
            "menuno": "000299",
            "menu_type": "classic",
            "browser": "",
            "platform": ""
        }

        try:
            response = requests.post(login_url, data=params, verify=False)
            response.raise_for_status()
            self.session_id = _extract_session_id(response.headers['REFRESH'])
            self.cookies = response.cookies.get_dict()  # Extract cookies from response
        except requests.RequestException as e:
            raise RuntimeError(f"Login Error: {e}")

    def get_schedule(self):
        if not self.session_id:
            self.login()  # Perform login if session ID is not available
        schedule_url = f"{self.base_url}/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=SCHEDULERPRINT&ARGUMENTS=-N{self.session_id},-N000376,-A{datetime.datetime.now().strftime('%d.%m.%Y')},-A,-N1"

        try:
            response = requests.get(schedule_url, cookies=self.cookies)  # Send cookies with the request
            response.raise_for_status()
            return format_schedule(_parse_schedule(response.content))
        except requests.RequestException as e:
            raise RuntimeError(f"Schedule Error: {e}")