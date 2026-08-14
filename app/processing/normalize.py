import datetime as dt

pfl = [
    {"date": "Sat, Aug 22", "title": "PFL Tampa"},
    {"date": "Fri, Oct 2", "title": "PFL MENA 11"},
    {"date": "Sat, Oct 10", "title": "PFL Africa Morocco"},
]
DATE_FORMATS = {
    "pfl": "%a, %b %d, %Y",
    "ufc": "%b %d, %Y",
    "rizin": "%Y年%m月%d日",
}


def normalize_dates(data, source):
    current_year = dt.datetime.now().year
    date_format = DATE_FORMATS[source]

    for event_info in data:
        date_string = event_info["date"]

        if source == "pfl":
            date_string = date_string + ", " + str(current_year)
            date_obj = dt.datetime.strptime(date_string, date_format)
        else:
            date_obj = dt.datetime.strptime(date_string, date_format)

        event_info["date"] = date_obj.strftime("%Y-%m-%d")

