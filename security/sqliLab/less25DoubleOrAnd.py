# sqlmap/tamper/escapequotes.py
from lib.core.enums import PRIORITY


__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    if payload:
        result = payload.replace("OR", "oorr").replace("AND", "aandnd")
        return result
