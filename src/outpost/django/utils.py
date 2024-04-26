import locale
from base64 import urlsafe_b64encode
from pathlib import PurePosixPath
from uuid import uuid4

from IPy import IP


class IPList(list):
    def __init__(self, addresses):
        super(IPList, self).__init__()
        for address in addresses:
            self.append(IP(address))

    def __contains__(self, address):
        for net in self:
            if address in net:
                return True
        return False


class LocaleManager:
    def __init__(self, localename):
        self.name = localename

    def __enter__(self):
        self.orig = locale.setlocale(locale.LC_CTYPE)
        locale.setlocale(locale.LC_ALL, self.name)

    def __exit__(self, exc_type, exc_value, traceback):
        locale.setlocale(locale.LC_ALL, self.orig)


class Uuid4Upload(str):
    def __new__(cls, instance, filename):
        f = PurePosixPath(filename)
        u = urlsafe_b64encode(uuid4().bytes).decode("ascii").rstrip("=")
        p = PurePosixPath(instance.__module__, instance._meta.object_name)
        return str.__new__(cls, p.joinpath(u).with_suffix(f.suffix))
