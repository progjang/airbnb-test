import calendar
from django.utils import timezone


class Date:
    def __init__(self, date, is_past, year, month):
        self.date = date
        self.year = year
        self.month = month
        self.is_past = is_past


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.week_days = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "ctober",
            "November",
            "December",
        )

    def get_month(self):
        return self.months[self.month - 1]

    def get_dates(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        dates = []
        now = timezone.now()

        for this_week in weeks:
            for date, _ in this_week:
                is_past = False
                if self.month == now.month:
                    if date <= now.day:
                        is_past = True
                dates.append(
                    Date(date=date, is_past=is_past, year=self.year, month=self.month)
                )
        return dates
