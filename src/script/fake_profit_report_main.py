
import append_sys_path
from insight_analysis.manager.env_manager import EnvManager
from insight_analysis.profit_handler.fake_data_handler import FakeDataHandler
from insight_analysis.profit_handler.read_excel_data import ReadExcelDataHandler
from insight_analysis.util import common_helper as comhelper
import os.path as ospath
import pandas as pd
import sys


def export_spend_report(delta_days):
    path_manager = EnvManager()
    latest_date = comhelper.get_delta_date(int(delta_days))
    profit_resource_dir = ospath.join("/var/www/html/eli/server/fakeProfitData", latest_date)
    # profit_resource_dir = path_manager.get_profit_resource_dir()
    facebook_file = ospath.join(profit_resource_dir, 'facebook_data.xlsx')

    profit_handler_dir = path_manager.get_profit_handler_dir()
    config_dir = ospath.join(profit_handler_dir, 'kpi_conf')
    af_handler = FakeDataHandler(config_dir, 'fake_super_conf.json')

    # output_dir = path_manager.get_output_dir()
    output_dir = ospath.join("/var/www/html/eli/server/fakeProfitData", latest_date)

    facebook_data = ReadExcelDataHandler.read_facebook_data(facebook_file)

    calculate_data = af_handler.calculate_income(facebook_data)
    pivot_data = af_handler.group_data_by_country(calculate_data)

    _save_data_to_excel(output_dir, calculate_data, pivot_data)


def _save_data_to_excel(output_dir, full_data, pivot_data):
    output_file = ospath.join(output_dir, 'profit.xlsx')
    writer = pd.ExcelWriter(output_file)
    product_names = full_data.keys()
    for key in product_names:
        if key in pivot_data:
            sheet_name = 'profit_data_' + key
            pivot_data[key].to_excel(writer, sheet_name)

        if key in full_data:
            sheet_name = 'all_data_' + key
            full_data[key].to_excel(writer, sheet_name)

    writer.save()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        days = -1
    else:
        days = sys.argv[1]
    export_spend_report(days)
