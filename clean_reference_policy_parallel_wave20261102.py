import hashlib
import json
from pathlib import Path
import subprocess


REFERENCE_NAMES = ('ansi', 'ceil', 'floor', 'math')
EXCLUDED = {'build', 'work', 'extract', 'asm', 'logs', 'inputs', 'tools', 'deps', '.git', '__pycache__'}


def reference_pins(read_blob):
    pins = {}
    for name in REFERENCE_NAMES:
        manifest = 'provenance/msl-' + name + '-reference-20261031.json'
        document = json.loads(read_blob(manifest))
        if document.get('sourceCredit') != 0 or document.get('revision') != '177da59137be40bcca5cd996e013c228ae20b198':
            raise ValueError('Committed MSL reference identity differs')
        prefix = Path('deps/msl-' + name + '-reference-20261031')
        for row in document['files']:
            relative = Path(row['path'])
            if relative.is_absolute() or '..' in relative.parts or not relative.is_relative_to(prefix):
                raise ValueError('Committed MSL reference escaped its declared directory')
            if relative.suffix not in ('.c', '.h') and relative.name != 'LICENSE':
                raise ValueError('Committed MSL reference is not ordinary source or a license')
            if row['path'] in pins:
                raise ValueError('Duplicate committed MSL reference')
            if hashlib.sha256(read_blob(row['path'])).hexdigest() != row['sha256']:
                raise ValueError('Committed MSL reference bytes differ from provenance')
            pins[row['path']] = row['sha256']
    if len(pins) != 10:
        raise ValueError('Complete committed MSL reference set differs')
    return pins


def committed_reference_pins(root, revision):
    def read_blob(name):
        return subprocess.run(['git', 'show', revision + ':' + name], cwd=root,
            check=True, capture_output=True).stdout
    return reference_pins(read_blob)


def validate_source_paths(paths, pins):
    for relative in paths:
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Tracked source snapshot path escaped the project')
        if relative.parts[0] in EXCLUDED and relative.as_posix() not in pins:
            raise ValueError('Tracked source snapshot contains cached outputs or private input payloads: ' + relative.as_posix())


def verify_reference_copy(relative, source, target, pins):
    name = relative.as_posix()
    if name not in pins:
        return False
    expected = pins[name]
    if hashlib.sha256(source.read_bytes()).hexdigest() != expected or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
        raise ValueError('Copied MSL reference would differ from the immutable committed source: ' + name)
    return True
