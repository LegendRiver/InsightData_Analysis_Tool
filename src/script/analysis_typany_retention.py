
from insight_analysis.manager.env_manager import EnvManager
from insight_analysis.profit_handler.read_excel_data import ReadExcelDataHandler
import os.path as ospath
import pandas as pd


def analysis_typany_retention():
    path_manager = EnvManager()
    resource_path = path_manager.get_resource_dir()
    typany_path = ospath.join(resource_path, 'typany')
    retention_file = ospath.join(typany_path, 'retention_typany.xlsx')
    retention_data = ReadExcelDataHandler.read_typany_retention(retention_file)
    # pivot_data = pd.pivot_table(retention_data, index=['Date', 'Country'], values=['Install Day', 'Day 1'],
    #                             aggfunc=np.sum, fill_value=0)
    pivot_data = retention_data.groupby(['Date', 'Country'], as_index=False).sum()

    output_dir = path_manager.get_output_dir()
    output_file = ospath.join(output_dir, 'typany.xlsx')
    writer = pd.ExcelWriter(output_file)
    pivot_data.to_excel(writer, 'retention')
    writer.save()

if __name__ == '__main__':

    analysis_typany_retention()
