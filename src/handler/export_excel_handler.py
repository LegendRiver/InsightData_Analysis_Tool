
import pandas as pd
import os.path
from insight_analysis.common.eli_logger import EliLogger


class ExcelExporter:

    def __init__(self):
        pass

    @staticmethod
    def export_excel_by_key(key_field, name_field, export_data, export_path):
        data_keys = export_data[key_field].unique()

        excel_writer = pd.ExcelWriter(export_path)

        for ckey in data_keys:
            one_key_data = export_data[export_data[key_field] == ckey]
            name_series = one_key_data[name_field].values
            one_key_data.to_excel(excel_writer, str(name_series[0]))

        excel_writer.save()

    @staticmethod
    def export_merger_retention(key_field, name_field, export_data, export_path):
        date_list = export_data.index.levels[0]
        for re_date in date_list:
            file_name = re_date + '.xlsx'
            file_path = os.path.join(export_path, file_name)

            date_data = export_data.loc[re_date]
            ExcelExporter.export_excel_by_key(key_field, name_field, date_data, file_path)

    @staticmethod
    def export_data_excel(df_data, export_path):

        excel_writer = pd.ExcelWriter(export_path)
        df_data.to_excel(excel_writer)
        excel_writer.save()

    @staticmethod
    def export_multi_data_excel(output_file, data_list, sheet_name_list):
        writer = pd.ExcelWriter(output_file)
        if len(data_list) != len(sheet_name_list):
            EliLogger.instance().warn('The length of data is not equal to the length of sheet name.')
            return
        for i in range(len(data_list)):
            data = data_list[i]
            if data is None:
                continue
            sheet_name = sheet_name_list[i]
            data.to_excel(writer, sheet_name)

        writer.save()

