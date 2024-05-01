from datetime import datetime

def convert_timesnap(timesnap):
    dt_object = datetime.fromtimestamp(timesnap)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")


#print(convert_timesnap("1714523336.8762164"))