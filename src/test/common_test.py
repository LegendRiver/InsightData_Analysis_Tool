
from insight_analysis.util import file_helper as fhelper
import pandas as pd
from insight_analysis.util import common_helper as chelper
from insight_analysis.common.eli_logger import EliLogger

import os.path
from datetime import datetime
from dateutil import tz


def timezone_test():
    # from_zone = tz.gettz('Asia/Shanghai')
    from_zone = tz.gettz('Europe/London')
    to_zone = tz.gettz('Asia/Jakarta')

    date = datetime.strptime('2017-07-01 10:54:22', '%Y-%m-%d %H:%M:%S')
    print date
    date = date.replace(tzinfo=from_zone)
    print date

    central = date.astimezone(to_zone)
    print central


def read_json_test():
    current_path = os.path.dirname(os.path.realpath(__file__))
    root_path = os.path.dirname(current_path)
    json_file = os.path.join(root_path, 'conf', 'insight_analysis_config.json')

    json_data = fhelper.read_json_file(json_file)
    print json_data


def date_mark_test():
    test_list = pd.date_range('20170401', periods=6)
    print test_list

    mark_result = chelper.mark_date_series(test_list, '', '')
    print mark_result


def date_test():
    date = chelper.get_delta_date(-2)
    print date


def log_test():
    EliLogger.instance().info('sss')
    EliLogger.instance().warn('sss')
    EliLogger.instance().error('sss')
    EliLogger.instance().debug('sss')

if __name__ == '__main__':
    timezone_test()
