import datetime as dt

DATE_FORMATS = {
    "pfl": "%a, %b %d, %Y",
    "ufc": "%b %d, %Y",
    "rizin": "%Y年%m月%d日",
    "one_fc": "%Y",
}


def normalize_dates(data, source):
    current_year = dt.datetime.now().year
    date_format = DATE_FORMATS[source]

    for event_info in data:
        date_string = event_info["date"]
        if source == "pfl":
            date_string = date_string + ", " + str(current_year)
            date_obj = dt.datetime.strptime(date_string, date_format)

        elif source == "one_fc":
            unix_timestamp = int(date_string)
            date_obj = dt.datetime.fromtimestamp(
                unix_timestamp, tz=dt.timezone.utc
            ).date()

        else:
            date_obj = dt.datetime.strptime(date_string, date_format)

        event_info["date"] = date_obj.strftime("%Y-%m-%d")

    return data
