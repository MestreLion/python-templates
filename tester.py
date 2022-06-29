#!/usr/bin/env python3
#
# This file is part of <project>, see <https://github.com/MestreLion/project>
# Copyright (C) 2022 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>

"""
NBT Libraries test
"""

import logging
import pathlib
import sys

# =============================================================================
# Add new functions here, moving old ones down


# =============================================================================


def main():
    loglevel = logging.INFO
    funcs = tuple(k for k, v in globals().items()
                  if callable(v) and k not in ('main',))

    # Lame argparse
    if len(sys.argv) <= 1 or '--help' in sys.argv[1:] or '-h' in sys.argv[1:]:
        print("Usage: {} FUNCTION [ARGS...]\nAvailable functions:\n\t{}".format(
            __file__, "\n\t".join(funcs)))
        return
    if '-v' in sys.argv[1:]:
        loglevel = logging.DEBUG
        sys.argv.remove('-v')
    logging.basicConfig(level=loglevel, format='%(levelname)-5.5s: %(message)s')

    func = sys.argv[1]
    args = sys.argv[2:]
    if func not in funcs:
        log.error("Function %r does not exist! Try one of:\n\t%s",
                  func, "\n\t".join(funcs))
        return

    def try_int(value):
        try:
            return int(value)
        except ValueError:
            return value
    args = [try_int(_) for _ in args]

    res = globals()[func](*args)
    if res is not None:
        print(repr(res))


log = logging.getLogger(__name__)
if __name__ == '__main__':
    log = logging.getLogger(pathlib.Path(__file__).stem)
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log.error("Aborted")
