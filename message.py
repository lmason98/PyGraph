"""
File: message.py
Author: Luke Mason

Description: Console output functions
"""
from settings import DEBUG, LOG


def log(*args):
    """
    General logging function, should replace print in debugging scenarios
    """
    if DEBUG: print(' [PG]:', ' '.join(map(str, args)))


def success(*args):
    """
    Success indication function, should indicate success at critical points in the app
    """
    if LOG: print('  [+]:', ' '.join(map(str, args)))


def error(*args):
    """
    Error indication function, should indicate error at critical points in the app
    """
    if LOG: print('  [x]:', ' '.join(map(str, args)))
