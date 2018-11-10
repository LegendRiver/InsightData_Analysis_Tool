
import pandas as pd
from insight_analysis.util import file_helper as fhelper
from insight_analysis.util import common_helper as chelper
from insight_analysis.constants import profit_constants as pconstants


class ReadExcelDataHandler:

    def __init__(self):
        pass

    @staticmethod
    def read_facebook_data(facebook_file):

        sheet_names = fhelper.get_excel_sheet_names(facebook_file)
        xls = pd.ExcelFile(facebook_file)

        facebook_data = {}
        for name in sheet_names:
            sheet_data = pd.read_excel(xls, name, parse_cols=pconstants.FACEBOOK_COL_INDEX)

            sheet_data[pconstants.FACEBOOK_COL_DATE] = sheet_data[pconstants.FACEBOOK_COL_DATE]. apply(str).\
                apply(chelper.covert_date_format).apply(pd.to_datetime)

            facebook_data[name] = sheet_data

        return facebook_data

    @staticmethod
    def read_appflyer_data(appflyer_file):

        sheet_names = fhelper.get_excel_sheet_names(appflyer_file)
        xls = pd.ExcelFile(appflyer_file)

        appsflyer_data = {}
        for name in sheet_names:
            sheet_data = pd.read_excel(xls, name, parse_cols=pconstants.APPSFLYER_COL_INDEX)
            sheet_data[pconstants.APPSFLYER_COL_DATE] = sheet_data[pconstants.APPSFLYER_COL_DATE].apply(pd.to_datetime)

            sheet_data[pconstants.APPSFLYER_COL_DAY1_RETENTION] = map(
                chelper.division_operation, sheet_data[pconstants.APPSFLYER_COL_DAY1_ACTION],
                sheet_data[pconstants.APPSFLYER_COL_INSTALL])

            appsflyer_data[name] = sheet_data

        return appsflyer_data

    @staticmethod
    def read_typany_retention(typany_file):

        sheet_names = fhelper.get_excel_sheet_names(typany_file)
        sheet_names.pop(0)
        xls = pd.ExcelFile(typany_file)

        data_list = []
        for name in sheet_names:
            sheet_data = pd.read_excel(xls, name, parse_cols='A,B,E,F')
            data_list.append(sheet_data)

        all_data = pd.concat(data_list)
        return all_data


