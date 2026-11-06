import copy
import json
import shutil
import subprocess
import sys
import uuid
from project import ROOT, read_json, write_json, sha256, now


def main():
    layout_name = 'src/utility/parallel_wave20261105/child-message-data/layout.json'
    layout = read_json(ROOT / layout_name)
    original_report = read_json(ROOT / 'evidence/data/child-message-semantic-20261106.json')
    clone = ROOT / 'work/child-message-data-copy' / uuid.uuid4().hex
    assert not clone.exists()
    clone.mkdir(parents=True)
    sources = ['project.py', 'project.json', 'audit_regions.py', 'utility_runtime.py',
               'match_child_message_data_20261106.py', 'child_message_data_codec_20261106.py', layout_name]
    sources += [row['semanticSource'] for row in layout['assets']]
    sources += ['extract/files/dwc/utility.bin', layout['binary'], 'tools/mwccarm/mwccarm/license.dat']
    tool_directory = ROOT / 'tools/mwccarm/mwccarm/2.0/base'
    sources += [path.relative_to(ROOT).as_posix() for path in tool_directory.iterdir()
                if path.is_file() and path.suffix.lower() in ['.exe', '.dll']]
    for name in sources:
        target = clone / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
        assert sha256(target) == sha256(ROOT / name)
    for package in ['ndspy', 'elftools']:
        shutil.copytree(ROOT / 'deps/native' / package, clone / 'deps/native' / package,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    assert not list(clone.rglob('*.o')) and not list(clone.rglob('*.elf'))
    report_path = clone / 'evidence/data/child-message-semantic-20261106.json'
    write_json(report_path, dict(staleReport=True, dataMatches=[]))
    def run():
        return subprocess.run([sys.executable, str(clone / 'match_child_message_data_20261106.py')],
                              cwd=clone, capture_output=True, text=True, timeout=180)
    result = run()
    assert result.returncode == 0, result.stdout + result.stderr
    fresh = read_json(report_path)
    assert len(fresh['dataMatches']) == 8 and fresh['dataMatchedBytes'] == 3808 and not fresh.get('staleReport')
    objects = []
    for old, new in zip(original_report['dataMatches'], fresh['dataMatches']):
        assert all(old[key] == new[key] for key in ['address', 'bytes', 'sourceSha256', 'targetSha256'])
        assert new['realLink']['exactDataBytes'] and new['sourceOnlyGeneration']
        assert sha256(clone / new['object']) == new['objectSha256']
        assert (clone / new['object']).is_file() and new['object'].startswith('work/child-message-data-native/objects/')
        objects.append(dict(address=new['address'], originalObjectSha256=old['objectSha256'],
                            copiedRootObjectSha256=new['objectSha256'], freshObject=True))
    clean_layout = copy.deepcopy(layout)
    first = clone / layout['assets'][0]['semanticSource']
    clean_source = first.read_bytes()
    clean_module = (clone / layout['binary']).read_bytes()
    controls = []
    def negative(label, mutation):
        (clone / layout_name).write_bytes((ROOT / layout_name).read_bytes())
        first.write_bytes(clean_source)
        (clone / layout['binary']).write_bytes(clean_module)
        before = {str(path): sha256(path) for path in (clone / 'work/child-message-data-native/objects').glob('*.o')}
        mutation()
        bad = run()
        assert bad.returncode != 0, label
        assert before == {str(path): sha256(path) for path in (clone / 'work/child-message-data-native/objects').glob('*.o')}
        controls.append(dict(case=label, rejectedBeforeNewObject=True, exitCode=bad.returncode))
    def changed_message():
        value = read_json(first)
        message = next(row for row in value['source']['messages'] if row['stringParts'])
        message['stringParts'][0] += 'changed'
        write_json(first, value)
        value = copy.deepcopy(clean_layout)
        value['assets'][0]['semanticSourceSha256'] = sha256(first)
        write_json(clone / layout_name, value)
    def wrong_alignment():
        value = read_json(first)
        value['storageAlignment'] = 1
        write_json(first, value)
        value = copy.deepcopy(clean_layout)
        value['assets'][0]['semanticSourceSha256'] = sha256(first)
        write_json(clone / layout_name, value)
    def wrong_namespace():
        value = copy.deepcopy(clean_layout)
        value['processor'] = 'arm7'
        write_json(clone / layout_name, value)
    def changed_original_module():
        value = bytearray(clean_module)
        value[0] ^= 1
        (clone / layout['binary']).write_bytes(value)
    negative('changed-semantic-source-with-updated-source-hash', changed_message)
    negative('wrong-storage-alignment-with-updated-source-hash', wrong_alignment)
    negative('wrong-cpu-namespace', wrong_namespace)
    negative('changed-private-original-module', changed_original_module)
    write_json(ROOT / 'evidence/lanes/parallel-wave20261105/child-message-data/copied-root-controls.json',
        dict(passed=True, sourceCredit=0, initializedBytes=3808, functionCount=0, freshCopiedObjects=objects,
             staleReportReplaced=True, staleWorkObjectsUsed=False, sourceGenerationOriginalReadRejections=2,
             controls=controls, copiedRoot=clone.relative_to(ROOT).as_posix(), createdUtc=now(),
             generatorSha256=sha256(__file__), originalReportSha256=sha256(ROOT / 'evidence/data/child-message-semantic-20261106.json')))
    print(dict(passed=True, freshObjects=8, initializedDataBytes=3808, controls=len(controls), sourceCredit=0))


if __name__ == '__main__':
    main()
