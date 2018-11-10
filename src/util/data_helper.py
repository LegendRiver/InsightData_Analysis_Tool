from insight_analysis.constants import insight_field_constants as iconstant
from insight_analysis.constants import common_constants as mconstant


def get_key_name(node_type):
        if node_type == mconstant.NODE_TYPE_CAMPAIGN:
            return iconstant.INSIGHT_FIELD_CAMPAIGN_NAME
        elif node_type == mconstant.NODE_TYPE_ADSET:
            return iconstant.INSIGHT_FIELD_ADSET_NAME
        elif node_type == mconstant.NODE_TYPE_AD:
            return iconstant.INSIGHT_FIELD_AD_NAME


def get_key_id(node_type):
    if node_type == mconstant.NODE_TYPE_CAMPAIGN:
        return iconstant.INSIGHT_FIELD_CAMPAIGN_ID
    elif node_type == mconstant.NODE_TYPE_ADSET:
        return iconstant.INSIGHT_FIELD_ADSET_ID
    elif node_type == mconstant.NODE_TYPE_AD:
        return iconstant.INSIGHT_FIELD_AD_ID
