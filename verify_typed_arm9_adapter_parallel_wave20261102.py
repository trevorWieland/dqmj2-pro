import copy
from pathlib import Path
import struct
import sys
import time
sys.dont_write_bytecode = True
import replay_parallel_packet_typed_arm9 as adapter
from project import ROOT, read_json, sha256, write_json


def main():
    source = ROOT / 'replay_parallel_packet_typed_arm9.py'
    pinned = '3b82ff1e3d48709ceb4413457ca3fc0621245271964da3d7789268745a0fb0e8'
    assert sha256(source) == pinned
    canonical = ROOT / 'evidence/matches/cohort149-parallel-wave20261102-next-ov006-0.json'
    original_hash = sha256(canonical)
    original = read_json(canonical)
    saved = copy.deepcopy(original)
    descriptor = 'provenance/cohort149-parallel-wave20261102-next-ov006-0-replay.json'
    positive = adapter.adapt(original, descriptor)
    assert original == saved and sha256(canonical) == original_hash
    for earlier, later in zip(original['matches'], positive['matches']):
        assert adapter.row_contract(earlier) == adapter.row_contract(later)
        assert {k: v for k, v in earlier.items() if k != 'nativeSymbolEntries'} == {k: v for k, v in later.items() if k != 'nativeSymbolEntries'}
    index = next(index for index, row in enumerate(original['matches']) if int(row['address'], 0) == 0x021eddf4)
    probe_index = next(index for index, probe in enumerate(original['matches'][index]['realLink']['bindingOnlyProbes']) if probe['mode'] == 'arm')
    work = ROOT / 'work/typed-arm9-adapter-audit-parallel-wave20261102' / str(time.time_ns())
    work.mkdir(parents=True)
    rejected = []

    def run_case(label, mutate):
        changed = copy.deepcopy(original)
        mutate(changed, changed['matches'][index])
        try:
            adapter.adapt(changed, descriptor)
        except (ValueError, OSError) as error:
            rejected.append(dict(name=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('Typed adapter accepted ' + label)

    for field, value in [('processor', 'arm7'), ('program', 'other-program'), ('module', 'ov000'), ('mode', 'thumb'), ('address', '0x2008be4'), ('kind', 'data')]:
        run_case('probe-' + field, lambda changed, row, field=field, value=value: row['realLink']['bindingOnlyProbes'][probe_index].update({field: value}))
    run_case('missing-probe', lambda changed, row: row['realLink']['bindingOnlyProbes'].pop(probe_index))
    run_case('duplicate-probe', lambda changed, row: row['realLink']['bindingOnlyProbes'].append(copy.deepcopy(row['realLink']['bindingOnlyProbes'][probe_index])))
    run_case('claimed-initialized-callee-code', lambda changed, row: row['realLink']['bindingOnlyProbes'][probe_index].update(initializedCodeBytes=4))
    run_case('different-source-object-proof', lambda changed, row: row['realLink'].update(sourceObjectSha256='0' * 64))
    run_case('wrong-caller-program', lambda changed, row: row.update(program='other-program'))
    run_case('wrong-report-program', lambda changed, row: changed.update(program='other-program'))
    run_case('missing-freshness-marker', lambda changed, row: changed.update(canonicalReportRefreshedFromFreshWorkerObjects=False))

    def conflict(changed, row):
        row['nativeSymbolEntries'] = copy.deepcopy(adapter.qualified_bindings(row))
        name = next(name for name, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function')
        row['nativeSymbolEntries'][name]['mode'] = 'thumb'

    run_case('existing-conflicting-typed-interface', conflict)
    probe = original['matches'][index]['realLink']['bindingOnlyProbes'][probe_index]
    anchor = ROOT / probe['object']
    raw = bytearray(anchor.read_bytes())
    with anchor.open('rb') as stream:
        elf = adapter.ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == probe['name'])
        table, stride, section = elf['e_shoff'], elf['e_shentsize'], symbol['st_shndx']
    struct.pack_into('<I', raw, table + stride * section + 4, 1)
    initialized = work / 'initialized-anchor.o'
    initialized.write_bytes(raw)
    wrong_marker = work / 'wrong-marker-anchor.o'
    raw = anchor.read_bytes()
    assert raw.count(b'$a\x00') == 1
    wrong_marker.write_bytes(raw.replace(b'$a\x00', b'$t\x00'))
    for label, path in [('actual-initialized-ELF-section', initialized), ('actual-wrong-ELF-mapping-symbol', wrong_marker)]:
        run_case(label, lambda changed, row, path=path: row['realLink']['bindingOnlyProbes'][probe_index].update(object=path.relative_to(ROOT).as_posix(), objectSha256=sha256(path)))
    assert len(rejected) == 16 and sha256(canonical) == original_hash and sha256(source) == pinned
    result = dict(passed=True, readOnly=True, sourceCredit=0, typedAdapterSha256=pinned,
        originalCanonicalSha256=original_hash, originalCanonicalUnchanged=True,
        originalInputObjectUnchanged=True, originalSourceObjectRelocationAndEveryOtherRowFieldPreserved=True,
        positiveRows=len(positive['matches']), positiveTypedFunctionBindings=sum(row['functionBindings'] for row in positive['typedArm9MetadataAdapter']['verifiedRows']),
        rejectedControls=rejected, privateELFMutationsOnly=str(work.relative_to(ROOT)),
        realLinkerOrCompilerInvocations=0, registryMutations=0, fullFreshReplayProven=False,
        generatorSha256=sha256(Path(__file__)))
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/typed-arm9-adapter-independent-audit.json', result)
    print(dict(passed=True, positiveRows=result['positiveRows'], rejectedControls=len(rejected), canonicalUnchanged=True, sourceCredit=0))


if __name__ == '__main__':
    main()
