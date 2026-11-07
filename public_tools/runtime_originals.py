import argparse
import hashlib
import importlib
import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path


RUNTIME_MODULES = 9
DSD_SHA256 = '5917df26bffc05d4752276a2e0b1edd21bd6e920aabe1992be8a50efc9d10932'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def safe_local(root, name):
    path = Path(name)
    try:
        relative = path.relative_to(root) if path.is_absolute() else path
    except ValueError:
        raise ValueError('Original runtime input escapes its checkout') from None
    if relative.is_absolute() or '..' in relative.parts or not relative.parts:
        raise ValueError('Original runtime input is not a repository-local binary original')
    path = root
    for component in relative.parts:
        path = path / component
        if path.is_symlink() or path.is_junction():
            raise ValueError('Original runtime input traverses a symlink or junction')
    if not path.resolve().is_relative_to(root) or path.exists() and not path.is_file():
        raise ValueError('Original runtime input is not a regular file in its checkout')
    return path


def safe_binary(root, name):
    path = safe_local(root, name)
    relative = path.relative_to(root)
    if relative.parts[0] != 'extract' or relative.suffix not in {'.bin', '.srl'}:
        raise ValueError('Original runtime input is not a repository-local binary original')
    return path


def load_modules(root):
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root))
    result = []
    for name in ('arm7_runtime', 'utility_runtime'):
        expected = root / (name + '.py')
        existing = sys.modules.get(name)
        if existing is not None and Path(existing.__file__).resolve() != expected:
            raise ValueError('Runtime derivation imported another checkout')
        module = importlib.import_module(name)
        if Path(module.__file__).resolve() != expected or Path(module.ROOT).resolve() != root:
            raise ValueError('Runtime derivation imported another checkout')
        result.append(module)
    return result


def install_files(root, files):
    for path, content in files.items():
        safe_binary(root, path)
        if path.exists() and path.read_bytes() != content:
            raise ValueError('Existing original runtime file differs from its derived bytes')
    created, reused = 0, 0
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        safe_binary(root, path)
        if path.exists():
            if path.read_bytes() != content:
                raise ValueError('Original runtime file changed before reuse')
            reused += 1
        else:
            with path.open('xb') as stream:
                stream.write(content)
            created += 1
        if path.read_bytes() != content:
            raise ValueError('Materialized original runtime bytes differ')
    return created, reused


def stage_host_originals(root, expected, rom_hash, runner):
    missing = {path: value for path, value in expected.items() if not path.exists()}
    if not missing:
        return 0
    config_path = safe_local(root, 'project.json')
    config = json.loads(config_path.read_bytes())
    rom, dsd = [safe_local(root, config[key]) for key in ('rom', 'dsd')]
    if config['romSha256'] != rom_hash or digest(rom) != rom_hash or digest(dsd) != DSD_SHA256:
        raise ValueError('Pinned original ROM or DSD extraction tool differs')
    pins = {config_path: digest(config_path), rom: rom_hash, dsd: DSD_SHA256}
    stage = root / 'work' / ('runtime-originals-dsd-' + uuid.uuid4().hex)
    safe_local(root, stage / 'extraction-receipt.json')
    stage.mkdir(parents=True)
    output = stage / 'extract'
    command = [str(dsd), 'rom', 'extract', '--rom', str(rom), '--output-path', str(output)]
    run = runner(command, cwd=root, capture_output=True, timeout=600)
    (stage / 'dsd-extract.log').write_bytes(run.stdout + run.stderr)
    receipt = dict(passed=False, romSha256=rom_hash, dsdSha256=DSD_SHA256, command=command,
                   toolExitCode=run.returncode, originalFiles=[])
    try:
        if run.returncode:
            raise ValueError('Pinned DSD original extraction failed')
        if any(digest(path) != expected_hash for path, expected_hash in pins.items()):
            raise ValueError('Pinned ROM extraction inputs changed')
        files = {}
        for target, value in missing.items():
            source = safe_binary(stage, target.relative_to(root))
            if digest(source) != value['sha256'] or value.get('bytes') is not None and source.stat().st_size != value['bytes']:
                raise ValueError('Staged original image differs from its frozen identity')
            files[target] = source.read_bytes()
            receipt['originalFiles'].append(dict(path=target.relative_to(root).as_posix(),
                sha256=value['sha256'], bytes=len(files[target])))
        created, unused_reused = install_files(root, files)
        receipt.update(passed=True, createdOriginalFiles=created)
    finally:
        (stage / 'extraction-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    resolved = output.resolve()
    if (resolved.parent != stage.resolve() or not resolved.is_relative_to((root / 'work').resolve())
            or output.is_symlink() or output.is_junction()):
        raise ValueError('Disposable DSD extraction escaped its dedicated work directory')
    shutil.rmtree(resolved)
    return created


def materialize(root, runner=None):
    root = Path(root).resolve()
    arm7_path = safe_binary(root, 'extract/arm7/arm7.bin')
    utility_path = safe_binary(root, 'extract/files/dwc/utility.bin')
    layout_paths = [root / 'evidence/arm7/runtime-layout.json', root / 'evidence/utility/runtime-layout.json']
    ledger_path = root / 'ledger/modules.json'
    immutable = [safe_local(root, path) for path in [ledger_path, *layout_paths]]
    immutable += [root / 'arm7_runtime.py', root / 'utility_runtime.py']
    if (root / 'extract/config.yaml').exists():
        immutable.append(safe_local(root, 'extract/config.yaml'))
    frozen = [json.loads(path.read_bytes()) for path in layout_paths]
    inventory = json.loads(ledger_path.read_bytes())
    all_modules = {safe_binary(root, module['binary']): module for module in inventory['modules']}
    if len(all_modules) != 20 or len(inventory['modules']) != 20:
        raise ValueError('All twenty measured native original modules are required')
    parents = {arm7_path: dict(sha256=frozen[0]['imageSha256'], bytes=frozen[0]['imageBytes']),
               utility_path: dict(sha256=frozen[1]['inputSha256'], bytes=frozen[1]['inputBytes'])}
    expected = {**all_modules, **parents}
    for path, value in expected.items():
        if path.exists() and (digest(path) != value['sha256'] or path.stat().st_size != value['bytes']):
            raise ValueError('Existing original runtime file differs from its measured identity')
    immutable += [path for path in expected if path.exists()]
    before = {path: digest(path) for path in immutable}
    host = {path: value for path, value in expected.items()
            if '/runtime/' not in path.relative_to(root).as_posix()}
    extracted = stage_host_originals(root, host, inventory['buildSha256'], runner or subprocess.run)
    arm7, utility = load_modules(root)
    image = arm7_path.read_bytes()
    arm7_report = arm7.derive(image)
    utility_report, utility_files = utility.derive()
    if [arm7_report, utility_report] != frozen:
        raise ValueError('Derived runtime layout differs from its frozen proof')
    files = {}
    for module in arm7_report['modules']:
        start, size = module['inputFileOffset'], module['inputBytes']
        if type(start) is not int or type(size) is not int or start < 0 or size <= 0 or start + size > len(image):
            raise ValueError('ARM7 original module extent escapes its physical parent')
        files[safe_binary(root, module['binary'])] = image[start:start + size]
    for name, content in utility_files.items():
        path = safe_binary(root, name)
        if path in files or not isinstance(content, (bytes, bytearray)):
            raise ValueError('Runtime derivation returned duplicate or invalid original bytes')
        files[path] = bytes(content)
    measured = {}
    for module in inventory['modules']:
        name = module['binary'].replace('\\', '/')
        if name.startswith(('extract/arm7/runtime/', 'extract/utility/runtime/')):
            path = safe_binary(root, name)
            if path in measured:
                raise ValueError('Measured runtime module inventory is ambiguous')
            measured[path] = module
    if len(measured) != RUNTIME_MODULES or not set(measured).issubset(files):
        raise ValueError('Runtime derivation omitted measured original modules')
    for path, module in measured.items():
        content = files[path]
        if len(content) != module['bytes'] or hashlib.sha256(content).hexdigest() != module['sha256']:
            raise ValueError('Derived original runtime module differs from its measured identity')
    if any(digest(path) != expected for path, expected in before.items()):
        raise ValueError('Immutable runtime inputs changed during derivation')
    created, reused = install_files(root, files)
    for path, module in all_modules.items():
        if digest(path) != module['sha256'] or path.stat().st_size != module['bytes']:
            raise ValueError('Materialized native original inventory differs from its twenty measured modules')
    if any(digest(path) != expected for path, expected in before.items()):
        raise ValueError('Immutable runtime inputs or frozen layouts changed')
    return dict(passed=True, derivedRuntimeModules=len(measured), verifiedNativeModules=len(all_modules),
                stagedDsdOriginalFiles=extracted, createdOriginalFiles=created + extracted,
                reusedOriginalFiles=reused, frozenMetadataUnchanged=True, sourceCredit=0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        result = materialize(args.root)
    except Exception as error:
        print(json.dumps(dict(passed=False, errorType=type(error).__name__)), flush=True)
        return 1
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
