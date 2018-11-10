
from insight_analysis.util import file_helper as fhelper
from insight_analysis.constants import profit_constants as pconstants
from insight_analysis.util import common_helper as comhelper
import pandas as pd
import os.path as opath
import numpy as np


class AFDataHandler:

    def __init__(self, conf_path, super_conf_name):
        self._conf_root_path = conf_path
        super_conf_file = opath.join(self._conf_root_path, super_conf_name)
        super_conf_info = fhelper.read_json_file(super_conf_file)
        self._conf_map = self._read_all_conf_file(super_conf_info)

        self._current_kpi_map = {}
        self._current_check_type = ''

    def calculate_income(self, product_map):
        calculate_result = {}

        for (product_name, product_data) in product_map.items():
            if product_name in self._conf_map:
                config_info = self._conf_map[product_name]
                cal_data = self._calculate_one_product(config_info, product_data)
                cal_data[pconstants.MERGE_COL_PROFIT] = \
                    cal_data[pconstants.MERGER_COL_ACTUAL_PAYMENT] - cal_data[pconstants.FACEBOOK_COL_SPEND]
                calculate_result[product_name] = cal_data

        return calculate_result

    @staticmethod
    def group_data_by_country(product_map):
        pivot_result = {}

        for (product_name, product_data) in product_map.items():
            pivot_data = pd.pivot_table(product_data, index=[pconstants.APPSFLYER_COL_COUNTRY],
                                        values=[pconstants.MERGER_COL_ACTUAL_PAYMENT, pconstants.FACEBOOK_COL_SPEND,
                                        pconstants.MERGE_COL_PROFIT], aggfunc=np.sum, fill_value=0)
            pivot_result[product_name] = pivot_data

        return pivot_result

    def merger_data(self, facebook_data, appsflyer_data):
        merger_data = {}
        for (product_name, fdata) in facebook_data.items():
            if product_name in appsflyer_data:
                config_info = self._conf_map[product_name]
                cal_platform = config_info[pconstants.CONFIG_CAL_PLATFORM]
                if pconstants.CAL_PLATFORM_FB == cal_platform:
                    join_type = 'left'
                else:
                    join_type = 'right'

                adata = appsflyer_data[product_name]
                product_data = pd.merge(fdata, adata, how=join_type, on=[pconstants.APPSFLYER_COL_DATE,
                                                                         pconstants.APPSFLYER_COL_COUNTRY])
                product_data.fillna(0, inplace=True)
                merger_data[product_name] = product_data

        return merger_data

    def _calculate_one_product(self, config_info, product_data):
        data_list = []
        retention_infos = config_info[pconstants.CONFIG_RETENTION_INFO]
        cal_platform = config_info[pconstants.CONFIG_CAL_PLATFORM]
        if pconstants.CAL_PLATFORM_FB == cal_platform:
            install_col = pconstants.FACEBOOK_COL_INSTALL
        else:
            install_col = pconstants.APPSFLYER_COL_INSTALL

        for info in retention_infos:
            self._current_check_type = info[pconstants.CONFIG_CHECK_TYPE]
            start_date = info[pconstants.CONFIG_START_DATE]
            end_date = info[pconstants.CONFIG_END_DATE]
            kpi_infos = info[pconstants.CONFIG_KPI]
            self._current_kpi_map = self._build_kpi_map(kpi_infos)

            sub_data = self._get_sub_data(product_data, start_date, end_date)
            country_data = sub_data[pconstants.APPSFLYER_COL_COUNTRY]
            install_data = sub_data[install_col]
            retention_data = sub_data[pconstants.APPSFLYER_COL_DAY1_RETENTION]
            price_data = map(self._get_price_by_country, country_data, install_data)
            sub_data[pconstants.MERGER_COL_FULL_PAYMENT] = install_data * price_data

            sub_data[pconstants.MERGER_COL_ACTUAL_PAYMENT] = map(self._calculate_actual_payment, country_data,
                                                                 retention_data,
                                                                 sub_data[pconstants.MERGER_COL_FULL_PAYMENT])
            data_list.append(sub_data)
        return pd.concat(data_list)

    def _get_price_by_country(self, country, install_value):
        if country in self._current_kpi_map:
            kpi_info = self._current_kpi_map[country]
            price_values = kpi_info[pconstants.CONFIG_PRICE]
            if type(price_values) is not list:
                price_values = [price_values]

            price = price_values[0]
            if pconstants.CONFIG_PRICE_THRESHOLD in kpi_info:
                threshold = kpi_info[pconstants.CONFIG_PRICE_THRESHOLD]
                index = self._get_value_index(threshold, install_value)
                price = price_values[index]

            return price
        else:
            return 0

    def _calculate_actual_payment(self, country, retention, full_price):
        if country in self._current_kpi_map:
            kpi_info = self._current_kpi_map[country]
            coefficient = self._get_cal_coefficient(kpi_info, retention)
            return full_price * coefficient
        else:
            return 0

    def _get_cal_coefficient(self, kpi_info, retention):
        thresholds = kpi_info[pconstants.CONFIG_THRESHOLD]
        coefficients = kpi_info[pconstants.CONFIG_COEFFICIENT]
        index = self._get_value_index(thresholds, retention)
        conf_coef = coefficients[index]

        if self._current_check_type == pconstants.CHECK_TYPE_EQUAL:
            if pconstants.EQUAL_RATIO_FLAG == conf_coef:
                if 0 == index:
                    return 1
                return comhelper.division_operation(retention, thresholds[0])
            else:
                return conf_coef
        else:
            return conf_coef

    def _read_all_conf_file(self, super_conf_info):

        conf_map = {}
        for (productKey, conf_name) in super_conf_info.items():
            conf_file = opath.join(self._conf_root_path, conf_name)
            config_info = fhelper.read_json_file(conf_file)
            conf_map[productKey] = config_info

        return conf_map


    @staticmethod
    def _get_sub_data(all_data, start_date, end_date):
        date_mark = comhelper.mark_date_series(all_data[pconstants.APPSFLYER_COL_DATE], start_date, end_date)
        return all_data[date_mark].copy()

    @staticmethod
    def _build_kpi_map(kpi_list):
        kpi_map = {}
        for kpi in kpi_list:
            country = kpi[pconstants.CONFIG_COUNTRY]
            kpi_map[country] = kpi
        return kpi_map

    @staticmethod
    def _get_value_index(thresholds, retention):
        for index in range(len(thresholds)):
            if retention >= thresholds[index]:
                return index
        else:
            return len(thresholds)
