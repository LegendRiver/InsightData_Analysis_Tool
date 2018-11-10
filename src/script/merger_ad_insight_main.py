import os.path
import pandas as pd
import time

from insight_analysis.util import file_helper as fhelper
from insight_analysis.util import common_helper as chelper
from insight_analysis.handler.export_excel_handler import ExcelExporter
from insight_analysis.manager.env_manager import EnvManager
from insight_analysis.handler.handler_factory import HandlerFactory
from insight_analysis.constants import common_constants as mconstant
from insight_analysis.constants import insight_field_constants as iconstant


def read_ad_insight_day(insight_data_files, data_handler, campaign_id=''):
    insight_datas = [data_handler.read_insight_data(file_path) for file_path in insight_data_files]
    all_insight_data = pd.concat(insight_datas)
    data_per_day = data_handler.get_insight_data_per_day(all_insight_data)

    if campaign_id.strip():
        campaign_id = int(campaign_id)
        data_per_day = data_per_day[data_per_day[iconstant.INSIGHT_FIELD_CAMPAIGN_ID] == campaign_id]

    return data_per_day


def parse_ad_name(ad_name):
    name_list = []

    if len(name_list):
        for name in name_list:
            if chelper.string_contains(name, ad_name):
                return name
    else:
        first_name = ad_name.split(' - ')[0]
        return first_name


def group_by_name(insight_data, contain_str=''):
    insight_data = insight_data.drop([iconstant.INSIGHT_FIELD_AD_ID, iconstant.INSIGHT_FIELD_CAMPAIGN_NAME,
                                      iconstant.INSIGHT_FIELD_ADSET_NAME, iconstant.INSIGHT_FIELD_ADSET_ID,
                                      iconstant.INSIGHT_FIELD_CAMPAIGN_ID], axis=1)
    if contain_str.strip():
        is_contain = insight_data[iconstant.INSIGHT_FIELD_AD_NAME].str.contains(contain_str)
        insight_data = insight_data[is_contain]
        insight_data.drop([iconstant.INSIGHT_FIELD_AD_NAME], axis=1)
        insight_data = insight_data.groupby(level=0).sum()

    else:
        insight_data[iconstant.NEW_FIELD_GROUP_AD_NAME] = map(parse_ad_name,
                                                              insight_data[iconstant.INSIGHT_FIELD_AD_NAME])
        insight_data.drop([iconstant.INSIGHT_FIELD_AD_NAME], axis=1)
        insight_data = insight_data.reset_index()
        insight_data = insight_data.groupby(['index', iconstant.NEW_FIELD_GROUP_AD_NAME], as_index=False).sum()

    insight_data['CTR'] = map(chelper.division_operation, insight_data['inline_link_clicks'], insight_data['impressions'])
    insight_data['CPI'] = map(chelper.division_operation, insight_data['spend'], insight_data['result'])
    insight_data['CPC'] = map(chelper.division_operation, insight_data['spend'], insight_data['inline_link_clicks'])
    insight_data['CPM'] = map(chelper.division_operation, insight_data['spend'] * 1000.0, insight_data['impressions'])

    return insight_data


def read_ad_data(account_id, campaign_id):
    path_manager = EnvManager()
    insight_dir = path_manager.get_insight_dir(mconstant.NODE_TYPE_AD)
    account_dir = os.path.join(insight_dir, account_id)

    config_path = path_manager.get_conf_dir()
    output_path = os.path.join(path_manager.get_output_dir(), mconstant.NODE_TYPE_AD)
    fhelper.make_dir(output_path)

    handler_factory = HandlerFactory(config_path)
    insight_handler = handler_factory.get_insight_handler(mconstant.NODE_TYPE_AD)

    in_act_files = fhelper.get_file_list(account_dir)

    data_per_day = read_ad_insight_day(in_act_files, insight_handler, campaign_id)

    ad_name_key = ''
    group_data = group_by_name(data_per_day, ad_name_key)

    if ad_name_key.strip():
        file_name = account_id + '_' + ad_name_key + '_' + str(time.time()) + '.xlsx'
        act_file = os.path.join(output_path, file_name)
        ExcelExporter.export_data_excel(group_data, act_file)
    else:
        file_name = account_id + '_' + str(time.time()) + '.xlsx'
        act_file = os.path.join(output_path, file_name)
        ExcelExporter.export_excel_by_key(iconstant.NEW_FIELD_GROUP_AD_NAME, iconstant.NEW_FIELD_GROUP_AD_NAME,
                                          group_data, act_file)


if __name__ == '__main__':

    read_ad_data('1202579213151769', '23842622657700616')
