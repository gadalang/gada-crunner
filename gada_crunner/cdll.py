"""Official runner for C dlls.
"""
import os
from ctypes import *
from typing import List, Optional
from gada import component


def run(comp, *, gada_config: dict, node_config: dict, argv: Optional[List] = None):
    # Check the entrypoint is configured
    entrypoint = node_config.get("entrypoint", None)
    if not entrypoint:
        raise Exception("missing entrypoint in configuration")

    # Force module to be in node_path
    comp_path = component.get_dir(comp)
    file_path = os.path.abspath(os.path.join(comp_path, node_config["file"]))
    if not os.path.isfile(file_path):
        raise Exception("file {} not found".format(node_config["file"]))
    elif not file_path.startswith(comp_path):
        raise Exception("can't run file outside of component directory")

    # Check the entrypoint exists
    lib = cdll.LoadLibrary(file_path)
    fun = getattr(comp, entrypoint, None)
    if not fun:
        raise Exception(f"dll {file_path} has no entrypoint {entrypoint}")

    # Call entrypoint
    fun()
