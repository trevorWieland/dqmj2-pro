import runpy
import sys
from pathlib import Path
from unittest.mock import patch
import project
from project import ROOT, read_json, write_json, sha256


def main():
    arguments = list(sys.argv[1:])
    assert arguments and not arguments[0].startswith('-')
    config = read_json(ROOT / arguments[0])
    board = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    before = sha256(board)
    proposed = {}
    original_write = project.write_json

    def defer(path, value):
        if Path(path).resolve() == board.resolve():
            assert not proposed
            proposed.update(value)
        else:
            original_write(path, value)

    script = ROOT / 'intake_parallel_ready_packet_20261105.py'
    with patch.object(project, 'write_json', side_effect=defer), patch.object(sys, 'argv', [str(script), *arguments]):
        runpy.run_path(str(script), run_name='__main__')
    assert proposed and sha256(board) == before
    def option(name):
        return arguments[arguments.index(name) + 1]
    name, owner = option('--ready'), option('--owner')
    ready = read_json(ROOT / name)
    cohort = config['cohort']
    folder = ROOT / 'evidence/lanes/parallel-wave20261105/deferred-packet-intake'
    folder.mkdir(exist_ok=True, parents=True)
    output = folder / (f'cohort{cohort}-' + option('--packet-id') + '.json')
    assert not output.exists()
    write_json(output, dict(passed=True, sourceCredit=0, sharedDispatchUnchanged=True,
        originalDispatchSha256=before, configuration=arguments[0], cohort=cohort,
        ready=name, readySha256=sha256(ROOT / name), owner=owner,
        packetId=option('--packet-id'), handedOffReports=[row['report'] for row in ready['packets']],
        pendingAggregate=proposed[f'pendingAggregate{cohort}'],
        specification=config['name'] + '-specification.json',
        specificationSha256=sha256(ROOT / (config['name'] + '-specification.json')),
        originalIntakeSha256=sha256(script), deferredIntakeSha256=sha256(__file__),
        nativeGuardsAndFrozenMembershipChecksRetained=True,
        sharedDispatchMergeRequiredAfterPackageClosure=True))
    print(dict(passed=True, sourceCredit=0, actualDispatchUnchanged=True,
        deferredOperation=output.relative_to(ROOT).as_posix()))


if __name__ == '__main__':
    main()
