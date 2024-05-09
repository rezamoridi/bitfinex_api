from datetime import datetime

def convert_timesnap(timesnap):
    dt_object = datetime.fromtimestamp(timesnap)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")


def convert_timesnap_time(timesnap):
    dt_object = datetime.fromtimestamp(timesnap)
    return dt_object.strftime("%H:%M:%S")