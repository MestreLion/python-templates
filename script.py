#!/usr/bin/env python3
#
#    Copyright (C) [YEAR] Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. See <http://www.gnu.org/licenses/gpl.html>

# This file is part of [PROJNAME], see <https://github.com/MestreLion/[PROJTAG]>
# Copyright (C) [YEAR] Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>

"""
Full Description
"""

import argparse
import logging
import os
import sys


COPYRIGHT="""
Copyright (C) 2018 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>
"""

log = logging.getLogger(os.path.basename(os.path.splitext(__file__)[0]))


class ProjectError(Exception):
    """Base class for custom exceptions, with errno and %-formatting for args.

    All modules in this package raise this (or a subclass) for all
    explicitely raised, business-logic, expected or handled exceptions
    """
    def __init__(self, msg:str="", *args, errno:int=0):
        super().__init__(str(msg) % args)
        self.errno = errno


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=COPYRIGHT,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet',
                       dest='loglevel',
                       const=logging.WARNING,
                       default=logging.INFO,
                       action="store_const",
                       help="Suppress informative messages.")

    group.add_argument('-v', '--verbose',
                       dest='loglevel',
                       const=logging.DEBUG,
                       action="store_const",
                       help="Verbose mode, output extra info.")

    parser.add_argument('-a', '--arg',
                        default="somearg",
                        help="Some Arg."
                            " [Default: %(default)s]")

    parser.add_argument('-o', '--option',
                        dest='option',
                        default=False,
                        action="store_true",
                        help="Some Option.")

    parser.add_argument(nargs='*',
                        dest='files',
                        help="Some files.")

    args = parser.parse_args(argv)
    args.debug = args.loglevel == logging.DEBUG

    return args


def main(argv=None):
    args = parse_args(argv)
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-5.5s: %(message)s')
    log.debug(args)

    # Program go here...




if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        # https://docs.python.org/3/library/signal.html#note-on-sigpipe
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
    except Exception as e:
        log.critical(e, exc_info=True)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(2)  # signal.SIGINT.value
