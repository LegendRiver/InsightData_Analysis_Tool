
from insight_analysis.common.singleton_class import Singleton
from insight_analysis.constants import common_constants as mconstant
from insight_analysis.util import file_helper as fhelper
import os.path


class EnvManager:

    __metaclass__ = Singleton

    def __init__(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.analysis_path = os.path.dirname(current_path)
        self.resource_path = os.path.join(self.analysis_path, mconstant.DIR_RESOURCES)

        conf_path = self.get_conf_dir()
        env_file = os.path.join(conf_path, 'env_conf.json')
        self.env_info = fhelper.read_json_file(env_file)

    def get_insight_dir(self, node_type, resource_path=''):
        insight_dir = ''
        if not resource_path:
            resource_path = self.resource_path

        if node_type == mconstant.NODE_TYPE_CAMPAIGN:
            insight_dir = os.path.join(resource_path, mconstant.DIR_CAMPAIGN_INSIGHT)
        elif node_type == mconstant.NODE_TYPE_ADSET:
            insight_dir = os.path.join(resource_path, mconstant.DIR_ADSET_INSIGHT)
        elif node_type == mconstant.NODE_TYPE_AD:
            insight_dir = os.path.join(resource_path, mconstant.DIR_AD_INSIGHT)
        return insight_dir

    def get_retention_dir(self, node_type):
        retention_dir = ''
        if node_type == mconstant.NODE_TYPE_CAMPAIGN:
            retention_dir = os.path.join(self.resource_path, mconstant.DIR_CAMPAIGN_RETENTION)
        elif node_type == mconstant.NODE_TYPE_ADSET:
            retention_dir = os.path.join(self.resource_path, mconstant.DIR_ADSET_RETENTION)
        elif node_type == mconstant.NODE_TYPE_AD:
            retention_dir = os.path.join(self.resource_path, mconstant.DIR_AD_RETENTION)
        return retention_dir

    def get_conf_dir(self):

        return os.path.join(self.analysis_path, mconstant.DIR_CONF)

    def get_output_dir(self):

        return os.path.join(self.analysis_path, mconstant.DIR_OUTPUT)

    def get_360_retention_dir(self):

        return os.path.join(self.resource_path, mconstant.DIR_360_RETENTION)

    def get_profit_resource_dir(self):

        return os.path.join(self.resource_path, mconstant.DIR_PROFIT_RESOURCE)

    def get_profit_handler_dir(self):

        return os.path.join(self.analysis_path, mconstant.DIR_PROFIT_HANDLER)

    def get_resource_dir(self):
        return self.resource_path

    def get_log_path(self):
        if mconstant.ENV_LOG_PATH in self.env_info:
            return self.env_info[mconstant.ENV_LOG_PATH]
        else:
            return ''

    def get_log_names(self):
        if mconstant.ENV_LOG_NAME in self.env_info:
            return self.env_info[mconstant.ENV_LOG_NAME]
        else:
            return [mconstant.LOG_NAME_ANALYSIS]

