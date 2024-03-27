import requests
from datetime import datetime
from typing import Optional

IRC_LOG = 'https://irclogs.ubuntu.com'
IRC_CHANNELS = [
    "#ubuntu-devel",
    "#ubuntu-meeting",
    "#ubuntu-release",
    "#ubuntu-server",
    "#ubuntu-bugs",
]


class Date:

    def __init__(self, date: datetime):
        self.date = datetime.astimezone(date)

    @classmethod
    def now(cls):
        return cls(datetime.now())

    @classmethod
    def from_date(cls, day: int, month: int, year: int):
        return cls(datetime(year, month, day))

    def __str__(self):
        year = self.date.year
        month = f"{self.date.month}"
        day = f"{self.date.day}"

        return f"{year}/{month.zfill(2)}/{day.zfill(2)}"

    @property
    def tz(self):
        offset = self.date.utcoffset()

        hours_delta = offset.days * 24
        seconds_delta_in_hours = offset.seconds // 3600
        total_hour_delta = hours_delta + seconds_delta_in_hours

        return f"(UTC {total_hour_delta})"

    def __sub__(self, other):
        return type(self)(self.date - other)


class BadUrlError(Exception):
    def __init__(
        self,
        url: str = None,
        channel: Optional[str] = None,
        date: Optional[Date] = None,
    ):
        message = (
            "404 Error: Log not found\n"
            f"URL: {url!r}\n"
        )

        if channel:
            message += f"Channel: {channel.replace('%23','#')!r}\n"

        if date:
            message += f"Date: {date} {date.tz}\n"
        super().__init__(message)


def parse_logs(queries: list[str], logs: list[str], highlight: bool = False) -> list:
    """Parse logs for lines containing query tokens

    All query tokens must exist in a line but are not case sensitive
    """
    good_lines: list[str] = []

    lower_queries: list[str] = [q.lower() for q in queries]
    for log in logs:
        log_lines: list[str] = log.splitlines()
        for line in log_lines:
            lower_line: str = line.lower()
            tokens: set[str] = set(lower_line.split())
            queries: set[str] = set(lower_queries)
            if queries - tokens == set():
                good_lines.append(line)

    return good_lines


def get_log(channel: str, date: Date) -> str:

    channel = channel.replace("#", "%23")
    url: str = f"{IRC_LOG}/{date}/{channel}.txt"

    response: requests.models.Response = requests.get(url)

    if response.status_code == 404:
        raise BadUrlError(url=url, channel=channel, date=date)

    return response.text
