
from insight_analysis.profit_handler.appsflyer_data_handler import AFDataHandler
from insight_analysis.constants import profit_constants as pconstants
import pandas as pd


class FakeDataHandler(AFDataHandler):
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
            price_data = map(self._get_price_by_country, country_data, install_data)
            sub_data[pconstants.MERGER_COL_FULL_PAYMENT] = install_data * price_data

            sub_data[pconstants.MERGER_COL_ACTUAL_PAYMENT] = sub_data[pconstants.MERGER_COL_FULL_PAYMENT]
            data_list.append(sub_data)
        return pd.concat(data_list)
