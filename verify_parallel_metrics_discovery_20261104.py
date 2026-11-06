import json
from pathlib import Path
import tempfile
from project import ROOT, write_json, sha256
from parallel_metrics import queue_snapshot


class Accepted:
    def read(self, name, revision=None):
        assert name == 'ledger/functions.jsonl'
        return ''


def packet(address, size, rom):
    row = dict(program='', processor='arm9', module='ov005', mode='arm', address=hex(address), bytes=size)
    return dict(status='ready-for-coordinator-acceptance', romSha256=rom,
        functions=1, bytes=size, identities=[row])


def main():
    work = ROOT / 'work/parallel-wave20261104/metrics-discovery'
    work.mkdir(parents=True, exist_ok=True)
    controls = []
    with tempfile.TemporaryDirectory(dir=work) as folder:
        root = Path(folder)
        rom = '0' * 64
        latest = dict(sourceCommit='a' * 40, cohort=150, romSha256=rom)
        lanes = root / 'evidence/lanes'
        paths = [('parallel-wave20261102/old/ready.json', packet(0x1000, 4, rom)),
                 ('parallel-wave20261104/new/ready.json', packet(0x2000, 8, rom)),
                 ('parallel-wave20261104/new/supplement/coordinator-ready.json', packet(0x3000, 12, rom))]
        for name, data in paths:
            write_json(lanes / name, data)
        snapshot = queue_snapshot(root, Accepted(), latest)
        assert snapshot['ready']['functions'] == 3 and snapshot['ready']['bytes'] == 24
        controls.append(dict(name='old-new-and-nested-wave-handoffs-discovered', passed=True))
        write_json(lanes / 'parallel-wave20261104/new/duplicate-ready.json', paths[1][1])
        snapshot = queue_snapshot(root, Accepted(), latest)
        assert snapshot['ready']['functions'] == 3 and snapshot['ready']['bytes'] == 24
        controls.append(dict(name='cross-path-duplicate-handoffs-still-deduplicated', passed=True))
        write_json(lanes / 'parallel-wave20261104/wrong/ready.json', packet(0x4000, 16, 'f' * 64))
        snapshot = queue_snapshot(root, Accepted(), latest)
        assert snapshot['ready']['bytes'] == 24 and len(snapshot['invalidReadyPackets']) == 1
        controls.append(dict(name='wrong-ROM-never-receives-ready-or-accepted-credit', passed=True))
        write_json(lanes / 'other-work/ready.json', packet(0x5000, 20, rom))
        write_json(lanes / 'parallel-wave20261104/draft/ready.json', dict(status='draft'))
        snapshot = queue_snapshot(root, Accepted(), latest)
        assert snapshot['ready']['bytes'] == 24
        controls.append(dict(name='unrelated-and-draft-metadata-excluded', passed=True))
        assert snapshot['scope'] == 'Observed working-tree handoffs; zero accepted credit'
        controls.append(dict(name='queue-observation-remains-zero-source-credit', passed=True))
    write_json(ROOT / 'evidence/lanes/parallel-wave20261104/metrics-discovery-controls.json',
        dict(passed=True, sourceCredit=0, controls=controls,
            generator=Path(__file__).name, generatorSha256=sha256(__file__),
            metricsSha256=sha256(ROOT / 'parallel_metrics.py')))
    print(dict(passed=True, controls=len(controls)))


if __name__ == '__main__':
    main()
