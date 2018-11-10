
from insight_analysis.constants import common_constants as mconstant
from campaign_data_handler import CampaignDataHandler
from ad_data_handler import AdDataHandler
from adset_data_handler import AdsetDataHandler
from campaign_retention_handler import CampaignRetentionHandler
from adset_retention_handler import AdsetRetentionHandler
from ad_retention_handler import AdRetentionHandler


class HandlerFactory:

    def __init__(self, config_path):

        self._config_path = config_path

    def get_insight_handler(self, node_type):

        if node_type == mconstant.NODE_TYPE_CAMPAIGN:
            return CampaignDataHandler(self._config_path)
        elif node_type == mconstant.NODE_TYPE_ADSET:
            return AdsetDataHandler(self._config_path)
        elif node_type == mconstant.NODE_TYPE_AD:
            return AdDataHandler(self._config_path)

    def get_retention_handler(self, node_type):
        if node_type == mconstant.NODE_TYPE_CAMPAIGN:
            return CampaignRetentionHandler(self._config_path)
        elif node_type == mconstant.NODE_TYPE_ADSET:
            return AdsetRetentionHandler(self._config_path)
        elif node_type == mconstant.NODE_TYPE_AD:
            return AdRetentionHandler(self._config_path)

