""" 
@file generate_file_checksums.py 
================================
@brief Generate MD5-cheksum on file.
Both with a GUI and as a CLI utility.
"""

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
    return md5.hexdigest()


def parse_args_and_execute():
    """ Parse args and run bg-process(es) """
    global use_gui
    #
    if use_gui:
        parser = GooeyParser()
        parser.add_argument('fw_file',
                            action='store',
                            widget='FileChooser',
                            help="File to calculate MD5-checksum on")
    else:
        parser = argparse.ArgumentParser(description="'GenerateFileChksum' command-line utility.")
        parser.add_argument('--file', '-f', action="store", dest="fw_file", type=str, help='File name')

    cli_args = parser.parse_args(sys.argv[1:])
    #
    fw_file = cli_args.fw_file
    #
    if fw_file is None:
        print("Specify a valid filename!")
    else:
        try:
            ret_val = calculate_md5(fw_file)
            #
            if ret_val:
                print("MD5-checksum:\r\n%s" % ret_val)
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
