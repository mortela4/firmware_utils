""" @file generate_file_checksums.py """

import sys
import subprocess
import argparse
# For (optional) GUI
from gooey import Gooey


use_gui = True


def check_ip(iface_name):
    """
    Returns IP-address of given interface.
    """
    ip_addr = None
    p1 = subprocess.Popen(['ipconfig'], stdout=subprocess.PIPE)

    # Run the command
    output = p1.communicate(timeout=30)[0]

    lines = output.splitlines()
    for line in lines:
        try:
            line_str = str(line, encoding='utf-8')
            if line_str.strip().startswith("IPv4 Address"):
                lead_txt, ip_addr = line_str.split(':')
        except str.FormatError as e:
            print("String formatting ERROR! Exc = %s" % e)
    #
    return ip_addr


def parse_args_and_execute():
    """ Parse args and run bg-process(es) """
    global use_gui
    #
    parser = argparse.ArgumentParser(description="'GetLocalIpAddress' utility.")
    parser.add_argument('--iface', '-i', action="store", dest="if_name", type=str, help='Name of interface')

    cli_args = parser.parse_args(sys.argv[1:])
    #
    if_name = cli_args.if_name
    if not if_name:
        print("Specify a valid interface!")
    else:
        try:
            ret_val = check_ip(if_name)
            #
            if ret_val:
                print("IP-address: \r\n%s" % ret_val)
            else:
                print("FAIL: no result!!")
        except Exception as e:
            print("FAIL: process failure!! Exception: %s" % e)


@Gooey
def gui_wrapper():
    parse_args_and_execute()


# ***************** MAIN ************************
if __name__ == "__main__":
    if use_gui:
        gui_wrapper()
    else:
        parse_args_and_execute()
