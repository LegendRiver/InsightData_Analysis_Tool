
from data_handler import AbstractDataHandler
from insight_analysis.constants import insight_field_constants as iconstant


class AdsetDataHandler(AbstractDataHandler):

    @property
    def _name(self):
        return iconstant.INSIGHT_FIELD_ADSET_NAME

    @property
    def _id(self):
        return iconstant.INSIGHT_FIELD_ADSET_ID

    @property
    def _common_field(self):
        return self.config_manager.adset_common_field
