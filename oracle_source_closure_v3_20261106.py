import ast
import hashlib
import json
import re
import subprocess
from project import ROOT,read_json,write_json,sha256
from static_json_reads_20261031 import required_json_reads
from oracle_source_closure_v2_20261106 import LEGACY_SHA256,EXCLUDED,SKIP,EXTENSIONS,_parent_requires_hashes
from collector_path_lookup_epoch_20261106 import PathLookupEpoch
V2_SHA256='f4b070a006e0c2ec6010876a086843bf16be3e52c1915e2cc23eeb971b452eb5'
SEARCH=[ROOT,ROOT/'evidence/application',ROOT/'evidence/encounter',ROOT/'evidence/save',ROOT/'nonmatching/encounter']


def collect():
    if sha256(ROOT / 'oracle_source_closure_20261031.py') != LEGACY_SHA256:
        raise ValueError('Pinned legacy source closure collector changed')
    if sha256(ROOT / 'oracle_source_closure_v2_20261106.py') != V2_SHA256:
        raise ValueError('Pinned qualifiedv2source closure collector changed')
    lookup = PathLookupEpoch(ROOT)
    parent_context = {}
    registry = lookup.read_json(ROOT / 'recovery.json')
    pending = []
    paths = {}
    missing = []
    reports = []
    seen = set()
    oracle_reports = set()
    processed = 0
    static_reads = set()

    def add(value, parent=ROOT, required=False):
        if not isinstance(value, str) or not 0 < len(value) < 512 or '\n' in value or ('\r' in value) or ('\x00' in value):
            return
        value = value.replace('\\', '/')
        path = None
        key = (value, str(parent), required)
        if key in seen:
            return
        seen.add(key)
        if not any((value.lower().endswith(ext) for ext in EXTENSIONS)):
            return
        for base in dict.fromkeys([ROOT, parent, *SEARCH]):
            candidate = lookup.resolve(base / value)
            if not candidate.is_relative_to(ROOT) or candidate.relative_to(ROOT).parts[0] in EXCLUDED:
                continue
            try:
                exists = lookup.is_file(candidate)
            except OSError:
                exists = False
            if exists:
                path = candidate
                break
        if path is None:
            if required:
                missing.append(value)
            return
        if path.suffix.lower() not in EXTENSIONS:
            return
        relative = path.relative_to(ROOT).as_posix()
        if relative == 'evidence/verification/oracle-source-closure-20261031.json' or relative.startswith('evidence/encounter/script-cfg-20261029/'):
            return
        if relative not in paths:
            paths[relative] = lookup.hash(path)
            pending.append(path)

    def walk(value, parent, required_hashes=False):
        if isinstance(value, dict):
            for key, item in value.items():
                if _parent_requires_hashes(required_hashes, parent, ROOT, parent_context) and key in {'path', 'source', 'header', 'profile'} and isinstance(item, str) and any((isinstance(digest, str) and re.fullmatch('[0-9a-fA-F]{64}', digest) for label, digest in value.items() if label in {'sha256', 'sourceSha256', 'headerSha256', 'profileSha256'})):
                    candidate = ROOT / item.replace('\\', '/')
                    if lookup.resolve(candidate).is_relative_to(ROOT) and candidate.relative_to(ROOT).parts[0] not in EXCLUDED:
                        add(item, parent, required=True)
                if key not in SKIP:
                    walk(item, parent, required_hashes)
        elif isinstance(value, list):
            for item in value:
                walk(item, parent, required_hashes)
        elif isinstance(value, str):
            add(value, parent)
    for name in ['run_checks.py', 'configure.py', 'validate_clean_checkout.py']:
        add(name, required=True)
    interpreted = lookup.read_json(ROOT / 'interpreted-recovery.json') if lookup.is_file(ROOT / 'interpreted-recovery.json') else {}
    batches = [*registry.get('batches', []), *interpreted.get('batches', [])]
    for oracle in [*registry['oracles'], *batches]:
        for token in oracle['reproduce']:
            if isinstance(token, str) and token.endswith('.py'):
                add(token, required=True)
        report = oracle['report']
        reports.append(report)
        oracle_reports.add(report.replace('\\', '/'))
        add(report, required=True)
        for relative in oracle.get('sourceHashes', {}):
            if relative.replace('\\', '/').split('/')[0] not in EXCLUDED:
                add(relative, required=True)
    while pending:
        path = pending.pop()
        processed += 1
        if processed % 250 == 0:
            print({'processed': processed, 'discovered': len(paths), 'pending': len(pending)}, flush=True)
        if path.suffix == '.py':
            tree = ast.parse(path.read_text(encoding='utf-8-sig'))
            for relative in required_json_reads(tree, ROOT):
                if relative.split('/')[0] not in EXCLUDED:
                    newly_required = relative not in static_reads
                    static_reads.add(relative)
                    add(relative, path.parent, required=True)
                    if newly_required and relative in paths and (ROOT / relative not in pending):
                        pending.append(ROOT / relative)
            for node in ast.walk(tree):
                modules = [x.name for x in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.module else []
                for name in modules:
                    add(name.replace('.', '/') + '.py', path.parent)
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    value = node.value
                    if value.endswith(tuple(EXTENSIONS)):
                        add(value, path.parent)
                    elif re.fullmatch('[A-Za-z_]\\w*(?:\\.[A-Za-z_]\\w*)*', value):
                        add(value.replace('.', '/') + '.py', path.parent)
        elif path.suffix == '.json' and (path.relative_to(ROOT).as_posix() in oracle_reports | static_reads or path.relative_to(ROOT).parts[0] in {'nonmatching', 'config', 'provenance'}):
            try:
                document = lookup.read_json(path)
            except (ValueError, UnicodeError):
                continue
            pinned_files = path.relative_to(ROOT).as_posix() in static_reads and path.relative_to(ROOT).parts[0] != 'provenance' and isinstance(document, dict) and isinstance(document.get('files'), list)
            walk(document, path.parent, pinned_files)
        elif path.suffix in ['.c', '.cpp', '.h', '.inc']:
            for include in re.findall('^\\s*#include\\s+"([^"]+)"', path.read_text(encoding='utf-8-sig'), re.M):
                add(include, path.parent)
    result = {'schemaVersion': 2, 'sourceCredit': 0, 'registrySha256': lookup.hash(ROOT / 'recovery.json'), 'oracleCount': len(registry['oracles']), 'registeredBatchCount': len(batches), 'oracleReports': [row['report'] for row in registry['oracles']], 'registeredReports': reports, 'staticJsonReads': sorted(static_reads), 'sourceAndEvidenceHashes': dict(sorted(paths.items())), 'missingRequiredPaths': sorted(set(missing)), 'scope': 'Native/interpreted batch and oracle commands/reports/source hashes, recursively resolved imports, static JSON reads, immutable pin files, nonmatching/config/provenance JSON inputs and quoted C includes', 'limitations': ['Static discovery cannot prove dynamically constructed runtime inputs; clean execution remains required', 'Unreferenced historical evidence JSON is not recursively expanded', 'This does not replace accepted source hash checks, input/tool pins, current-product gates or fresh full-suite execution']}
    lookup.verify()
    return result
