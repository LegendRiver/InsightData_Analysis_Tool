
import pandas as pd
import numpy as np
from insight_analysis.constants import insight_field_constants as iconstant
from data_handler import AbstractDataHandler

from abc import ABCMeta


class AbstractRetentionHandler(AbstractDataHandler):

    __metaclass__ = ABCMeta

    @property
    def _value_field(self):
        return self.config_manager.retention_value_field

    def get_retention_per_day(self, file_path):
        retention_data = self._read_retention_data(file_path)
        retention_per_day = self.get_insight_data_per_day(retention_data)
        return retention_per_day

    def _read_retention_data(self, file_path):
        original_data = pd.read_table(file_path, parse_dates=[iconstant.INSIGHT_FIELD_REQUEST_TIME])
        if iconstant.INSIGHT_FIELD_RESULT not in original_data.columns:
            original_data[iconstant.INSIGHT_FIELD_RESULT] = np.zeros((len(original_data.index), 1))
        original_data.fillna(0, inplace=True)
        original_data.set_index(iconstant.INSIGHT_FIELD_REQUEST_TIME, inplace=True)
        field_names = self._common_field + self._value_field
        original_data = original_data[field_names]

        return original_data



