# helpers/utils.py — stub utilities used by private_sudos.py
import os, platform

def get_size(bytes_val, suffix="B"):
    """Convert bytes to human readable."""
    for unit in ["", "K", "M", "G", "T"]:
        if abs(bytes_val) < 1024.0:
            return f"{bytes_val:.1f} {unit}{suffix}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} Y{suffix}"

def humanbytes(size):
    return get_size(size)
