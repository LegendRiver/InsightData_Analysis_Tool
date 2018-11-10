from insight_analysis.manager.env_manager import EnvManager
from insight_analysis.handler.export_excel_handler import ExcelExporter
from insight_analysis.util import common_helper as comhelper
import os.path as ospath
import pandas as pd


def export_conversion(resource_root_path, output_root_path):
    install_file = ospath.join(resource_root_path, 'install_data.xlsx')
    conversion_file = ospath.join(resource_root_path, 'conversion.csv')

    conversion_cols = ['Campaign', 'Campaign ID', 'Conversions', 'All conv.', 'Cost']
    conversion_data = pd.read_csv(conversion_file, header=5, usecols=conversion_cols)
    conversion_data = conversion_data[:-1]
    conversion_data['Conversions'] = conversion_data['Conversions'].apply(str.replace, args=(',', '')).apply(float)
    conversion_data['All conv.'] = conversion_data['All conv.'].apply(str.replace, args=(',', '')).apply(float)
    conversion_data['Cost'] = conversion_data['Cost'].apply(str.replace, args=(',', '')).apply(float)

    install_data = pd.read_excel(install_file, parse_cols="B, C")
    install_data['campaign'] = install_data['campaign'].apply(str)
    install_data.rename(columns={'campaign': 'Campaign ID', 'install': 'AF Install'}, inplace=True)

    merger_data = pd.merge(conversion_data, install_data, on='Campaign ID', how='outer')
    merger_data.fillna(0, inplace=True)
    merger_data['Other Conversion'] = merger_data['All conv.'] - merger_data['Conversions']
    merger_data['Cost/AF'] = map(comhelper.division_operation, merger_data['Cost'], merger_data['AF Install'])
    merger_data['Cost/Coversion'] = map(comhelper.division_operation, merger_data['Cost'], merger_data['Conversions'])
    merger_data['Cost/All'] = map(comhelper.division_operation, merger_data['Cost'], merger_data['All conv.'])
    merger_data['Cost/Other'] = map(comhelper.division_operation, merger_data['Cost'], merger_data['Other Conversion'])

    export_data = merger_data[['Campaign ID', 'Campaign', 'AF Install', 'Conversions', 'All conv.', 'Other Conversion',
                               'Cost', 'Cost/AF', 'Cost/Coversion', 'Cost/All', 'Cost/Other']]

    date_str = comhelper.get_delta_date(-1)
    file_name = 'adword_conversion_' + date_str + '.xlsx'
    export_file = ospath.join(output_root_path, file_name)
    ExcelExporter.export_data_excel(export_data, export_file)


if __name__ == '__main__':
    path_manager = EnvManager()
    resource_path = path_manager.get_resource_dir()
    conversion_path = ospath.join(resource_path, 'aw_conversion')
    output_path = path_manager.get_output_dir()
    export_conversion(conversion_path, output_path)
