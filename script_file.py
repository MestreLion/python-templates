#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
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


"""
    Full Description
"""

import sys
import os
import argparse
import logging
import contextlib


log = logging.getLogger(os.path.basename(os.path.splitext(__file__)[0]))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__)

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

    parser.add_argument(nargs="?",
                        dest='file',
                        metavar="FILE",
                        help="File to export to or import from."
                            " [Default: stdout / stdin]")

    args = parser.parse_args(argv)
    args.debug = args.loglevel == logging.DEBUG

    return args


@contextlib.contextmanager
def openstd(filename=None, mode="r"):
    if filename and filename != '-':
        fh = open(filename, mode)
        name = "'%s'" % filename
    else:
        if mode.startswith("r"):
            fh = sys.stdin
            name = "<stdin>"
        else:
            fh = sys.stdout
            name = "<stdout>"
    try:
        yield fh, name
    finally:
        if fh is not sys.stdout:
            fh.close()


def main(argv=None):
    args = parse_args(argv or [])
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)s: %(message)s')
    log.debug(args)

    with openstd(args.file, 'r') as (fd, name):
        log.debug("Reading from %s", name)
        for line in fd:
            log.info(line.strip())

#     with openstd(args.file, 'w') as (fd, name):
#         log.debug("Writing to %s", name)
#         fd.write("" + "\n")




if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:
        log.critical(e, exc_info=True)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
