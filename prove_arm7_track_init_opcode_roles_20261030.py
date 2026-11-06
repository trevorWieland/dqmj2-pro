import hashlib
import json
from pathlib import Path
import arm7_runtime
import arm7_track_init_opcode_roles_20261030 as roles
from project import write_json

ROOT = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    proof = roles.evidence(layout)
    controls = []
    def reject(name, operation):
        try:
            operation()
        except Exception as error:
            controls.append({'name': name, 'rejected': True, 'exception': type(error).__name__, 'reason': str(error)})
        else:
            raise ValueError('Opcode-role rejection control failed: ' + name)
    reject('wrong-module-same-value', lambda: roles.qualify(layout, 'arm7-wram', 0x027E68EC, 0x03800902))
    reject('unqualified-data-position-same-value', lambda: roles.qualify(layout, 'arm7-main', 0x027E68F0, 0x03800902))
    reject('wrong-raw-code-word', lambda: roles.qualify(layout, 'arm7-main', 0x027E68EC, 0x03800903))
    reject('independent-orr-model-rejects-wrong-mask', lambda: roles.previous_roles.execute(0x027E68EC, 0x03800903, 0x8000, 4, 0))
    raw = bytearray((ROOT / 'extract/arm7/runtime/arm7-main.bin').read_bytes())
    raw[0x68EC:0x68F0] = (0x03800903).to_bytes(4, 'little')
    reject('original-bounded-segment-model-rejects-wrong-operation', lambda: roles.segment(bytes(raw), 0x027E0000, 1, 0, 0))
    result = {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'proof': proof, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'actualInstructionBoundaryStops': proof['actualInstructionBoundaryStops'],
        'actualOriginalSegmentBoundaryStops': proof['originalSegment']['actualBoundaryStops'],
        'functionReturnCredit': 0, 'sourceOrAssemblyCredit': 0,
        'limitation': 'One specific configured executable word only; no blanket opcode/pointer exclusion or computed dual-use-data absence'}
    destination = ROOT / 'evidence/verification/arm7-track-init-opcode-word-role-20261030.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed'], 'functionReturnCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
