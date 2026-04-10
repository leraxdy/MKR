
import os
from typing import List, Optional


def read_file(file_path: str) -> List[str]:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except IOError as e:
        raise IOError(f"Cannot read file {file_path}: {e}")


def filter_lines(lines: List[str], keyword: str) -> List[str]:
    """Filter lines that contain a specific keyword."""
    if not keyword:
        return []

    return [line for line in lines if keyword in line]