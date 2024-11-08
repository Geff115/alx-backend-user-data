#!/usr/bin/env python3
"""
This script implements a function called
filter_datum that returns a log message
"""

import re
import logging
import os
import mysql.connector
# from logging import logger
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        # Call the parent format method to handle the rest of the formatting
        return super().format(record)


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


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    This function initializes a logger user_data and
    return a logger object
    """
    logger = logging.getLogger("user_data")
    # Setting the logger level to INFO
    logger.setLevel(logging.INFO)
    # Disabling propagation
    logger.propagate = False

    # Instantiating a StreamHandler
    console_handler = logging.StreamHandler()
    # Passing the PII_FIELDS to RedactingFormatter
    formatter = RedactingFormatter(PII_FIELDS)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    This function connects to a secure holberton
    database to read a users table.
    """
    # Retrieving the database credentials
    DB_USERNAME = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    DB_PASSWORD = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    DB_HOST = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    DB_NAME = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connecting to the database
    mydb = mysql.connector.connect(
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME
    )

    return mydb
