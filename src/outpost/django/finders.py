import os
from django.contrib.staticfiles import utils
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import BaseFinder
from django.core.checks import Error


class OutpostFinder(BaseFinder):
    def check(self, **kwargs):
        errors = []
        if not isinstance(settings.OUTPOST_STATIC_PATHS, (list, tuple)):
            errors.append(
                Error(
                    "The OUTPOST_STATIC_PATHS setting is not a list.",
                    hint="Perhaps you forgot to include it in your settings?",
                    id="outpost.django.E001",
                )
            )
        for entry in settings.OUTPOST_STATIC_PATHS:
            if not isinstance(entry, tuple):
                errors.append(
                    Error(
                        f"Not a valid mapping for OUTPOST_STATIC_PATHS: {entry}",
                        hint="Mapping should be defined as tuple.",
                        id="outpost.django.E002",
                    )
                )
            if len(entry) != 2:
                errors.append(
                    Error(
                        f"Not a valid mapping for OUTPOST_STATIC_PATHS: {entry}",
                        hint="Mapping needs a virtual and a local path.",
                        id="outpost.django.E003",
                    )
                )
            virtual, local = entry
            if len(virtual) == 0:
                errors.append(
                    Error(
                        f"Not a valid mapping for OUTPOST_STATIC_PATHS: {entry}",
                        hint="Virtual path must not be empty.",
                        id="outpost.django.E004",
                    )
                )
            if not virtual.endswith("/"):
                errors.append(
                    Error(
                        f"Not a valid mapping for OUTPOST_STATIC_PATHS: {entry}",
                        hint="Virtual path must end with slash.",
                        id="outpost.django.E005",
                    )
                )
            if not os.path.exists(local):
                errors.append(
                    Error(
                        f"Not a valid mapping for OUTPOST_STATIC_PATHS: {entry}",
                        hint="Local path does not exist.",
                        id="outpost.django.E006",
                    )
                )
        return errors

    def find(self, path, all=False):
        matches = []
        for virtual, local in settings.OUTPOST_STATIC_PATHS:
            if not path.startswith(virtual):
                continue
            path = os.path.join(local, path[len(virtual):])
            if not os.path.exists(path):
                continue
            if not all:
                return path
            matches.append(path)
        return matches

    def list(self, ignore_patterns):
        for virtual, local in settings.OUTPOST_STATIC_PATHS:
            storage = FileSystemStorage(location=local)
            for path in utils.get_files(storage, ignore_patterns):
                yield path, storage
