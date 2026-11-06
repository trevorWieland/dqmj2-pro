import contextlib
import sys
from pathlib import Path
from project import ROOT, sha256


ORIGINAL = sha256
ACTIVE = None


class SnapshotHashes:
    def __init__(self, original=ORIGINAL):
        self.original = original
        self.values = {}
        self.aliases = {}
        self.calls = 0
        self.hits = 0

    @staticmethod
    def stamp(path):
        info = path.stat()
        return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns

    def __call__(self, name):
        self.calls += 1
        alias = Path(name).absolute()
        path = alias.resolve()
        if alias in self.aliases and self.aliases[alias] != path:
            raise ValueError('Hash input alias changed during a closed read snapshot')
        self.aliases[alias] = path
        stamp = self.stamp(path)
        if path in self.values:
            old_stamp, digest = self.values[path]
            if old_stamp != stamp:
                actual = self.original(path)
                if actual != digest:
                    raise ValueError('Hash input content changed during a closed read snapshot')
                self.values[path] = stamp, digest
            self.hits += 1
            return digest
        digest = self.original(path)
        if self.stamp(path) != stamp:
            raise ValueError('Hash input changed while initially reading a closed snapshot')
        self.values[path] = stamp, digest
        return digest

    def verify(self):
        for alias, path in self.aliases.items():
            if alias.resolve() != path:
                raise ValueError('Hash input alias changed before snapshot closure')
        for path, (stamp, digest) in self.values.items():
            if self.original(path) != digest:
                raise ValueError('Hash input content changed before snapshot closure')
        return dict(calls=self.calls, hits=self.hits, uniqueFiles=len(self.values),
            everyDistinctFileFullyHashedAgainAtClosure=True)


def replace(before, after):
    for module in list(sys.modules.values()):
        if module is None or getattr(module, 'sha256', None) is not before:
            continue
        name = getattr(module, '__file__', None)
        if name and Path(name).resolve().is_relative_to(ROOT):
            module.sha256 = after


@contextlib.contextmanager
def scope(receipts):
    global ACTIVE
    if ACTIVE is not None:
        yield ACTIVE
        return
    cache = SnapshotHashes()
    ACTIVE = cache
    replace(ORIGINAL, cache)
    try:
        yield cache
        receipts.append(cache.verify())
    finally:
        replace(cache, ORIGINAL)
        ACTIVE = None
