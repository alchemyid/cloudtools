import decimal
import datetime
import subprocess
import os
import re

class helpers:
    @staticmethod
    def jsonSerializer(obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        elif isinstance(obj, decimal.Decimal):
            return str(obj)

        raise TypeError(
            'Cannot serialize {!r} (type {})'.format(obj, type(obj)))

    @staticmethod
    def command(s):
        proc = subprocess.Popen([s], stdout=subprocess.PIPE, shell=True)
        out, _ = proc.communicate()
        # print(re.sub(r"[\n\t\s]*", "",out.decode()))
        return re.sub(r"[\n\t\s]*", "",out.decode())
        # return out.decode()
    
    @staticmethod
    def env(s):
        r =  os.environ[s]
        return r
