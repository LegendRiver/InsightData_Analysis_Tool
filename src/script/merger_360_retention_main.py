
from insight_analysis.manager.env_manager import EnvManager
from insight_analysis.util import file_helper as fhelper
from insight_analysis.constants import insight_field_constants as iconstant
from insight_analysis.constants import common_constants as mconstant
from insight_analysis.handler.merger_data_handler import MergerDataHandler
from insight_analysis.handler.export_excel_handler import ExcelExporter

import os.path
import pandas as pd
import numpy as np


def get_360_retention_data(retention_file):
    execl_file = pd.ExcelFile(retention_file)
    excel_data = pd.read_excel(execl_file, 0)
    excel_data = excel_data[iconstant.FIELD_360_FILTER]
    excel_data[iconstant.FIELD_360_ADSET] = excel_data[iconstant.FIELD_360_ADSET].str.lower()
    return excel_data


def _diff_app_start(x):
    return np.max(x) - np.min(x)


def _last_value(x):
    return str(x[-1]).lower()


def get_insight_data(act_id, pmanager):
    node_type = mconstant.NODE_TYPE_ADSET
    insight_dir = pmanager.get_insight_dir(node_type)
    retention_dir = pmanager.get_retention_dir(node_type)
    in_act_dir = os.path.join(insight_dir, act_id)
    re_act_dir = os.path.join(retention_dir, act_id)
    in_act_files = fhelper.get_file_list(in_act_dir)
    re_act_files = fhelper.get_file_list(re_act_dir)

    config_path = pmanager.get_conf_dir()
    merger_handler = MergerDataHandler(config_path)
    merger_in_data = merger_handler.merger_in_re_per_day(in_act_files, re_act_files, node_type)
    merger_in_data.set_index([iconstant.INSIGHT_FIELD_ADSET_ID], append=True, inplace=True)
    grouped_data = merger_in_data.groupby(level=[0, 2]).agg({
        iconstant.INSIGHT_FIELD_RESULT: np.max,
        iconstant.INSIGHT_FIELD_UNIQUE_MOBILE_START: _diff_app_start,
        iconstant.INSIGHT_FIELD_ADSET_NAME: _last_value
    })
    grouped_data = grouped_data.reset_index()
    grouped_data.rename(columns={'level_0': iconstant.FIELD_360_DATE,
                        iconstant.INSIGHT_FIELD_ADSET_NAME: iconstant.FIELD_360_ADSET}, inplace=True)
    grouped_data[iconstant.FIELD_360_DATE] = grouped_data[iconstant.FIELD_360_DATE].astype('datetime64')
    return grouped_data


if __name__ == '__main__':

    path_manager = EnvManager()
    dir_360_retention = path_manager.get_360_retention_dir()
    file_list = fhelper.get_file_list(dir_360_retention)
    output_path = path_manager.get_output_dir()
    account_id = '1227059300703760'
    for advertiser_file in file_list:
        advertiser_data = get_360_retention_data(advertiser_file)
        insight_data = get_insight_data(account_id, path_manager)
        merger_data = pd.merge(advertiser_data, insight_data, how='left',
                               on=[iconstant.FIELD_360_DATE, iconstant.FIELD_360_ADSET])
        merger_data.drop([iconstant.FIELD_360_CAMPAIGN, iconstant.INSIGHT_FIELD_ADSET_ID], axis=1,
                         inplace=True)
        ExcelExporter.export_data_excel(merger_data, os.path.join(output_path, 'merger.xlsx'))

