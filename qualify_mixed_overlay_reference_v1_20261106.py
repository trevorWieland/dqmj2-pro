import argparse
import copy
import subprocess
import sys
import uuid
from pathlib import Path
from project import ROOT, read_json, sha256, write_json
from host_arm9_overlay_reference_policy_v1_20261106 import load_contract, scope_snapshot, ensure_scope, CONTRACT, LEDGER
from host_arm9_overlay_reference_v1_20261106 import qualify, require


def partition(specification, contract):
    selected = {item['report'] for item in contract['consumers']}
    require(len(selected) == 14 and all(sum(packet['report'] == name for packet in specification['packets']) == 1 for name in selected), 'Frozen174 selected overlay membership differs')
    residual = copy.deepcopy(specification)
    residual['packets'] = [packet for packet in residual['packets'] if packet['report'] not in selected]
    require(len(residual['packets']) + len(selected) == len(specification['packets']), 'Packet partition changed full frozen membership')
    return residual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--register', action='store_true')
    options = parser.parse_args()
    contract = load_contract()
    require(options.specification == contract['specification']['path'] and sha256(ROOT / options.specification) == contract['specification']['sha256'], 'Only the exact frozen174 full specification is qualified')
    specification = read_json(ROOT / options.specification)
    residual = partition(specification, contract)
    directory = ROOT / 'work/integration/host-arm9-overlay-reference-v1' / ('admission-' + uuid.uuid4().hex[:12])
    proof = qualify(contract, directory, committed=False)
    subset = directory / 'unchanged-residual-specification.json'
    write_json(subset, residual)
    command = [sys.executable, str(ROOT / 'qualify_mixed_arm9_reference_context_v5_20261106.py'), subset.relative_to(ROOT).as_posix()]
    if options.register:
        command.append('--register')
    subprocess.run(command, cwd=ROOT, check=True)
    post = scope_snapshot(contract, directory / 'post-legacy-main-appends', committed=False)
    ensure_scope(post)
    legacy = f'evidence/verification/cohort{specification["cohort"]}-mixed-reference-inputs-20261105.json'
    require(read_json(ROOT / legacy)['passed'] is True, 'Unchanged residual legacy qualifier failed')
    output = ROOT / f'evidence/verification/cohort{specification["cohort"]}-namespaced-overlay-reference-v1-20261106.json'
    write_json(output, dict(passed=True, sourceCredit=0, registered=options.register,
        fullSpecification=options.specification, fullSpecificationSha256=sha256(ROOT / options.specification),
        fullPacketCount=len(specification['packets']), independentlyQualifiedOverlayPackets=14,
        legacyResidualPackets=len(residual['packets']), originalFrozenMembershipPreserved=True,
        qualification=proof, postLegacyMutableRoleAudit=post,
        legacyResidualSpecification=dict(path=subset.relative_to(ROOT).as_posix(), sha256=sha256(subset)),
        legacyQualification=dict(path=legacy, sha256=sha256(ROOT / legacy)), legacyCommand=command,
        contract=dict(path=CONTRACT, sha256=sha256(ROOT / CONTRACT)), separateOverlayLedger=dict(path=LEDGER, sha256=sha256(ROOT / LEDGER)),
        legacyMainAssertionsAndOriginal26ConsumersPreserved=True, generator=Path(__file__).name, generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
