# This file is part of PROJECT, see <https://github.com/MestreLion/PROJECT>
# Copyright (C) 2023 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>
"""
Project Short Description

Unlike other modules, main's description is the project short description
It can, and maybe should, contain additional paragraphs such as this one.

Whatever goes here is a nice candidate as the README's abstract, and vice-versa.
"""
from __future__ import annotations

import logging
import sys

from . import util as u

__version__ = "2023.9.1"  # no leading zeros! https://semver.org/#spec-item-2

log: logging.Logger = logging.getLogger(__package__)


def cli(argv: list[str] | None = None) -> None:
    """Command-line argument handling and logging setup"""
    parser = u.ArgumentParser(description=__doc__, version=__version__)
    parser.add_argument(
        nargs="?",
        default="-",
        dest="infile",
        metavar="INPUT_FILE",
        help="Input file to import from. [Default: stdin]",
    )
    parser.add_argument(
        "-o",
        "--option",
        dest="option",
        default=False,
        action="store_true",
        help="Some boolean option, False by default, set to True when added.",
    )
    parser.add_argument(
        "-a",
        "--argument",
        default="somearg",
        metavar="ARG",
        help="A string argument with a default value. [Default: %(default)s]",
    )

    args = parser.parse_args(argv)
    u.setup_logging(level=args.loglevel, fmt="%(levelname)-8s: %(message)s")
    log.debug(args)

    log.info("Hello World!")


def run(argv: list[str] | None = None) -> None:
    """CLI entry point, handling exceptions from cli() and setting exit code"""
    try:
        cli(argv)
    except u.ProjectError as err:
        log.critical(err)
        sys.exit(1)
    except Exception as err:
        log.exception(err)
        sys.exit(1)
    except KeyboardInterrupt:
        log.info("Aborting")
        sys.exit(2)  # signal.SIGINT.value, but not actually killed by SIGINT
