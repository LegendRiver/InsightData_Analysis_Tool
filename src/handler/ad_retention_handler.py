
from retention_handler import AbstractRetentionHandler
from insight_analysis.constants import insight_field_constants as iconstant


class AdRetentionHandler(AbstractRetentionHandler):

    @property
    def _name(self):
        return iconstant.INSIGHT_FIELD_AD_NAME

    @property
    def _id(self):
        return iconstant.INSIGHT_FIELD_AD_ID

    @property
    def _common_field(self):
        return self.config_manager.ad_common_field

