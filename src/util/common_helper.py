import numpy as np
import os.path
from datetime import datetime
from datetime import timedelta
import pytz
from dateutil import tz
from insight_analysis.constants import common_constants as cmconstants


def division_operation(dividend, divisor, decimals=4):
    if 0 == divisor:
        return 0
    else:
        return round(dividend/float(divisor), decimals)


def get_diff_data(original_data):
    data_size = original_data.size
    data_array = original_data.values
    shift_data = np.concatenate((np.array([0]), data_array[:data_size-1]))
    diff_data = data_array - shift_data
    return diff_data


def get_retention_date(file_path):
    file_name = os.path.basename(file_path)
    start_index = file_name.rfind('_')
    end_index = file_name.rfind('.')
    return file_name[start_index+1: end_index]


def convert_str_date(date_str, format_str='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(date_str, format_str)


def get_now_date(format_str='%Y-%m-%d', timezone_str=cmconstants.DEFAULT_TIMEZONE):
    timezone = pytz.timezone(timezone_str)
    return datetime.now(timezone).strftime(format_str)


def get_delta_date(days, timezone_str=cmconstants.DEFAULT_TIMEZONE):
    timezone = pytz.timezone(timezone_str)
    date_time = datetime.now(timezone) + timedelta(days=days)
    return date_time.strftime('%Y-%m-%d')


def covert_date_format(date_str, original_format='%Y%m%d', to_format='%Y-%m-%d'):
    date_int_time = datetime.strptime(date_str, original_format)
    return date_int_time.strftime(to_format)


def convert_timezone(date_time_str, to_tz, from_tz=cmconstants.DEFAULT_TIMEZONE, from_format='%Y-%m-%d %H:%M:%S',
                     to_format='%Y-%m-%d %H:%M:%S'):
    from_zone = tz.gettz(from_tz)
    to_zone = tz.gettz(to_tz)

    date = datetime.strptime(date_time_str, from_format)
    replace_date = date.replace(tzinfo=from_zone)
    to_date = replace_date.astimezone(to_zone)

    result_date = to_date.strftime(to_format)
    return result_date


def string_contains(substring, srcstring):
    if not substring or not srcstring:
        return False

    if srcstring.find(substring) >= 0:
        return True
    else:
        return False


def mark_date_series(data, start_date, end_date):
    if start_date.strip():
        start_datetime = convert_str_date(start_date, '%Y-%m-%d')
    else:
        start_datetime = datetime.min

    if end_date.strip():
        end_datetime = convert_str_date(end_date, '%Y-%m-%d')
    else:
        end_datetime = datetime.max

    return [start_datetime <= item <= end_datetime for item in data]



