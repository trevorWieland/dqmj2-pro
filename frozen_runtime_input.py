import builtins
import hashlib
import os
from pathlib import Path
import re
import threading

_ACTIVE = threading.Lock()


def _digest(path, opener):
    with opener(path, 'rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


class FrozenRuntimeInput:
    def __init__(self, root, *, fromPath, expectedSha256, snapshotPath, snapshotSha256):
        if fromPath != 'ledger/functions.jsonl':
            raise ValueError('Only the exact ledger/functions.jsonl input may be mapped')
        for value in (expectedSha256, snapshotSha256):
            if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
                raise ValueError('Expected an exact lowercase SHA256 pin')
        if expectedSha256 != snapshotSha256:
            raise ValueError('Snapshot pin must equal the required frozen input pin')
        self.root = Path(root).resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError('Mapping root must be a directory')
        logical = self.root / fromPath
        self.logical = logical.resolve(strict=True)
        if self.logical != logical or not self.logical.is_file():
            raise ValueError('Logical ledger must be the actual contained regular file')
        candidate = Path(snapshotPath)
        if '..' in candidate.parts:
            raise ValueError('Snapshot path traversal is forbidden')
        candidate = candidate if candidate.is_absolute() else self.root / candidate
        self.snapshot = candidate.resolve(strict=True)
        if not self.snapshot.is_relative_to(self.root) or not self.snapshot.is_file():
            raise ValueError('Snapshot must be a contained regular file')
        if self.snapshot == self.logical or self.snapshot.samefile(self.logical):
            raise ValueError('Frozen input cannot map to itself or a live-file hardlink')
        self.expected = expectedSha256
        self.from_path = fromPath
        self.reads = []
        self.before = None
        self.after = None
        self.entered = False
        self.finished = False
        self.original = None
        self.hooks = None

    def _verify_snapshot(self):
        opener = self.original[3]
        if self.snapshot.resolve(strict=True) != self.snapshot:
            raise ValueError('Snapshot path changed or escaped after validation')
        if self.logical.resolve(strict=True) != self.logical:
            raise ValueError('Live ledger path changed after validation')
        if _digest(self.snapshot, opener) != self.expected:
            raise ValueError('Frozen runtime snapshot content changed')

    def _route(self, file, mode, api, options=None):
        if isinstance(file, int):
            return file
        try:
            lexical = Path(os.path.abspath(os.fsdecode(os.fspath(file))))
            candidate = lexical.resolve(strict=False)
        except (TypeError, ValueError, OSError, RuntimeError):
            return file
        if candidate not in (self.logical, self.snapshot) and lexical not in (self.logical, self.snapshot):
            return file
        if not isinstance(mode, str):
            raise TypeError('Mapped input mode must be a string')
        if any(value in mode for value in 'wax+'):
            raise PermissionError('Frozen runtime inputs are read-only')
        if mode not in ('r', 'rt', 'tr', 'rb', 'br'):
            raise ValueError('Only ordinary read modes are supported for frozen inputs')
        if options and options.get('opener') is not None:
            raise PermissionError('Custom openers are forbidden for frozen inputs')
        if lexical == self.snapshot or candidate == self.snapshot:
            self._verify_snapshot()
            return self.snapshot
        self._verify_snapshot()
        self.reads.append(dict(api=api, mode=mode))
        return self.snapshot

    def __enter__(self):
        if self.entered or self.finished:
            raise RuntimeError('A frozen-input context may be entered only once')
        if not _ACTIVE.acquire(blocking=False):
            raise RuntimeError('Nested or simultaneous frozen-input contexts are forbidden')
        self.original = (Path.open, Path.read_text, Path.read_bytes, builtins.open)
        try:
            self._verify_snapshot()
            self.before = _digest(self.logical, self.original[3])
            old_path_open, old_text, old_bytes, old_open = self.original

            def path_open(path, mode='r', *args, **kwargs):
                return old_path_open(self._route(path, mode, 'Path.open', kwargs), mode, *args, **kwargs)

            def read_text(path, *args, **kwargs):
                return old_text(self._route(path, 'r', 'Path.read_text'), *args, **kwargs)

            def read_bytes(path, *args, **kwargs):
                return old_bytes(self._route(path, 'rb', 'Path.read_bytes'), *args, **kwargs)

            def open_file(file, mode='r', *args, **kwargs):
                options = dict(kwargs)
                if len(args) > 5:
                    options['opener'] = args[5]
                return old_open(self._route(file, mode, 'builtins.open', options), mode, *args, **kwargs)

            self.hooks = (path_open, read_text, read_bytes, open_file)
            Path.open, Path.read_text, Path.read_bytes, builtins.open = self.hooks
            self.entered = True
            return self
        except BaseException:
            Path.open, Path.read_text, Path.read_bytes, builtins.open = self.original
            _ACTIVE.release()
            raise

    def __exit__(self, kind, error, traceback):
        current = (Path.open, Path.read_text, Path.read_bytes, builtins.open)
        Path.open, Path.read_text, Path.read_bytes, builtins.open = self.original
        self.finished = True
        try:
            self._verify_snapshot()
            self.after = _digest(self.logical, self.original[3])
            if self.after != self.before:
                raise ValueError('Live ledger changed during frozen-input context')
            if current != self.hooks:
                raise RuntimeError('Read hooks changed unexpectedly during frozen-input context')
        finally:
            _ACTIVE.release()
        return False

    def receipt(self):
        return dict(fromPath=self.from_path, expectedSha256=self.expected,
            snapshotPath=self.snapshot.relative_to(self.root).as_posix(), snapshotSha256=self.expected,
            liveSha256Before=self.before, liveSha256After=self.after, readCalls=list(self.reads),
            completed=self.finished, liveLedgerUnchanged=self.finished and self.before == self.after,
            statHooked=False, scope='Four Python read APIs; not an OS sandbox or subprocess remapping')
