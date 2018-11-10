import os.path
import pandas as pd
import time

from insight_analysis.util import file_helper as fhelper
from insight_analysis.handler.export_excel_handler import ExcelExporter
from insight_analysis.manager.env_manager import EnvManager
from insight_analysis.handler.handler_factory import HandlerFactory
from insight_analysis.constants import common_constants as mconstant
from insight_analysis.util import data_helper as dhelper


def read_insight_per_day(insight_data_files, data_handler, output_path, node_type, act_id=''):
    insight_datas = [data_handler.read_insight_data(file_path, account_id=act_id) for file_path in insight_data_files]
    if not insight_datas:
        return None
    all_insight_data = pd.concat(insight_datas)
    data_per_day = data_handler.get_insight_data_per_day(all_insight_data)
    ExcelExporter.export_excel_by_key(dhelper.get_key_id(node_type), dhelper.get_key_id(node_type),
                                      data_per_day, output_path)
    return data_per_day


def read_insight_hour_increment(insight_data_files, data_handler, output_path, node_type, act_id=''):
    insight_datas = [data_handler.read_insight_increment(file_path, act_id) for file_path in insight_data_files]
    all_insight_data = pd.concat(insight_datas)

    data_per_day = data_handler.get_increment_mean(all_insight_data)
    ExcelExporter.export_excel_by_key(dhelper.get_key_id(node_type), dhelper.get_key_id(node_type),
                                      data_per_day, output_path)


def read_all_account_data(node_type):
    path_manager = EnvManager()
    insight_dir = path_manager.get_insight_dir(node_type)
    account_list = fhelper.get_subdir_name_list(insight_dir)

    config_path = path_manager.get_conf_dir()
    output_path = os.path.join(path_manager.get_output_dir(), node_type)
    fhelper.make_dir(output_path)

    handler_factory = HandlerFactory(config_path)
    insight_handler = handler_factory.get_insight_handler(node_type)

    for account_id in account_list:
        in_act_dir = os.path.join(insight_dir, account_id)
        in_act_files = fhelper.get_file_list(in_act_dir)

        file_name = account_id + '_' + str(time.time()) + '.xlsx'
        act_file = os.path.join(output_path, file_name)

        read_insight_per_day(in_act_files, insight_handler, act_file, node_type, account_id)


if __name__ == '__main__':

    read_all_account_data(mconstant.NODE_TYPE_ADSET)



