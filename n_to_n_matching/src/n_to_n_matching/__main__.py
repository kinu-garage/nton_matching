import argparse
import sys

from gj.role import Roles_ID
from n_to_n_matching.test_main import test_2, test_3

DESC_TOOL = """'gjls_match' command HELP TBD."""

def stdin():
    _MSG_LIMITATION_VOLUME = ("")
    _PATH_XLSX_TEST1 = 'n_to_n_matching/test/20240602-updated_gjls_student-master.xlsx'
    _PATH_XLSX_TEST_20250322 =  "n_to_n_matching/test/2024年度_家庭名簿_当番マスタ24年度正式版_20250322_委員25年度更新.xlsx"
    _PATH_XLSX_TEST_20250503 =  "n_to_n_matching/test/20250503_gjls-family-master_mod-by-130s.xlsx"
    _SHEET_NAME = "2025当番マスター"
    _PATH_OUTIDR = '~/Desktop'
    _PATH_OUTIDR_IN_CONTAINER = "/cws/src/130s/nton_matching"

    _test_path_xlsx = _PATH_XLSX_TEST_20250503
    parser = argparse.ArgumentParser(description=DESC_TOOL)
    parser.add_argument("-t", '--type_role', type=Roles_ID, choices=list(Roles_ID), nargs="+",
                        default=[Roles_ID.TOSHO])
    parser.add_argument("-i", "--input_master_file", help="Path (relative or absolute) of the file of the list of famillies. File format: .xlsx is the only supported format for v0.2.",
                        default=_test_path_xlsx, action="store_true")
    parser.add_argument("-d", "--debug", help="Disabled by default.", action="store_true")
    parser.add_argument("-o", "--path_output", help="Path (relative or absolute) to the directory where output files will be generated", 
                        #default=_PATH_OUTIDR,
                        default=_PATH_OUTIDR_IN_CONTAINER,
                        action="store_true")
    parser.add_argument("-s", "--master_sheet", help="Name of the sheet in the input file", 
                        default=_SHEET_NAME, action="store_true")
    args = parser.parse_args()
    return args
    
def main():
    # Check Python environment
    print("Python sys.path: {}".format(sys.path))
    _args = stdin()
    roles = _args.type_role
    for role_obj in roles:
        role = role_obj.value
        print(f"011 {role_obj=}, {role=}")
        if (role == Roles_ID.ANZEN.value) or (role == Roles_ID.HOKEN.value) or (role == Roles_ID.TOSHO.value):
            test_3(_args.input_master_file, sheet_name=_args.master_sheet, output_path=_args.path_output, role=role)
        else:
            raise RuntimeError("No eligible role passed.")
    #test_2()

if __name__ == "__main__":
    main()
