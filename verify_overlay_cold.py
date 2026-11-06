import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from project import ROOT, read_json, sha256, write_json

BATCHES = ('ov000-reuse01', 'ov001-reuse01')


def regular(path):
    if path.is_symlink() or path.is_junction() or getattr(path.lstat(), 'st_file_attributes', 0) & 1024:
        raise ValueError('Replay inputs must be materialized files, not reparse points: ' + str(path))


def copy_file(relative, destination, copied):
    source = ROOT / relative
    regular(source)
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    entry = {'path': relative, 'bytes': target.stat().st_size}
    if relative.endswith('/license.dat'):
        entry['copiedWithoutContentInspection'] = True
    else:
        entry['sha256'] = sha256(target)
        if entry['sha256'] != sha256(source):
            raise ValueError('Replay copy changed an input file')
    copied.append(entry)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination', type=Path)
    args = parser.parse_args()
    if platform.python_version() != '3.13.5':
        raise ValueError('Cold replay requires pinned Python3.13.5')
    destination = (args.destination or ROOT.parent / ('j2p-overlay-replay-' + uuid.uuid4().hex[:10])).resolve()
    if destination.exists() or destination == ROOT or not destination.parent.exists():
        raise ValueError('Replay needs a new local directory with an existing parent')
    reports = {batch: read_json(ROOT / f'evidence/matches/{batch}.json') for batch in BATCHES}
    files = {'reuse_overlay_c.py', 'match_runtime.py', 'project.py', 'project.json', 'provenance/seed-manifest.json', 'inputs/game.nds', 'inputs/save.sav'}
    for batch, report in reports.items():
        files.update({f'evidence/matches/{batch}.json', f"extract/arm9_overlays/{report['module']}.bin", f"config/arm9/overlays/{report['module']}/symbols.txt"})
        for entry in report['matches']:
            files.update((entry['source'], entry['sourceReuseProvenance']['source']))
            if sha256(ROOT / entry['source']) != entry['sourceSha256'] or sha256(ROOT / entry['sourceReuseProvenance']['source']) != entry['sourceReuseProvenance']['sourceSha256']:
                raise ValueError('Frozen source/provenance changed before cold copy')
            compiler = entry.get('compilerPath', entry.get('compiler'))
            if compiler != 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe' or sha256(ROOT / compiler) != entry['compilerSha256']:
                raise ValueError('Unexpected compiler in the targeted overlay source cohort')
    files.update('tools/mwccarm/mwccarm/2.0/base/' + name for name in ('mwccarm.exe', 'ELFIO.dll', 'lmgr8c.dll', 'MSL_All-DLL80_x86.dll'))
    files.add('tools/mwccarm/mwccarm/license.dat')
    for package in ('elftools', 'unicorn'):
        folder = ROOT / 'deps/native' / package
        regular(folder)
        for path in folder.rglob('*'):
            regular(path)
            if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc', '.lib', '.o', '.elf'):
                files.add(path.relative_to(ROOT).as_posix())
    destination.mkdir()
    copied = []
    for relative in sorted(files):
        if Path(relative).suffix in ('.o', '.elf') or relative.startswith(('work/', 'build/', 'oracle/')):
            raise ValueError('Old compiled artifacts are forbidden in cold replay inputs')
        copy_file(relative, destination, copied)
    forbidden = [path for path in destination.rglob('*') if path.suffix in ('.o', '.elf') or path.is_symlink() or path.is_junction()]
    if forbidden or (destination / 'work').exists() or (destination / 'build').exists():
        raise ValueError('Cold replay directory contains old artifacts or links')
    guard = destination / 'replay_guard.py'
    guard.write_text("import json\nimport runpy\nimport sys\nfrom pathlib import Path\nroot=Path.cwd().resolve()\nforbidden=Path(sys.argv[1]).resolve()\nbatch=sys.argv[2]\nmodule=sys.argv[3]\ncommands=[]\ndef audit(event,args):\n    if event=='open' and isinstance(args[0],(str,bytes)):\n        candidate=Path(args[0]).resolve()\n        if candidate.is_relative_to(forbidden):\n            raise RuntimeError('Forbidden old-root open: '+str(candidate))\n    if event=='subprocess.Popen':\n        executable,argv,cwd,env=args\n        if any(str(forbidden).lower() in str(value).lower() for value in argv):\n            raise RuntimeError('Compiler invocation refers to old root')\n        commands.append({'executable':str(executable),'argv':argv,'cwd':str(cwd),'licensePath':env.get('LM_LICENSE_FILE')})\nsys.addaudithook(audit)\nsys.argv=['reuse_overlay_c.py',module,'--batch',batch,'--verify']\ntry:\n    runpy.run_path('reuse_overlay_c.py',run_name='__main__')\nfinally:\n    (root/(batch+'-compiler-invocations.json')).write_text(json.dumps(commands,indent=2)+'\\n')\n")
    environment = dict(os.environ, PYTHONPATH='', PYTHONDONTWRITEBYTECODE='1')
    runs = []
    for batch, report in reports.items():
        command = [sys.executable, str(guard), str(ROOT), batch, report['module']]
        log = destination / (batch + '-replay.log')
        with log.open('w') as output:
            process = subprocess.run(command, cwd=destination, env=environment, stdout=output, stderr=subprocess.STDOUT, timeout=600)
        runs.append({'batch': batch, 'command': command, 'exitCode': process.returncode, 'log': str(log), 'logSha256': sha256(log)})
        if process.returncode:
            raise ValueError('Cold overlay replay failed; preserved log at ' + str(log))
    compared = []
    for batch, old in reports.items():
        path = destination / f'evidence/matches/{batch}.json'
        fresh = read_json(path)
        old_entries = {entry['name']: entry for entry in old['matches']}
        if set(old_entries) != {entry['name'] for entry in fresh['matches']}:
            raise ValueError('Cold replay changed the accepted source function set')
        for entry in fresh['matches']:
            before = old_entries[entry['name']]
            for key in ('sourceSha256', 'address', 'module', 'mode', 'bytes', 'targetSha256', 'outputSha256', 'compilerSha256', 'compilerFlags', 'sourceReuseProvenance'):
                if before[key] != entry[key]:
                    raise ValueError('Cold replay changed source/native provenance: ' + key)
            obj = destination / entry['object']
            if not obj.is_relative_to(destination) or sha256(obj) != entry['objectSha256']:
                raise ValueError('Rebuilt object is absent or outside the cold checkout')
            compared.append({'batch': batch, 'name': entry['name'], 'module': entry['module'], 'address': entry['address'], 'bytes': entry['bytes'],
                             'oldObjectSha256': before['objectSha256'], 'freshObjectSha256': entry['objectSha256'], 'objectHashRefreshed': before['objectSha256'] != entry['objectSha256'],
                             'sourceSha256': entry['sourceSha256'], 'nativeSpanSha256': entry['targetSha256'], 'freshObject': str(obj)})
        invocations = read_json(destination / (batch + '-compiler-invocations.json'))
        if len(invocations) != len(fresh['matches']):
            raise ValueError('Cold replay did not freshly compile every accepted C function')
    result = {'schemaVersion': 1, 'createdUtc': datetime.now(timezone.utc).isoformat(), 'originRoot': str(ROOT), 'freshRoot': str(destination),
              'python': {'path': sys.executable, 'version': platform.python_version(), 'sharedPinnedHostRuntime': True}, 'oldObjectCountBeforeReplay': 0,
              'copiedWorkOrBuildDirectories': False, 'copiedLinks': False, 'oldRootReadsBlockedDuringReplay': True, 'copiedInputs': copied,
              'runs': runs, 'functions': len(compared), 'sourceBytes': sum(entry['bytes'] for entry in compared),
              'refreshedObjectHashes': sum(entry['objectHashRefreshed'] for entry in compared), 'objects': compared,
              'limitations': ['This is an independent targeted C/oracle replay, not a new full-module or ROM-container link', 'The pinned host Python and standard Windows runtime are shared; source,private inputs,compiler DLLs and Python extension dependencies are materialized copies', 'License material is copied without content inspection; no license content appears in this evidence']}
    write_json(ROOT / 'evidence/verification/overlay-cold-replay.json', result)
    print({'freshRoot': str(destination), 'functions': result['functions'], 'bytes': result['sourceBytes'], 'refreshedObjectHashes': result['refreshedObjectHashes'], 'oldObjectsBeforeReplay': 0})


if __name__ == '__main__':
    main()
