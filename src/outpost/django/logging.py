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


class ExceptionFilter(logging.Filter):
    """
    Python logging filter that ignores certain Exceptions.
    """

    def __init__(self, exceptions):
        self.exceptions = exceptions

    def filter(self, record):
        if not record.exc_info:
            return True
        t, *_ = record.exc_info
        return t not in self.exceptions
