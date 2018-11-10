
from insight_analysis.manager.env_manager import EnvManager
from insight_analysis.constants import common_constants as mconstant
import os.path as ospath
from insight_analysis.util import file_helper as fhelper
from insight_analysis.util import common_helper as mhelper
import re
import pandas as pd
import numpy as np
from insight_analysis.common.eli_logger import EliLogger


class InsightReader:

    def __init__(self, account_id, handler_factory, start_date='', end_date='', node_types=None, insight_path=''):
        self._path_manager = EnvManager()
        self._handler_factory = handler_factory
        self._current_act_id = account_id
        self._all_data = {}
        self._all_handler = {}
        self._start_date = start_date
        self._end_date = end_date
        if not end_date:
            self._end_date = mhelper.get_now_date()

        if node_types:
            self._node_type = node_types
        else:
            self._node_type = [mconstant.NODE_TYPE_CAMPAIGN, mconstant.NODE_TYPE_ADSET, mconstant.NODE_TYPE_AD]

        self._insight_path = insight_path

        self._read_all_data()

    def read_daily_data(self, node_type, start_date='', end_date=''):
        if node_type not in self._all_handler:
            return None

        if node_type not in self._all_data:
            return None

        handler = self._all_handler[node_type]
        insight_data = self._all_data[node_type]
        data_per_day = handler.get_insight_data_per_day(insight_data)

        if not end_date:
            end_date = self._end_date
        index_mask = np.logical_and(data_per_day.index >= start_date, data_per_day.index <= end_date)
        filter_data = data_per_day[index_mask]
        return filter_data

    def read_hourly_data(self, node_type, start_date='', end_date=''):
        if node_type not in self._all_handler:
            return None

        if node_type not in self._all_data:
            return None

        handler = self._all_handler[node_type]
        insight_data = self._all_data[node_type]
        increment_data = handler.read_increment_by_data(insight_data)

        hour_data = handler.get_increment_per_hour(increment_data)
        if not end_date:
            end_date = self._end_date
        start_object = mhelper.convert_str_date(start_date, '%Y-%m-%d').date()
        end_object = mhelper.convert_str_date(end_date, '%Y-%m-%d').date()
        index_mask = np.logical_and(hour_data.index.date >= start_object, hour_data.index.date <= end_object)
        filter_data = hour_data[index_mask]
        return filter_data

    def _read_all_data(self):
        for ntype in self._node_type:
            data_handler = self._handler_factory.get_insight_handler(ntype)
            file_list = self._get_file_list(ntype)
            insight_datas = [data_handler.read_insight_data(file_path, self._current_act_id) for file_path in file_list]
            if not insight_datas:
                continue

            all_insight_data = pd.concat(insight_datas)
            self._all_data[ntype] = all_insight_data
            self._all_handler[ntype] = data_handler

    def _get_file_list(self, node_type):
        node_dir = self._path_manager.get_insight_dir(node_type, self._insight_path)
        account_dir = ospath.join(node_dir, self._current_act_id)
        node_files = fhelper.get_file_list(account_dir)
        filtered_files = [path for path in node_files if self._filter_file(path)]
        return filtered_files

    def _filter_file(self, file_path):
        date_dirname = ospath.basename(file_path)
        pattern = '\d+-\d+-\d+'
        search_date = re.search(pattern, date_dirname)
        if not search_date:
            return True

        date_dir = search_date.group()
        if self._start_date <= date_dir <= self._end_date:
            return True
        else:
            return False



