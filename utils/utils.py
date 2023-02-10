import sys
sys.path.insert(0, '.')

from datetime import datetime
import pytz

class DateTimeUtils:

    def convert_utc_to_pst(self, utc_time):
        utc_time                    = pytz.utc.localize(utc_time)
        pst_time_datetime_instance  = utc_time.astimezone(pytz.timezone("US/Pacific"))
        pst_time                    = pst_time_datetime_instance.strftime("%Y-%m-%d %H:%M:%S")

        return pst_time