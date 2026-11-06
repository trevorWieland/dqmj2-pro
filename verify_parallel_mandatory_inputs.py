from pathlib import Path
import tempfile
from project import ROOT, write_json, sha256
from prepare_parallel_packet_wave import mandatory_inputs


def main():
    work = ROOT / 'work/parallel-wave20261102/mandatory-input-controls'
    work.mkdir(parents=True, exist_ok=True)
    controls = []
    with tempfile.TemporaryDirectory(dir=work) as folder:
        root = Path(folder)
        external = root / 'inventory.json'
        write_json(external, dict(entries=[1, 2, 3]))
        external_pin = dict(path='inventory.json', sha256=sha256(external))
        manifest = root / 'manifest.json'
        write_json(manifest, dict(mandatoryExternalInputs=[external_pin]))
        original = dict(path='manifest.json', sha256=sha256(manifest))
        assert mandatory_inputs([original], root) == [original, external_pin]
        assert mandatory_inputs([original, external_pin], root) == [original, external_pin]
        controls.append(dict(name='promote-and-deduplicate-real-external-input-pins', passed=True))

        def reject(name, values):
            try:
                mandatory_inputs(values, root)
            except (ValueError, KeyError):
                controls.append(dict(name=name, rejected=True))
                return
            raise AssertionError('Invalid mandatory input accepted: ' + name)

        reject('changed-manifest', [dict(original, sha256='0' * 64)])
        reject('conflicting-direct-external-identity', [original, dict(external_pin, sha256='0' * 64)])
        write_json(external, dict(entries=[9]))
        reject('changed-external-content', [original])
        external.unlink()
        reject('missing-external-input', [original])
        write_json(manifest, dict(mandatoryExternalInputs=[dict(path='../outside.json', sha256='0' * 64)]))
        reject('escaped-external-input', [dict(original, sha256=sha256(manifest))])
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/mandatory-input-controls.json',
        dict(passed=True, sourceCredit=0, controls=controls, liveInputsAndSourcesChanged=False))
    print(dict(passed=True, controls=len(controls)))


if __name__ == '__main__':
    main()
