import time
from datetime import datetime as dt


class Account:
    def __init__(self, id: str, name: str, currency: str):
        self.id = id
        self.name = name
        self.currency = currency


class Entry:
    def __init__(self, account: Account, entry: dict) -> None:
        self.time = create_date(entry["time"])[2]
        self.amount = entry["amount"] / 100
        self.currency = account.currency
        self.from_name = account.name
        self.to_name = None
        self.description = entry["description"]


def date_to_time(date: dt) -> int:
    return int(time.mktime(date.timetuple()))


def create_date(time: int) -> tuple[dt, int, str]:
    date = dt.fromtimestamp(time)
    return date, time, date.strftime("%m/%d/%Y %H:%M:%S")
