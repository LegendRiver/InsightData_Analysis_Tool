
import pandas as pd
from insight_analysis.manager.env_manager import EnvManager
import os.path as ospath


def read_campaign_retention():
    path_manager = EnvManager()
    resource_path = path_manager.get_resource_dir()
    source_dir = ospath.join(resource_path, 'campaign_retention')
    source_file = ospath.join(source_dir, 'campaign_retention.csv')
    source_data = pd.read_csv(source_file, usecols=['Date', 'Campaign', 'Install Day', 'Day 1'])

    sa_mask = source_data['Campaign'].apply(isContain, sub_string='_SA_')
    sa_data = source_data[sa_mask]
    sa_sum = sa_data.groupby('Date').sum()
    row_num = len(sa_sum.index)
    if row_num > 0:
        country_list = pd.Series(['SA']*row_num, index=sa_sum.index)
        sa_sum['country'] = country_list

    ph_mask = source_data['Campaign'].apply(isContain, sub_string='_ph_')
    ph_data = source_data[ph_mask]
    ph_sum = ph_data.groupby('Date').sum()
    row_num = len(ph_sum.index)
    if row_num > 0:
        country_list = pd.Series(['PH']*row_num, index=ph_sum.index)
        ph_sum['country'] = country_list

    result_data = pd.concat([sa_sum, ph_sum])

    writer = pd.ExcelWriter('sum_retention.xlsx')
    result_data.to_excel(writer, 'retention')
    writer.save()

def isContain(source_string, sub_string):
    return sub_string in source_string


if __name__ == '__main__':
    read_campaign_retention()
