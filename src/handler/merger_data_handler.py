
from insight_analysis.handler.handler_factory import HandlerFactory
from insight_analysis.util import common_helper as chelper

import pandas as pd


class MergerDataHandler:

    def __init__(self, config_path):
        self.hfactory = HandlerFactory(config_path)

    def merger_in_re_per_day(self, insight_files, retention_files, node_type):

        insight_handler = self.hfactory.get_insight_handler(node_type)
        insight_datas = [insight_handler.read_insight_data(file_path) for file_path in insight_files]
        all_insight_data = pd.concat(insight_datas)
        insight_data_per_day = insight_handler.get_insight_data_per_day(all_insight_data)

        retention_handler = self.hfactory.get_retention_handler(node_type)
        retention_dates = [chelper.get_retention_date(file_path) for file_path in retention_files]
        retention_datas = [retention_handler.get_retention_per_day(file_path) for file_path in retention_files]
        retention_data_per_day = pd.concat(retention_datas, keys=retention_dates)

        all_merger_data = []
        retention_columns = retention_data_per_day.columns
        for date_key in retention_dates:
            one_retention = retention_data_per_day.ix[date_key]
            if date_key not in insight_data_per_day.index:
                one_day_data = one_retention
            else:
                one_insight = insight_data_per_day.loc[date_key]
                one_insight = one_insight[retention_columns]
                one_day_data = one_retention.append(one_insight)
                one_day_data.sort_index(inplace=True)
            all_merger_data.append(one_day_data)

        return pd.concat(all_merger_data, keys=retention_dates)



