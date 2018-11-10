from abc import ABCMeta, abstractproperty

import pandas as pd
import numpy as np

from insight_analysis.manager.config_manager import ConfigManager
from insight_analysis.constants import insight_field_constants as iconstant
from insight_analysis.constants import config_constants as cconstant
from insight_analysis.constants import common_constants as cmconstant
from insight_analysis.util import common_helper as chelper


class AbstractDataHandler:
    __metaclass__ = ABCMeta

    def __init__(self, config_path):
        self.config_manager = ConfigManager(config_path)

    @abstractproperty
    def _common_field(self):
        pass

    @abstractproperty
    def _id(self):
        pass

    @abstractproperty
    def _name(self):
        pass

    @property
    def _value_field(self):
        return self.config_manager.value_field

    def read_insight_data(self, insight_file, account_id=''):
        insight_data = pd.read_csv(insight_file, sep=self.config_manager.insight_sep)
        # insight_data = insight_data[
        #     insight_data[iconstant.INSIGHT_FIELD_REQUEST_TIME] > self.config_manager.start_time]
        request_date_time = insight_data[iconstant.INSIGHT_FIELD_END_DATE] + " " + \
                            insight_data[iconstant.INSIGHT_FIELD_REQUEST_TIME]
        convert_timezone = self._get_timezone(account_id)
        index_datetime = request_date_time.apply(chelper.convert_timezone, to_tz=convert_timezone)
        insight_data.index = pd.to_datetime(index_datetime, format='%Y-%m-%d %H:%M:%S')
        insight_data.fillna(0, inplace=True)

        common_field_list = self._common_field + self._value_field
        insight_data = insight_data[common_field_list]
        insight_data[self._common_field] = insight_data[self._common_field].applymap(str)

        return insight_data

    def get_insight_data_per_day(self, result_data):
        insight_ids = result_data[self._id].unique()
        all_data_list = []

        for cid in insight_ids:
            one_insight_data = result_data[result_data[self._id] == cid]
            df_data = pd.DataFrame()

            for field_name in self._value_field:
                field_data = one_insight_data[field_name].resample('D').apply(np.max)
                df_data[field_name] = field_data

            self._append_common_field_data(one_insight_data, df_data)
            all_data_list.append(df_data)

        return pd.concat(all_data_list)

    def read_insight_increment(self, insight_file, account_id=''):
        insight_data = self.read_insight_data(insight_file, account_id)
        return self.read_increment_by_data(insight_data)

    def read_increment_by_data(self, insight_data):
        insight_ids = insight_data[self._id].unique()
        increment_list = []
        for cid in insight_ids:
            one_insight_data = insight_data[insight_data[self._id] == cid]
            date_data = self._increment_multi_date(one_insight_data)
            if date_data is None:
                continue
            increment_list.append(date_data)

        if increment_list:
            return pd.concat(increment_list)
        else:
            return None

    def _increment_multi_date(self, insight_data):
        date_list = pd.unique(insight_data.index.date)
        all_date_list = []
        for index_date in date_list:
            date_data = insight_data[insight_data.index.date == index_date]
            insight_increment = date_data[self._common_field].copy()
            for field_name in self._value_field:
                field_data = date_data[field_name]
                diff_data = chelper.get_diff_data(field_data)
                insight_increment.loc[:, field_name] = diff_data
            all_date_list.append(insight_increment)

        if all_date_list:
            return pd.concat(all_date_list)
        else:
            return None

    def get_increment_per_hour(self, increment_data):
        insight_ids = increment_data[self._id].unique()
        all_data_list = []
        for cid in insight_ids:
            one_insight_data = increment_data[increment_data[self._id] == cid]
            increment_list = []
            for field_name in self._value_field:
                field_data = self._get_hour_data(one_insight_data, field_name)
                increment_list.append(field_data)

            if not increment_list:
                continue
            combine_data = pd.concat(increment_list, axis=1)
            self._append_cal_field(combine_data)
            self._append_common_field_data(one_insight_data, combine_data)
            all_data_list.append(combine_data)
        if all_data_list:
            return pd.concat(all_data_list)
        else:
            return None

    def get_increment_mean(self, increment_data):
        insight_ids = increment_data[self._id].unique()
        all_data_list = []

        for cid in insight_ids:
            one_insight_data = increment_data[increment_data[self._id] == cid]
            mean_list = []
            for field_name in self._value_field:
                field_data = self._get_hour_data(one_insight_data, field_name)
                mean_data = self._get_hour_mean(field_data, field_name)
                mean_list.append(mean_data)

            if not mean_list:
                continue
            combine_data = pd.concat(mean_list, axis=1)
            self._append_cal_field(combine_data)
            self._append_common_field_data(one_insight_data, combine_data)
            all_data_list.append(combine_data)
        if all_data_list:
            return pd.concat(all_data_list)
        else:
            return None

    def _get_timezone(self, act_id):
        if not act_id:
            return cmconstant.DEFAULT_TIMEZONE

        timezone_map = self.config_manager.act_timezone
        if act_id in timezone_map:
            return timezone_map[act_id]
        else:
            return cmconstant.DEFAULT_TIMEZONE

    def _append_common_field_data(self, original_data, output_data):
        row_count = len(output_data.index)
        for field_name in self._common_field:
            name_series = original_data[field_name].values
            field_value = name_series[0]
            output_data[field_name] = [field_value] * row_count

    def _append_cal_field(self, df_data):
        cal_fields = self.config_manager.cal_fields
        df_columns = df_data.columns

        for field_name, operand_dict in cal_fields.items():
            is_mean = operand_dict[cconstant.IS_MEAN]
            multiple = operand_dict[cconstant.MULTIPLE]
            operand_one_name = operand_dict[cconstant.OPERAND_ONE]
            operand_two_name = operand_dict[cconstant.OPERAND_TWO]
            if operand_one_name in df_columns and operand_two_name in df_columns:
                df_data[field_name] = map(chelper.division_operation,
                                          df_data[operand_one_name].apply(lambda x: x * multiple),
                                          df_data[operand_two_name])

            if is_mean:
                operand_one_name += iconstant.FIELD_MEAN_POSTFIX
                operand_two_name += iconstant.FIELD_MEAN_POSTFIX
                if operand_one_name in df_columns and operand_two_name in df_columns:
                    df_data[field_name] = map(chelper.division_operation,
                                              df_data[operand_one_name].apply(lambda x: x * multiple),
                                              df_data[operand_two_name])

    @staticmethod
    def _get_hour_mean(hour_data, field_name):
        hour_data[iconstant.NEW_FIELD_HOUR] = hour_data.index.hour

        mean_data = hour_data.groupby(iconstant.NEW_FIELD_HOUR).mean()
        mean_new_name = field_name + iconstant.FIELD_MEAN_POSTFIX
        mean_data.rename(columns={field_name: mean_new_name}, inplace=True)
        round_mean = mean_data.round({mean_new_name: 2})

        std_data = hour_data.groupby(iconstant.NEW_FIELD_HOUR).std()
        std_new_name = field_name + iconstant.FIELD_STD_POSTFIX
        std_data.rename(columns={field_name: std_new_name}, inplace=True)
        round_std = std_data.round({std_new_name: 2})

        return pd.concat([round_mean, round_std], axis=1)

    @staticmethod
    def _get_hour_data(original_data, field):
        hour_data = original_data[field].resample('H').apply(np.sum)
        hour_data.dropna(inplace=True)
        hour_data = pd.DataFrame(hour_data.T)
        return hour_data
