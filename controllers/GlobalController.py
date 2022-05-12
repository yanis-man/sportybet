from .components.Database import Database
from .components.DataApi import DataApi
from .components.UtilsComponent import UtilsComponents

class GlobalController:

    def __init__(self) -> None:
        self.database = Database()
        self.api_url = DataApi()
        self.utils = UtilsComponents()