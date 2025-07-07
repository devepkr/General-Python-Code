import requests
import calendar
from datetime import date


def get_12_month_date(s_date, e_date):
    start_date = date.fromisoformat(s_date)
    end_date = date.fromisoformat(e_date)
    start_year = start_date.year
    end_year = end_date.year
    start_month = start_date.month
    end_month = end_date.month


    for year in range(start_year, end_year + 1):
        month_start = start_month if year == start_year else 1
        month_end = end_month if year == end_year else 12

        for month in range(month_start, month_end + 1):
            month_start_date = date(year, month, 1)
            num_days = calendar.monthrange(year, month)[1]
            month_end_date = date(year, month, num_days)
            if month_start_date < start_date:
                month_start_date = start_date
            if month_end_date > end_date:
                month_end_date = end_date
            month_name = calendar.month_name[month]
            Start_Date = month_start_date.strftime('%Y-%m-%d')
            End_Date = month_end_date.strftime('%Y-%m-%d')
            print(Start_Date)

if __name__ == '__main__':
    startDate = "2025-07-01"
    endDate = "2025-09-30"
    get_12_month_date(startDate, endDate)

