import hashlib
import json
import subprocess
from project import ROOT, read_json, sha256


def protected(namespace, revision):
    intervals, pins = [], []

    def walk(node, parent):
        if isinstance(node, list):
            for row in node:
                walk(row, parent)
        elif isinstance(node, dict):
            context = {key: node.get(key) or parent.get(key) for key in ['program', 'processor', 'module']}
            module = context['module']
            if module:
                program = context['program'] or ('dwc/utility.bin/move/child.srl' if module.startswith('utility-child-') else '')
                cpu = context['processor'] or ('arm7' if 'arm7' in module else 'arm9')
                if (program, cpu, module) == namespace and node.get('address'):
                    size = node.get('storedBytes', node.get('bytes', node.get('size')))
                    if size:
                        start = int(node['address'], 0) if isinstance(node['address'], str) else node['address']
                        if isinstance(size, str):
                            size = len(bytes.fromhex(size)) if 'instruction' in node else int(size, 0)
                        assert type(size) is int and size > 0
                        intervals.append((start, start + size))
            for value in node.values():
                walk(value, context)

    for name, key in [('ledger/functions.jsonl', None), ('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        raw = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(raw).hexdigest()))
        walk([json.loads(line) for line in raw.splitlines()] if key is None else json.loads(raw)[key], {})
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
                   set((ROOT / 'evidence/lanes').rglob('data-claim.json')) |
                   set(ROOT.glob('cohort16*-*specification.json')))
    for path in paths:
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        walk(read_json(path), {})
    ghidra = ROOT / 'evidence/utility/ghidra-arm9.json'
    pins.append(dict(path=ghidra.relative_to(ROOT).as_posix(), sha256=sha256(ghidra)))
    for row in read_json(ghidra)['functions']:
        if row['module'] == namespace[2]:
            intervals.extend((int(a, 0), int(b, 0)) for a, b in row['ranges'])
    if namespace == ('dwc/utility.bin/move/child.srl', 'arm9', 'utility-child-arm9-main'):
        intervals.append((0x020111e8, 0x02011200))
    return intervals, pins
