""" @file generate_file_checksums.py """

import sys
import hashlib
import argparse
# For (optional) GUI
from gooey import Gooey, GooeyParser


use_gui = True


def calculate_md5(filename, block_size=2**20):
    """
    Returns MD% checksum for given file.
    """
    md5 = hashlib.md5()
    try:
        file = open(filename, 'rb')
        while True:
            data = file.read(block_size)
            if not data:
                break
            md5.update(data)
    except IOError:
        print('File \'' + filename + '\' not found!')
        return None
    except:
        return None
    #
    return md5.hexdigest()


def parse_args_and_execute():
    """ Parse args and run bg-process(es) """
    global use_gui
    #
    if use_gui:
        parser = GooeyParser()
        parser.add_argument('fw_file1',
                            action='store',
                            widget='FileChooser',
                            help="File no.1 to calculate MD5-checksum on")
        parser.add_argument('fw_file2',
                            action='store',
                            widget='FileChooser',
                            help="File no.2 to calculate MD5-checksum on")
    else:
        parser = argparse.ArgumentParser(description="'GenerateFileChksum' command-line utility.")
        parser.add_argument('--file1', '-f1', action="store", dest="fw_file1", type=str, help='File no.1 name')
        parser.add_argument('--file2', '-f2', action="store", dest="fw_file1", type=str, help='File no.2 name')

    cli_args = parser.parse_args(sys.argv[1:])
    #
    fw_file1 = cli_args.fw_file1
    fw_file2 = cli_args.fw_file2
    #
    if fw_file1 is None or fw_file2 is None:
        print("Specify a valid filename!")
    else:
        try:
            ret_val1 = calculate_md5(fw_file1)
            ret_val2 = calculate_md5(fw_file2)
            #
            if ret_val1 is not None and ret_val2 is not None:
                print("MD5-checksum file1: %s\r\n%s" % (fw_file1, ret_val1))
                print("\r\n-----------------------------------------\r\n")
                print("MD5-checksum file2: %s\r\n%s" % (fw_file2, ret_val2))
                print("\r\n===================================\r\n")
                #tst1 = str(ret_val1).encode('ascii').strip()
                #tst2 = str(ret_val2).encode('ascii').strip()
                #if tst1 == tst2:
                if ret_val1 == ret_val2:
                    print("OK: file1 and file2 are EQUAL.\r\n")
                else:
                    print("WARN: file1 and file2 are NOT equal!")
            else:
                print("FAIL: checksum computation error!!")
        except Exception as e:
            print("FAIL: checksum computation failure!! Exception: %s" % e)


@Gooey
def gui_wrapper():
    parse_args_and_execute()


# ***************** MAIN ************************
if __name__ == "__main__":
    if use_gui:
        gui_wrapper()
    else:
        parse_args_and_execute()
