from insight_analysis.common.singleton_class import Singleton
from insight_analysis.util import file_helper as fhelper
from insight_analysis.constants import config_constants as cconstant
import os.path


class ConfigManager:

    __metaclass__ = Singleton

    def __init__(self, config_path):
        # insight config
        insight_file = os.path.join(config_path, cconstant.INSIGHT_CONFIG_NAME)
        insight_info = fhelper.read_json_file(insight_file)
        self.campaign_common_field = insight_info[cconstant.CAM_COMMON_FIELD]
        self.adset_common_field = insight_info[cconstant.ADSET_COMMON_FIELD]
        self.ad_common_field = insight_info[cconstant.AD_COMMON_FIELD]
        self.value_field = insight_info[cconstant.VALUE_FIELD]
        self.start_time = insight_info[cconstant.VALID_TIME_START]
        self.insight_sep = insight_info[cconstant.INSIGHT_SEP]
        self.cal_fields = insight_info[cconstant.CAL_FIELD]
        self.act_timezone = insight_info[cconstant.ACCOUNT_TIMEZONE]

        # retention config
        retention_file = os.path.join(config_path, cconstant.RETENTION_CONFIG_NAME)
        retention_info = fhelper.read_json_file(retention_file)
        self.retention_value_field = retention_info[cconstant.RETENTION_VALUE_FIELD]




