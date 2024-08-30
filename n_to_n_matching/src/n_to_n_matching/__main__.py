from n_to_n_matching.test_main import test_2, test_3_tosho

import sys

def main():
    # Check Python environment
    print("Python sys.path: {}".format(sys.path))
    path_touban_master_sheet = 'n_to_n_matching/test/20240602-updated_gjls_student-master.xlsx'
    #test_3_tosho(path_touban_master_sheet)

    test_2()

if __name__ == "__main__":
    main()
