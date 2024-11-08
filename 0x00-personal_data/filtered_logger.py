#!/usr/bin/env python3
"""
This script implements a function called
filter_datum that returns a log message
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    This function uses a regex to replace occurences of
    certain field values.
    """
    # Generate the regex pattern dynamically
    pattern = r'\b(' + '|'.join(fields) + r')\b' + \
              re.escape(separator) + r'(.*?)'
    return re.sub(pattern, r'\1' + separator + redaction, message)
