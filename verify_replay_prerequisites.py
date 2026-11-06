import tempfile
from pathlib import Path
from project import ROOT, write_json
from recovery_order import order_batches, RecoveryOrderError


def main():
    work = ROOT / 'work/replay-prerequisite-controls'
    work.mkdir(parents=True, exist_ok=True)
    controls = []

    def run(name, definitions, expected=None, rejection=None, batch_requires=None):
        with tempfile.TemporaryDirectory(prefix=name + '-', dir=work) as directory:
            root = Path(directory)
            items = []
            for path, requires, namespace in definitions:
                write_json(root / path, {'romSha256': namespace, 'matches': [], 'replayRequires': requires})
                items.append({'report': path, **({'replayRequires': batch_requires} if batch_requires is not None else {})})
            try:
                result = order_batches(items, root=root)
            except RecoveryOrderError as error:
                if rejection is None or rejection not in str(error):
                    raise AssertionError((name, str(error), rejection))
                controls.append({'name': name, 'rejected': True, 'reason': str(error)})
                return
            if rejection:
                raise AssertionError('Invalid prerequisite graph accepted: ' + name)
            actual = [row['report'] for row in result]
            assert actual == expected, (name, actual, expected)
            controls.append({'name': name, 'passed': True, 'order': actual})

    namespace = 'a' * 64
    run('producer-after-consumer-lexically', [('a.json', ['z.json'], namespace), ('z.json', [], namespace)], ['z.json', 'a.json'])
    run('three-stage-generated-chain', [('a.json', ['b.json'], namespace), ('b.json', ['z.json'], namespace),
                                       ('z.json', [], namespace)], ['z.json', 'b.json', 'a.json'])
    run('shared-generated-producer', [('a.json', ['z.json'], namespace), ('b.json', ['z.json'], namespace),
                                     ('z.json', [], namespace)], ['z.json', 'a.json', 'b.json'])
    run('missing-producer', [('a.json', ['missing.json'], namespace)], rejection='Missing registered replay prerequisite')
    run('self-dependency', [('a.json', ['a.json'], namespace)], rejection='Self replay prerequisite')
    run('wrong-ROM', [('a.json', ['z.json'], namespace), ('z.json', [], 'b' * 64)], rejection='build namespace differs')
    run('string-not-list', [('a.json', 'z.json', namespace)], rejection='must be a list')
    run('non-path-entry', [('a.json', [17], namespace)], rejection='must be a list')
    run('cycle', [('a.json', ['z.json'], namespace), ('z.json', ['a.json'], namespace)], rejection='dependency cycle')
    run('registry-prerequisite-checked', [('a.json', [], namespace)], rejection='Missing registered replay prerequisite',
        batch_requires=['missing.json'])
    write_json(ROOT / 'evidence/verification/replay-prerequisite-controls-20261030.json',
               {'passed': True, 'controls': controls, 'newSourceCredit': 0, 'cachedObjectsUsed': False})
    print({'passed': True, 'controls': len(controls)}, flush=True)


if __name__ == '__main__':
    main()
