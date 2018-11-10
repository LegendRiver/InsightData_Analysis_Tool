
import append_sys_path
from insight_analysis.manager.insight_reader import InsightReader
from insight_analysis.manager.env_manager import EnvManager
from insight_analysis.util import file_helper as fhelper
from insight_analysis.util import common_helper as chelper
from insight_analysis.handler.handler_factory import HandlerFactory
from insight_analysis.constants import config_constants as conconstants
from insight_analysis.constants import insight_field_constants as inconstants
import os.path as ospath
from insight_analysis.handler.export_excel_handler import ExcelExporter
from insight_analysis.common.eli_logger import EliLogger


def export_data_weekly():
    path_manager = EnvManager()
    conf_dir = path_manager.get_conf_dir()
    weekly_conf = ospath.join(conf_dir, 'insight_weekly_conf.json')
    conf_info = fhelper.read_json_file(weekly_conf)
    account_map = conf_info[conconstants.WEEKLY_ACCOUNT_ID]
    node_types = conf_info[conconstants.WEEKLY_NODE_TYPE]
    output_path = conf_info[conconstants.WEEKLY_OUTPUT_PATH]
    insight_path = conf_info[conconstants.WEEKLY_INSIGHT_PATH]
    if not output_path:
        output_path = path_manager.get_output_dir()
    read_start_date = conf_info[conconstants.WEEKLY_READ_START_DATE]

    current_day = chelper.get_now_date()
    output_path = ospath.join(output_path, current_day)
    fhelper.make_dir(output_path)

    if not read_start_date:
        read_start_date = chelper.get_delta_date(-9)
    filter_start_date = chelper.get_delta_date(-8)
    filter_end_date = chelper.get_delta_date(-2)

    handler_factory = HandlerFactory(conf_dir)

    try:
        for (act_id, act_desc) in account_map.items():
            reader = InsightReader(act_id, handler_factory, read_start_date, node_types=node_types,
                                   insight_path=insight_path)
            data_list = []
            sheet_name_list = []
            file_name = act_desc + '_' + act_id + '_' + filter_start_date + '_' + filter_end_date + '.xlsx'
            output_file = ospath.join(output_path, file_name)
            EliLogger.instance().info('Export account: ' + act_desc + '; outputPath: ' + output_file)
            print 'Export account: ' + act_desc + '; outputPath: ' + output_file

            for ntype in node_types:
                daily_data = reader.read_daily_data(ntype, filter_start_date, filter_end_date)
                hourly_data = reader.read_hourly_data(ntype, filter_start_date, filter_end_date)
                if daily_data is not None and not daily_data.empty:
                    data_list.append(daily_data)
                    daily_name = inconstants.SHEET_NAME_PREFIX_DAILY + '_' + ntype
                    sheet_name_list.append(daily_name)
                if hourly_data is not None and not hourly_data.empty:
                    data_list.append(hourly_data)
                    hourly_name = inconstants.SHEET_NAME_PREFIX_HOURLY + '_' + ntype
                    sheet_name_list.append(hourly_name)
                EliLogger.instance().info('Succeed to export node type: ' + ntype)
                print 'Succeed to export node type: ' + ntype

            if len(data_list) > 0:
                ExcelExporter.export_multi_data_excel(output_file, data_list, sheet_name_list)
    except Exception, e:
        EliLogger.instance().error('Failed to export insight analysis. ' + e.message)
        print 'Failed to export insight analysis. ' + e.message


if __name__ == '__main__':

    export_data_weekly()
