import gzip
import json
import struct
import sys
import match_runtime as c
import unicorn
import probe_main_float592_native_20261101 as Q
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module
SIGNED_FLOAT, ADD, SIGNED_TRUNCATE = 0x02025A28, 0x02024E0C, 0x020259B4


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('630 runtime differs')
    info, arm, symbols = measured_module('main')
    if info['sha256'] != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise ValueError('630 main input differs')
    integer_values = set(range(-20, 21))
    integer_values.update([-2147483648, 2147483647, -65537, -65536, -32768, 32767, 65535, 65536])
    for value in [1 << 23, 1 << 24, 1 << 25, 1 << 30]:
        for delta in [-1, 0, 1]:
            integer_values.update([value + delta, -value + delta])
    cases, seen = [], set()
    for value in sorted(integer_values):
        machine = Q.Machine(arm, len(cases))
        returned = machine.call(SIGNED_FLOAT, [value & 0xFFFFFFFF])
        expected = word(float(value))
        if returned[0] != expected:
            raise ValueError(('630 native signed32-to-binary32 differs', value))
        cases.append(dict(kind='signed-to-float', inputSigned32=value, expectedReturnedWord=expected, actualCalls=machine.calls))
        seen.update(machine.seen)
    pairs = [(90.0, float(draw)) for draw in range(20)]
    pairs += [(1.0, f32(f32(0.012) * float(value))) for value in [0, 1, 2, 39, 40, 100, 140, 1000]]
    pairs += [(f32(value), f32(delta)) for value in [0, 1, 9999, 32767] for delta in [-1.25, 0.0, 0.65, 1.15, 1.25, 128.0]]
    for left, right in pairs:
        machine = Q.Machine(arm, len(cases))
        returned = machine.call(ADD, [word(left), word(right)])
        expected = word(f32(left + right))
        if returned[0] != expected:
            raise ValueError(('630 native binary32 addition differs', left, right))
        cases.append(dict(kind='float-add', inputValues=[left, right], expectedReturnedWord=expected, actualCalls=machine.calls))
        seen.update(machine.seen)
    values = [-2147483648.0, -32768.75, -100.25, -1.75, -0.0, 0.0, 0.012, 0.65, 1.15, 1.25, 1.75, 99.75, 9999.75, 32767.5, 2147483520.0]
    for value in values:
        value = f32(value)
        machine = Q.Machine(arm, len(cases))
        returned = machine.call(SIGNED_TRUNCATE, [word(value)])
        expected = int(value) & 0xFFFFFFFF
        if returned[0] != expected:
            raise ValueError(('630 native finite signed truncation differs', value))
        cases.append(dict(kind='float-to-signed', inputValue=value, expectedReturnedWord=expected, actualCalls=machine.calls))
        seen.update(machine.seen)
    raw = encoded(dict(cases=cases))
    artifact = ROOT / 'evidence/generated/main-float630-growth-native-traces-20261101.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    functions = []
    for entry in [SIGNED_FLOAT, ADD, SIGNED_TRUNCATE]:
        line = next(line for line in symbols.splitlines() if 'addr:0x%08x' % entry in line.lower())
        functions.append(dict(address=hex(entry), canonicalSymbolLine=line))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='main', moduleSha256=info['sha256'], mode='arm', sourceCredit=0, providedCalls=0, actualTopReturns=len(cases), nestedReturnsNotCounted=True, nonstackWrites=0, publicOriginalFormalTypesProven=False, functions=functions, emulationModel='UC_CPU_ARM_946', contracts=[dict(entry=hex(SIGNED_FLOAT), input='R0 signed32', result='IEEE binary32 in R0', qualifiedDomain='Listed integer, rounding and signed-boundary cases'), dict(entry=hex(ADD), input='R0 and R1 IEEE binary32', result='IEEE binary32 in R0', qualifiedDomain='Listed finite positive/negative sums, including90+draw and1+modifier products'), dict(entry=hex(SIGNED_TRUNCATE), input='R0 IEEE binary32', result='Signed32 truncation toward zero in R0; other caller-saved words remain scratch', qualifiedDomain='Listed finite in-range positive/negative inputs')], cases=[dict(kind=case['kind'], actualTopReturns=1, traceSha256=c.sha(encoded(case))) for case in cases], observedAddresses=sorted(seen), generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=c.sha(raw)), limits=['Original-native finite physical contracts only; no source matching or global catalogue edits.', 'Each call resets stack/registers and must actually return; nonstack writes and PCs outside measured initialized main are rejected.', 'No NaN/Inf/subnormal/general overflow semantics or original public types are inferred.', 'This does not execute or qualify the larger D240 caller or its unresolved inherited-R8/SP+4 paths.'])
    write_json(ROOT / 'evidence/abi/main-float630-growth-word-contracts-20261101.json', report)
    print(dict(actualTopReturns=len(cases), providers=0, sourceCredit=0), flush=True)


if __name__ == '__main__':
    execute()
