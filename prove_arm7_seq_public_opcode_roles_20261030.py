import hashlib
import json
from pathlib import Path
import arm7_runtime
import arm7_seq_public_opcode_roles_20261030 as roles
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
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('Invalid opcode role accepted: ' + name)
    reject('wrong-module', lambda: roles.qualify(layout, 'arm7-main', roles.PC, roles.WORD))
    reject('different-word', lambda: roles.qualify(layout, 'arm7-wram', roles.PC, roles.WORD ^ 1))
    reject('neighboring-pc', lambda: roles.qualify(layout, 'arm7-wram', roles.PC + 4, roles.WORD))
    reject('wrong-independent-mask', lambda: roles.isolated.execute(roles.PC, roles.WORD, 0x04000000, 4, 0))
    module = next(row for row in layout['modules'] if row['id'] == 'arm7-wram')
    base = int(module['base'], 0)
    raw = bytearray((ROOT / module['binary']).read_bytes())
    raw[roles.PC - base:roles.PC - base + 4] = (0xE1A00000).to_bytes(4, 'little')
    reject('omitted-original-conditional-or', lambda: roles.segment(bytes(raw), base, 2, 0, 0))
    destination = ROOT / 'evidence/verification/arm7-seq-public-opcode-word-role-20261030.json'
    report = {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'proof': proof, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'functionAndSourceCredit': 0, 'originalBytesChanged': False}
    write_json(destination, report)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'isolatedBoundaryStops': len(proof['probe']['records']),
        'originalSegmentBoundaryStops': proof['originalEnclosingSegment']['actualBoundaryStops'], 'allPassed': report['allPassed']}))


if __name__ == '__main__':
    main()
