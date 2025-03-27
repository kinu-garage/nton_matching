import argparse
import sys

from gj.role import Roles_ID
from n_to_n_matching.test_main import test_2, test_3

DESC_TOOL = """'gjls_match' command HELP TBD."""

def stdin():
    _MSG_LIMITATION_VOLUME = ("")
    _PATH_XLSX_TEST1 = 'n_to_n_matching/test/20240602-updated_gjls_student-master.xlsx'
    _PATH_OUTIDR = '~/Desktop'
    _PATH_OUTIDR_IN_CONTAINER = "/cws/src/130s/nton_matching"

    parser = argparse.ArgumentParser(description=DESC_TOOL)
    parser.add_argument("-t", '--type_role', type=Roles_ID, choices=list(Roles_ID), nargs="+",
                        default=[Roles_ID.TOSHO])
    parser.add_argument("-i", "--input_master", help="Path (relative or absolute) of the file of the list of famillies. File format: .xlsx is the only supported format for v0.2.",
                        default=_PATH_XLSX_TEST1, action="store_true")
    parser.add_argument("-d", "--debug", help="Disabled by default.", action="store_true")
    parser.add_argument("-o", "--path_output", help="Path (relative or absolute) to the directory where output files will be generated", 
                        #default=_PATH_OUTIDR,
                        default=_PATH_OUTIDR_IN_CONTAINER,
                        action="store_true")
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
            test_3(_args.input_master, output_path=_args.path_output, role=role)
        else:
            raise RuntimeError("No eligible role passed.")
    #test_2()

if __name__ == "__main__":
    main()
