# almaweb_client.py

import re
import requests
import datetime
from bs4 import BeautifulSoup


def format_schedule(schedule_entries):
    """Format schedule data for display."""
    formatted_schedule = "📅 Stundenplan für die kommende Woche:\n\n"
    prev_date = None
    for entry in schedule_entries:
        if entry['date'] != prev_date:
            if prev_date is not None:
                formatted_schedule += "\n"
            formatted_schedule += f"📆 {entry['date']}:\n"
            prev_date = entry['date']
        formatted_schedule += f"    📚 Kurs: {entry['course_name']}\n"
        formatted_schedule += f"        👨‍🏫 Dozent: {entry['lecturer']}\n"
        formatted_schedule += f"        ⏰ Zeit: {entry['time']}\n"
        formatted_schedule += f"        🏫 Raum: {entry['room']}\n\n"
    return formatted_schedule



def _parse_schedule(html):
    """Parse HTML to extract schedule data."""
    soup = BeautifulSoup(html, 'html.parser')
    schedule_data = []
    date = None
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols:
            if 'Kursnr.' in cols[0].text.strip() or 'Veranstaltung' in cols[0].text.strip():
                continue
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
    """Extract session ID from HTTP headers."""
    if refresh_header:
        url_match = re.search(r'-N(\d+)', refresh_header)
        if url_match:
            session_id = url_match.group(1)
            return session_id
    raise ValueError("Session ID not found in headers")


class AlmaWebClient:
    """Client for accessing AlmaWeb."""

    def __init__(self, username, password):
        """Initialize the AlmaWebClient with username and password."""
        self.base_url = "https://almaweb.uni-leipzig.de"
        self.username = username
        self.password = password
        self.session_id = None
        self.cookies = {}

    def login(self):
        """Perform login to the AlmaWeb system."""
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
            self.cookies = response.cookies.get_dict()
        except requests.RequestException as e:
            raise RuntimeError(f"Login Error: {e}")

    def get_schedule(self):
        """Get schedule data from AlmaWeb."""
        if not self.session_id:
            self.login()

        tomorrow_date_formatted = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
        schedule_url = f"{self.base_url}/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=SCHEDULERPRINT&ARGUMENTS=-N{self.session_id},-N000376,-A{tomorrow_date_formatted},-A,-N1"

        try:
            response = requests.get(schedule_url, cookies=self.cookies)
            response.raise_for_status()
            return format_schedule(_parse_schedule(response.content))
        except requests.RequestException as e:
            raise RuntimeError(f"Schedule Error: {e}")
