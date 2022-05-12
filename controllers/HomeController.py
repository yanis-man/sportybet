from flask import render_template
import datetime

from .GlobalController import GlobalController


class HomeController(GlobalController):
    def __init__(self) -> None:
        super().__init__()
    
    def index(self):
        today = datetime.datetime.today()
        today_date = today.strftime("%d-%m-%Y")
        today_hour = today.strftime("%H:%M")
        remaining_fixtures_tuple = self.database.pull_from_db(f"SELECT * FROM fixtures WHERE day = {today_date} AND hour >= '{today_hour}'", order_by="league_name")
        remaining_fixtures = []
        for fixture in remaining_fixtures_tuple:
            new_fixture = list(fixture)
            new_fixture[8] = today.replace(hour=0, minute=0, second=0) + fixture[8]
            remaining_fixtures.append(new_fixture)
        return remaining_fixtures
