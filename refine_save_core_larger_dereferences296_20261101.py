import concurrent.futures
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from link_runtime_unit import measured_module
import census_compile_save_core_near140_20261101 as C

SPECS = {
    0x0206E73C: [(0x0206E778, 'ldr', 'r7, [r4]')],
    0x020743F8: [(0x02074508, 'ldr', 'r0, [r1, r2, lsl #2]'), (0x02074538, 'ldrh', 'r7, [r1, r3]')],
    0x02080C04: [(0x02080DA4, 'ldr', 'r0, [fp, #4]'), (0x02080DAC, 'ldrb', 'r3, [r0, r7]'),
        (0x02080EEC, 'ldrb', 'r2, [r2, r1]'), (0x02081078, 'ldrb', 'r1, [r1, r0]')],
    0x02046AF4: [(0x02046B44, 'ldrb', 'r0, [r6, sb]')],
    0x02070FD8: [],
    0x0208870C: [(0x02088858, 'ldrb', 'r3, [sl]')],
    0x020BFC04: [(0x020BFC3C, 'ldr', 'r2, [r4, #8]'), (0x020BFC40, 'ldr', 'sb, [r2, sl, lsl #3]')],
    0x020C06E8: [(0x020C075C, 'ldr', 'r0, [sl, r4, lsl #4]'), (0x020C0864, 'ldr', 'r0, [sl, r7, lsl #4]')],
    0x020C0A8C: [(0x020C0C50, 'ldr', 'r0, [sb, r0, lsl #4]'), (0x020C0E3C, 'ldr', 'r0, [sb, r2, lsl #4]')]
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def patch(address, text):
    edits = []

    def change(before, after):
        nonlocal text
        count = text.count(before)
        assert count, (hex(address), before)
        text = text.replace(before, after)
        edits.append(dict(before=before, after=after, count=count))

    if address == 0x0206E73C:
        change('temp_r7 = *temp_r4_2;', 'temp_r7 = M2C_FIELD(temp_r4_2, void **, 0);')
    elif address == 0x020743F8:
        change('*(native_data_021c5df8 + (M2C_FIELD(native_data_021c5a30, s32 *, 0) * 4))',
            'M2C_FIELD(native_data_021c5df8, u32 *, M2C_FIELD(native_data_021c5a30, s32 *, 0) * 4)')
        change('*temp_r4 = (u16) *(native_data_020dbc18 + ((native_fn_02066a6c((u32) M2C_FIELD((void *) native_fn_02065d88((u32) temp_r9), u8 *, 0x24)) + 0x17B) * 2));',
            'M2C_FIELD(temp_r4, u16 *, 0) = M2C_FIELD(native_data_020dbc18, u16 *, (native_fn_02066a6c((u32) M2C_FIELD((void *) native_fn_02065d88((u32) temp_r9), u8 *, 0x24)) + 0x17B) * 2);')
    elif address == 0x02080C04:
        change('*(native_data_020de580.field_4 + ', '*((u8 *)native_data_020de580.field_4 + ')
    elif address == 0x02046AF4:
        change('*(arg1 + var_r9)', 'M2C_FIELD(arg1, u8 *, var_r9)')
        change('*var_r10', 'M2C_FIELD(var_r10, u8 *, 0)')
        pattern = '*(native_data_020fae64 + (M2C_FIELD(native_data_020fb264, u16 *, 0x80) * 2))'
        change(pattern, 'M2C_FIELD(native_data_020fae64, u16 *, M2C_FIELD(native_data_020fb264, u16 *, 0x80) * 2)')
    elif address == 0x02070FD8:
        change('*(temp_r7 + var_r5)', 'M2C_FIELD(temp_r7, u8 *, var_r5)')
    elif address == 0x0208870C:
        change('*temp_r10_2', 'M2C_FIELD(temp_r10_2, u8 *, 0)')
        change('*temp_r10_3', 'M2C_FIELD(temp_r10_3, u8 *, 0)')
    elif address == 0x020BFC04:
        change('*(M2C_FIELD(native_data_021d4bec, s32 *, 8) + (var_r10 * 8))',
            'M2C_FIELD(M2C_FIELD(native_data_021d4bec, u32 *, 8), u32 *, var_r10 * 8)')
    elif address == 0x020C06E8:
        for index in ('var_r4', 'var_r7_2'):
            change('*(arg1 + (' + index + ' * 0x10))', 'M2C_FIELD(arg1, u32 *, ' + index + ' * 0x10)')
    elif address == 0x020C0A8C:
        change('*(arg1 + (M2C_FIELD(arg0, s8 *, 5) * 0x10))',
            'M2C_FIELD(arg1, u32 *, M2C_FIELD(arg0, s8 *, 5) * 0x10)')
    assert len(text.splitlines()) <= 500 and not re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b', text)
    return text, edits


def prepare():
    C.SNAPSHOT = 'evidence/verification/accepted-cohort124-identities-v2-20261101.json'
    ranges, receipts = C.exclusions()
    metadata, binary, config = measured_module('main')
    origin_manifest = json.loads((ROOT / 'evidence/lanes/save-core/application-drafts285-ready-20261101.json').read_text())
    hashes = {row['path']: row['sha256'] for row in origin_manifest['files']}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    jobs, skipped = [], []
    for address, assertions in SPECS.items():
        found = re.search(r'^(\S+) kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + '$', config, re.M)
        assert found
        alias, length = found[1], int(found[2], 0)
        if any(address < end and start < address + length for start, end in ranges):
            skipped.append(dict(address=hex(address), bytes=length, reason='Accepted/pending interval overlap'))
            continue
        native = binary[address - 0x02000000:address - 0x02000000 + length]
        instructions = {i.address: i for i in decoder.disasm(native, address)}
        access = []
        for pc, mnemonic, operands in assertions:
            actual = instructions[pc]
            assert (actual.mnemonic, actual.op_str) == (mnemonic, operands), (hex(pc), actual.mnemonic, actual.op_str)
            access.append(dict(pc=hex(pc), mnemonic=mnemonic, operands=operands, bytes=actual.bytes.hex()))
        if address == 0x02070FD8:
            matches = [i for i in instructions.values() if i.mnemonic == 'ldrb' and i.op_str == 'r0, [r7, r5]']
            assert len(matches) == 1
            access.append(dict(pc=hex(matches[0].address), mnemonic=matches[0].mnemonic, operands=matches[0].op_str, bytes=matches[0].bytes.hex()))
        if address == 0x02046AF4:
            matches = [i for i in instructions.values() if i.mnemonic == 'ldrb' and i.op_str == 'r0, [sl]']
            assert matches
            access += [dict(pc=hex(i.address), mnemonic=i.mnemonic, operands=i.op_str, bytes=i.bytes.hex()) for i in matches]
            assert any(i.mnemonic == 'strh' for i in instructions.values())
        origins = list(ROOT.glob(f'nonmatching/save-core/20261101-app-large27*/native_main_{address:08x}.c'))
        assert len(origins) == 1
        origin = origins[0]
        relative = origin.relative_to(ROOT).as_posix()
        assert sha(origin.read_bytes()) == hashes[relative]
        text, edits = patch(address, origin.read_text())
        path = ROOT / f'nonmatching/save-core/20261101-larger-dereferences296/native_main_{address:08x}.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_text() == text
        else:
            path.write_text(text)
        jobs.append(dict(module='main', processor='arm9', program='', mode='arm', address=hex(address), bytes=length,
            alias=alias, nativeModuleSha256=metadata['sha256'], nativeSpanSha256=sha(native),
            source=path.relative_to(ROOT).as_posix(), sourceSha256=sha(path.read_bytes()),
            originDraft=relative, sourceOriginSha256=sha(origin.read_bytes()), reusedDraft=True, newAddressNamedDraftAttempt=False,
            work=f'work/save-core/larger-dereferences296/{address:08x}', edits=edits, measuredAccesses=access,
            interfaceClosurePending=True, sourceCredit=0))
    return jobs, skipped, receipts


def run(job):
    folder = ROOT / job['work']
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / 'job.json'
    path.write_text(json.dumps(job, indent=2) + '\n')
    producer = ROOT / 'evidence/application/save_core_larger_dereferences296_worker_20261101.py'
    result = subprocess.run([sys.executable, str(producer), str(path)], cwd=ROOT, capture_output=True,
        text=True, timeout=300, creationflags=subprocess.CREATE_NO_WINDOW)
    (folder / 'stdout.txt').write_text(result.stdout)
    (folder / 'stderr.txt').write_text(result.stderr)
    assert result.returncode == 0, result.stderr
    return json.loads((folder / 'result.json').read_text())


def main():
    jobs, skipped, receipts = prepare()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(run, jobs))
    raw = (json.dumps(rows, sort_keys=True, separators=(',', ':')) + '\n').encode()
    sidecar = ROOT / 'evidence/vectors/save-core-larger-dereferences296-20261101.json.gz'
    sidecar.write_bytes(gzip.compress(raw, mtime=0))
    counts = dict(refinedHypotheses=len(rows), draftedNativeBytes=sum(row['bytes'] for row in rows),
        compilable=sum(row.get('compilable', False) for row in rows), genuineLinkedProfiles=sum(sum(a.get('realLinkSucceeded', False) for a in row.get('compileAttempts', [])) for row in rows),
        near=sum(row.get('nearCandidate', False) for row in rows), exact=sum(row.get('byteExactCandidate', False) for row in rows), nativeSemanticallyQualified=0, acceptedSourceBytes=0)
    result = dict(schema=1, counts=counts, exclusions=receipts, skipped=skipped, compilerWorkers=2,
        fullProvenanceSidecar=dict(path=sidecar.relative_to(ROOT).as_posix(), sha256=sha(sidecar.read_bytes()), contentSha256=sha(raw)),
        generatorSha256=sha(Path(__file__).read_bytes()), sourceCredit=0,
        limits=['Nine prior failed larger drafts receive explicit pointer-value dereferences and measured load/store width corrections, preserving the original byte-address arithmetic.',
            'The original selected C declarations, escaped stack extents, call arities and return APIs have not received complete compatibility or semantic proof. This pass is compile/link hypothesis research with zero source acceptance.',
            'Native read-site bytes are checked before drafting. They prove physical accesses, not original field declarations, aggregate extents, alias independence or ordinary scene reachability.',
            'Two isolated compiler subprocesses use the prior base and speed profiles; originals and all accepted sources remain unchanged.'])
    target = ROOT / 'evidence/lanes/save-core/larger-dereferences296-20261101.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
