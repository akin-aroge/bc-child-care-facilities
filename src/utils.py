""" utilities """

import pathlib


def get_proj_root() -> pathlib.Path:
    return pathlib.Path(__file__).parent.parent