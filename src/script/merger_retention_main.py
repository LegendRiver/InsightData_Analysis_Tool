
from insight_analysis.handler.merger_data_handler import MergerDataHandler
from insight_analysis.manager.env_manager import EnvManager
from insight_analysis.util import file_helper as fhelper
from insight_analysis.handler.export_excel_handler import ExcelExporter
from insight_analysis.constants import common_constants as mconstant
from insight_analysis.util import data_helper as dhelper

import os.path


def merger_all_account_data(node_type):
    path_manager = EnvManager()
    insight_dir = path_manager.get_insight_dir(node_type)
    retention_dir = path_manager.get_retention_dir(node_type)
    account_list = fhelper.get_subdir_name_list(retention_dir)

    config_path = path_manager.get_conf_dir()
    merger_handler = MergerDataHandler(config_path)

    output_path = os.path.join(path_manager.get_output_dir(), node_type)
    fhelper.make_dir(output_path)

    for account_id in account_list:
        in_act_dir = os.path.join(insight_dir, account_id)
        re_act_dir = os.path.join(retention_dir, account_id)
        in_act_files = fhelper.get_file_list(in_act_dir)
        re_act_files = fhelper.get_file_list(re_act_dir)
        merger_data = merger_handler.merger_in_re_per_day(in_act_files, re_act_files, node_type)

        output_act_path = os.path.join(output_path, account_id)
        fhelper.make_dir(output_act_path)
        ExcelExporter.export_merger_retention(dhelper.get_key_id(node_type), dhelper.get_key_id(node_type), merger_data,
                                              output_act_path)


if __name__ == '__main__':

    merger_all_account_data(mconstant.NODE_TYPE_ADSET)
