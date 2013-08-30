#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    # print os.path.join(os.path.realpath(dirname), '..')
    sys.path.append( os.path.abspath(os.path.join(__file__, os.pardir)) + '/mycityhall_scrapers/')
    sys.path.insert(0,'./mycityhall_scrapers')

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
