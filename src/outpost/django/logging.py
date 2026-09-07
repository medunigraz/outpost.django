import logging


class StaticFieldFilter(logging.Filter):
    """
    Python logging filter that adds the given static contextual information
    in the ``fields`` dictionary to all logging records.
    """

    def __init__(self, fields):
        self.static_fields = fields

    def filter(self, record):
        for k, v in self.static_fields.items():
            setattr(record, k, v)
        return True


class NameFilter(logging.Filter):
    """
    Python logging filter that ignores certain record names.
    """

    def __init__(self, names):
        self.names = names

    def filter(self, record):
        name = getattr(record, "name", None)
        if not name:
            return True
        return name not in self.names
