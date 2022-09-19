# sqlmap/tamper/normal.py
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    if payload:
        result = payload.replace("OR", "oorr").replace("AND", "%26%26").replace("\'","%27").replace(" ","%A0").replace("--%A0-",'%26%26%A0%28%271%27%29%3D%28%271').replace("(","%28").replace(")","%29").replace(",","%2C").replace("=","%3D")
        return result