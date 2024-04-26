from pathlib import Path

from compressor.filters import CompilerFilter
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django_libsass import (
    OUTPUT_STYLE,
    SOURCE_COMMENTS,
    SassCompiler,
    compile,
)


class DjangoLessFilter(CompilerFilter):
    def __init__(self, content, **kwargs):
        DIRS = finders.find(".", all=True)
        c = "lessc --include-path={path} {{infile}} {{outfile}}".format(
            path=":".join(DIRS)
        )
        super(DjangoLessFilter, self).__init__(content, command=c, **kwargs)


class DjangoSassCompiler(SassCompiler):
    @staticmethod
    def importer(path, prev=None):

        n = Path(path)
        for name in (
            n.with_suffix(".scss"),
            n.with_name(f"_{n.name}").with_suffix(".scss"),
        ):
            search = str(name)
            if prev is not None:
                p = Path(prev)
                if not p.is_absolute():
                    search = str(p.parent / name)
            if not staticfiles_storage.exists(search):
                continue
            with staticfiles_storage.open(search) as content:
                return [(search, content.read())]

    def input(self, **kwargs):
        if self.filename:
            return compile(
                filename=self.filename,
                output_style=OUTPUT_STYLE,
                source_comments=SOURCE_COMMENTS,
                importers=[(0, DjangoSassCompiler.importer)],
            )
        else:
            return compile(
                string=self.content,
                output_style=OUTPUT_STYLE,
                importers=[(0, DjangoSassCompiler.importer)],
            )
