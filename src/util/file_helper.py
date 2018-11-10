
import os
import os.path
import json
import openpyxl


def get_subdir_list(root_path):
    dir_list = []
    for parent, dirs, files in os.walk(root_path):
        for dir_name in dirs:
            full_path = os.path.join(parent, dir_name)
            dir_list.append(full_path)
    return dir_list


def get_subdir_name_list(root_path):
    dir_list = []
    for parent, dirs, files in os.walk(root_path):
        for dir_name in dirs:
            dir_list.append(dir_name)
    return dir_list


def get_file_list(root_path):
    file_list = []
    for parent, dirs, files in os.walk(root_path):
        for file_name in files:
            if file_name.startswith('.'):
                continue
            full_path = os.path.join(parent, file_name)
            file_list.append(full_path)
    return file_list


def read_json_file(file_path):
    with open(file_path) as json_file:
        json_data = json.load(json_file)
        return json_data


def make_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_excel_sheet_names(excel_file):

    try:
        wb = openpyxl.load_workbook(excel_file, True)
        sheets = wb.get_sheet_names()

        return sheets

    except Exception:
        print "read excel exception."


