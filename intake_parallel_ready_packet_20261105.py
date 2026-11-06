import argparse
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
from closed_c_compiler_inputs_20261105 import compiler_inputs as closed_inputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configuration')
    parser.add_argument('--ready', required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--packet-id', required=True)
    parser.add_argument('--owner', required=True)
    options = parser.parse_args()
    config_path = ROOT / options.configuration
    config = read_json(config_path)
    cohort = config['cohort']
    assert not config.get('membershipFrozen'), 'Packet membership is frozen'
    driver = ROOT / f'evidence/verification/cohort{cohort}-continuation-driver-v22-20261105.json'
    transaction = ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json'
    prepared = ROOT / f'work/integration/cohort{cohort}-recovery-transaction.json'
    assert not driver.exists() and not transaction.exists() and not prepared.exists(), 'Shared preparation already owns this cohort'
    ready_path = (ROOT / options.ready).resolve()
    assert ready_path.is_relative_to(ROOT.resolve()) and ready_path.name == 'ready.json'
    assert sha256(ready_path) == options.sha256
    ready = read_json(ready_path)
    assert ready['functions'] > 0 and ready['bytes'] > 0
    for packet in ready['packets']:
        for row in read_json(ROOT / packet['report'])['matches']:
            if row['processor'] == 'arm9' and row['module'] == 'main' and row['mode'] == 'thumb':
                closed_inputs(row)
    if options.ready in config['readyPackets']:
        assert config['packetIds'][options.ready] == options.packet_id
    else:
        assert options.packet_id not in config['packetIds'].values()
    board_path = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    board = read_json(board_path)
    owners = [row for row in board['active'] if row['id'] == options.owner]
    assert len(owners) == 1 and '/' + options.owner + '/' in options.ready
    original = config_path.read_bytes()
    if options.ready not in config['readyPackets']:
        config['readyPackets'].append(options.ready)
    config['packetIds'][options.ready] = options.packet_id
    helper = 'intake_parallel_ready_packet_20261105.py'
    if helper not in config['extra']:
        config['extra'].append(helper)
    write_json(config_path, config)
    try:
        subprocess.run([sys.executable, str(ROOT / 'prepare_parallel_packet_wave.py'),
            options.configuration], cwd=ROOT, check=True)
    except BaseException:
        config_path.write_bytes(original)
        raise
    rows = [(name, read_json(ROOT / name)) for name in config['readyPackets']]
    functions = sum(row['functions'] for name, row in rows)
    size = sum(row['bytes'] for name, row in rows)
    specification = read_json(ROOT / (config['name'] + '-specification.json'))
    assert len(specification['expectedAdditions']) == functions
    assert sum(row['bytes'] for row in specification['expectedAdditions']) == size
    for packet in ready['packets']:
        if packet['report'] not in owners[0]['handedOffReports']:
            owners[0]['handedOffReports'].append(packet['report'])
    board[f'pendingAggregate{cohort}'] = dict(functions=functions, bytes=size,
        membershipFrozen=False, sourceCredit=0)
    board['pendingSpecifications'][str(cohort)] = config['name'] + '-specification.json'
    if cohort not in board['pendingAcceptedCohorts']:
        board['pendingAcceptedCohorts'].append(cohort)
    pending = [board[f'pendingAggregate{number}'] for number in board['pendingAcceptedCohorts']]
    board['aggregatePendingFunctions'] = sum(row['functions'] for row in pending)
    board['aggregatePendingBytes'] = sum(row['bytes'] for row in pending)
    write_json(board_path, board)
    lines = [f'# Parallel source union {cohort} — 2026-11-05', '',
        f'Growing proposal: {functions} functions / {size:,} initialized bytes. '
        'Source credit remains zero until all original shared checks and committed source/input closure pass.', '',
        '| Frozen packet | Functions | Bytes |', '| --- | ---: | ---: |']
    document = ROOT / config['document']
    for name, row in rows:
        label = config['packetIds'][name]
        lines.append(f'| [{label}](../{name}) | {row["functions"]} | {row["bytes"]:,} |')
    lines += [f'| Total | {functions} | {size:,} |', '',
        'Each linked READY report records actual native/source returns or explicit entry stops, '
        'original bindings and CPU mode, independent models, wrong-C/layout controls and copied-root replay. '
        'Imported helpers, data symbols, linkage anchors, callback contracts and hardware providers '
        'receive zero additional source credit. Partial entry stops do not establish caller returns '
        'or hardware execution.', '',
        'The existing packet preparer retains every immutable pin, exact native extent, '
        'genuine link and physical ownership check. This metadata intake helper grants no acceptance '
        'and changes no source, compiler, oracle, registry or validation gate.', '']
    document.write_text('\n'.join(lines), encoding='utf-8')
    print(dict(cohort=cohort, functions=functions, bytes=size, sourceCredit=0,
        nextReplay='provenance/' + config['name'] + '-' + options.packet_id + '-0-replay.json'))


if __name__ == '__main__':
    main()
