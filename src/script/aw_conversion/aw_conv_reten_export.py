import append_sys_path
from insight_analysis.manager.env_manager import EnvManager
from insight_analysis.handler.export_excel_handler import ExcelExporter
from insight_analysis.util import common_helper as comhelper
import os.path as ospath
import pandas as pd


def cal_revenue(retention, install):
    if retention >= 0.22:
        return install * 0.8
    elif retention >= 0.15:
        return install * 0.8 * 0.75
    else:
        return 0


def cal_revenue_ru(retention, install):
    if retention >= 0.15:
        return install * 0.55
    elif retention >= 0.1:
        return install * 0.55 * 0.8
    else:
        return 0


def export_conversion(resource_root_path, output_root_path):
    install_file = ospath.join(resource_root_path, 'retention_data.xlsx')
    conversion_file = ospath.join(resource_root_path, 'conversion.csv')

    conversion_cols = ['Day', 'Campaign', 'Campaign ID', 'Conversions', 'All conv.', 'Cost']
    conversion_data = pd.read_csv(conversion_file, usecols=conversion_cols)
    # conversion_data = conversion_data[:-1]
    # conversion_data['Conversions'] = conversion_data['Conversions'].apply(str.replace, args=(',', '')).apply(float)
    # conversion_data['All conv.'] = conversion_data['All conv.'].apply(str.replace, args=(',', '')).apply(float)
    # conversion_data['Cost'] = conversion_data['Cost'].apply(str.replace, args=(',', '')).apply(float)
    conversion_data['Cost'] = conversion_data['Cost']/1000000.0
    conversion_data['Day'] = conversion_data['Day'].apply(pd.to_datetime)
    conversion_data['Campaign ID'] = conversion_data['Campaign ID'].apply(str)

    retention_data = pd.read_excel(install_file, parse_cols="C:F")
    retention_data['country'] = retention_data['country'].apply(str)
    retention_data['date'] = retention_data['date'].apply(pd.to_datetime)
    retention_data.rename(columns={'country': 'Campaign ID', 'install_af': 'AF Install', 'date': 'Day',
                                   'day_1': 'Day 1'}, inplace=True)

    merger_data = pd.merge(conversion_data, retention_data, on=['Day', 'Campaign ID'], how='outer')
    merger_data.fillna(0, inplace=True)
    merger_data['Other Conversion'] = merger_data['All conv.'] - merger_data['Conversions']
    merger_data['Retention'] = map(comhelper.division_operation, merger_data['Day 1'], merger_data['AF Install'])
    merger_data['Cost/AF'] = map(comhelper.division_operation, merger_data['Cost'], merger_data['AF Install'])
    merger_data['Cost/Coversion'] = map(comhelper.division_operation, merger_data['Cost'], merger_data['Conversions'])
    merger_data['Cost/All'] = map(comhelper.division_operation, merger_data['Cost'], merger_data['All conv.'])
    merger_data['Cost/Other'] = map(comhelper.division_operation, merger_data['Cost'], merger_data['Other Conversion'])
    merger_data['Revenue'] = map(cal_revenue_ru, merger_data['Retention'], merger_data['AF Install'])
    # merger_data['Revenue'] = map(cal_revenue, merger_data['Retention'], merger_data['Conversions'])
    merger_data['Profit'] = merger_data['Revenue'] - merger_data['Cost']

    export_data = merger_data[['Day', 'Campaign ID', 'Campaign', 'AF Install', 'Day 1', 'Retention', 'Conversions',
                               'All conv.', 'Other Conversion', 'Cost', 'Cost/AF', 'Cost/Coversion', 'Cost/All',
                               'Cost/Other', 'Revenue', 'Profit']]

    # date_str = comhelper.get_delta_date(-1)
    file_name = 'adword_conversion' + '.xlsx'
    export_file = ospath.join(output_root_path, file_name)
    ExcelExporter.export_data_excel(export_data, export_file)


if __name__ == '__main__':
    # path_manager = EnvManager()
    # resource_path = path_manager.get_resource_dir()
    # conversion_path = ospath.join(resource_path, 'aw_conversion')
    # output_path = path_manager.get_output_dir()
    today = comhelper.get_now_date()
    conversion_path = ospath.join("/var/www/html/eli/server/awConversion", today)
    export_conversion(conversion_path, conversion_path)
