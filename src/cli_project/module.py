# This file is part of [PROJECT NAME], see <https://github.com/MestreLion/[PROJECT]>
# Copyright (C) [YEAR] Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>
"""
Module Description
"""
from __future__ import annotations

import logging
import typing_extensions as t

from . import util as u

log: logging.Logger = logging.getLogger(__name__)


def function(fd: t.BinaryIO) -> None:
    """Docstring"""
    u.printf("Path: %s", fd.name)
    ...
