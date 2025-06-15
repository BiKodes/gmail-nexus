"""Utility functions for file handling and date parsing."""
import os
from typing import Union
from datetime import datetime

try:
    from dateutil import parser as date_parser
except ImportError:
    date_parser = None


def get_absolute_path(file_name: str, within_package: bool = True) -> str:
    """
    Construct the absolute path to afile.
    """
    base_dir = os.path.dirname(__file__) if within_package else os.path.join(os.path.dirname(__file__), os.pardir)
    return os.path.abspath(os.path.join(base_dir, file_name))

def read_file_contents(file_name: str, within_package: bool = True) -> str:
    """
    Read and return the content of a file.
    """
    file_path = get_absolute_path(file_name, within_package=within_package)

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    
def parde_string_to_date(date_string: Union[str, None]) -> Union[datetime, None]:
    """
    Parse a string into a datetime object.
    """
    if not date_parser:
        raise RuntimeError("`dateutil` package is required for date parsing. Install it using `pip install python-dateutil`.")
    
    if not date_string:
        return None
    
    try:
        return date_parser.parse(date_string)
    except (ValueError, TypeError):
        return None
