import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PRODUCERS = ['replay_save_core_preparation301_20261101.py',
    'evidence/application/save_core_glyph305_fixtures_20261101.py',
    'evidence/application/save_core_preview317_fixtures_20261101.py']


def main():
    if len(sys.argv) > 1:
        reads = set()
        def audit(event, args):
            if event != 'open' or not isinstance(args[0], (str, bytes)):
                return
            try:
                path = Path(args[0]).resolve()
                if path.is_relative_to(ROOT) and not (isinstance(args[1], str) and any(c in args[1] for c in 'wa+')):
                    reads.add(path.relative_to(ROOT).as_posix())
            except (OSError, ValueError, TypeError):
                pass
        sys.dont_write_bytecode = True
        sys.addaudithook(audit)
        sys.argv = [str(ROOT / sys.argv[1])]
        runpy.run_path(sys.argv[0], run_name='__main__')
        return reads
    rows = []
    for index, producer in enumerate(PRODUCERS):
        output = ROOT / f'work/save-core/preparation320/read-{index}.json'
        output.parent.mkdir(parents=True, exist_ok=True)
        process = subprocess.run([sys.executable, str(Path(__file__).resolve()), producer, str(output)], cwd=ROOT, capture_output=True, text=True, timeout=900)
        assert process.returncode == 0, (producer, process.stdout[-500:], process.stderr[-1500:])
        reads = json.loads(output.read_text())
        rows.append(dict(producer=producer, reads=reads))
    files = sorted({p for row in rows for p in row['reads'] if not p.startswith(('work/', 'tools/', 'inputs/', 'extracted/', 'deps/'))})
    reports = [p for p in files if p.endswith(('.json', '.json.gz'))]
    path = ROOT / 'evidence/lanes/save-core/preparation320-read-closure-20261101.json'
    result = dict(schema=1, sourceCredit=0, producerReads=rows, nonScratchRepositoryReads=files, reportReads=reports,
        historicalConstructorReportRequired='evidence/application/save-core-constructor270-20261101.json' in files,
        limits=['Python read audit does not observe native compiler/linker file access; declared source/header/runtime closure remains separately pinned.',
        'Generated current work files and producer outputs are not preexisting replay dependencies.'])
    assert not result['historicalConstructorReportRequired']
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(reportReads=reports, files=len(files), historicalConstructorReportRequired=False)))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        output = Path(sys.argv[2])
        reads = main()
        output.write_text(json.dumps(sorted(reads), indent=2) + '\n')
    else:
        main()
