import gzip
import hashlib
import json
import math
import random
import struct
import sys
from pathlib import Path
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module
import unicorn
from probe_main_float592_native_20261101 import Machine, dw

SIGNED_WIDEN = 0x020244C4
MULTIPLY = 0x02024540
TRUNCATE = 0x02024394


def clipped_integer(value):
    integral = math.trunc(value)
    return max(-2147483648, min(2147483647, integral))


def execute():
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    module, image, symbols = measured_module('main')
    assert module['sha256'] == 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    functions = []
    for address in [SIGNED_WIDEN, MULTIPLY, TRUNCATE]:
        line = next(line for line in symbols.splitlines() if f'addr:0x{address:08x}' in line.lower())
        functions.append(dict(address=hex(address), mode='arm', canonicalSymbolLine=line))
    values = {-2147483648, -2147483647, -1431655766, -1431655765, -65536, -32768,
        -257, -256, -1, 0, 1, 255, 256, 257, 32767, 65535, 65536,
        1431655764, 1431655765, 2147483646, 2147483647}
    for bit in range(31):
        for delta in [-1, 0, 1]:
            for sign in [-1, 1]:
                value = sign * ((1 << bit) + delta)
                if -2147483648 <= value <= 2147483647:
                    values.add(value)
    rng = random.Random(0x244C4243540)
    values.update(rng.randrange(-2147483648, 2147483648) for unused in range(256))
    values = sorted(values)
    chains, direct, negative, observed = [], [], [], set()
    for index, value in enumerate(values):
        machine = Machine(image, index)
        wide = machine.call(SIGNED_WIDEN, [value & 0xFFFFFFFF])[:2]
        assert wide == dw(float(value)), (value, wide)
        product = machine.call(MULTIPLY, wide + dw(1.5))[:2]
        expected_product = float(value) * 1.5
        assert product == dw(expected_product), (value, product)
        result = machine.call(TRUNCATE, product)[0]
        expected = clipped_integer(expected_product)
        assert result == expected & 0xFFFFFFFF, (value, result, expected)
        defined = -2147483648 <= math.trunc(expected_product) <= 2147483647
        chains.append(dict(inputSigned32=value, inputWord=value & 0xFFFFFFFF,
            expectedWideWords=wide, multiplierWords=dw(1.5), expectedProductWords=product,
            expectedSignedResult=expected, portableSignedCastDefined=defined, calls=machine.calls))
        observed.update(machine.seen)
    fractional_values = {-2147483649.0, -2147483648.5, -2147483648.0, -2147483647.5,
        -65535.5, -257.75, -1.5, -0.999999, -0.5, -0.0, 0.0, 0.5, 0.999999,
        1.5, 255.5, 257.75, 65535.5, 2147483646.5, 2147483647.0,
        2147483647.5, 2147483648.0, 2147483648.5}
    for index, value in enumerate(sorted(fractional_values)):
        machine = Machine(image, 10000 + index)
        expected = clipped_integer(value)
        result = machine.call(TRUNCATE, dw(value))[0]
        assert result == expected & 0xFFFFFFFF, (value, result, expected)
        direct.append(dict(inputWords=dw(value), expectedSignedResult=expected,
            portableSignedCastDefined=-2147483648 <= math.trunc(value) <= 2147483647,
            calls=machine.calls))
        observed.update(machine.seen)
    controls = chains[::7]
    if not any(case['inputSigned32'] == 0 for case in controls):
        controls.append(next(case for case in chains if case['inputSigned32'] == 0))
    for index, case in enumerate(controls):
        machine = Machine(image, 20000 + index)
        broken_words = [case['expectedProductWords'][0], 0]
        result = machine.call(TRUNCATE, broken_words)[0]
        negative.append(dict(inputSigned32=case['inputSigned32'], brokenWords=broken_words,
            result=result, properResult=case['expectedSignedResult'] & 0xFFFFFFFF,
            rejected=result != case['expectedSignedResult'] & 0xFFFFFFFF, calls=machine.calls))
        observed.update(machine.seen)
    rejected = sum(case['rejected'] for case in negative)
    assert rejected > 0 and rejected < len(negative)
    raw = json.dumps(dict(chains=chains, directConversions=direct, brokenHighWordControls=negative),
        sort_keys=True, separators=(',', ':')).encode()
    trace = ROOT / 'evidence/generated/main-signed-double-chain601-native-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main',
        moduleSha256=module['sha256'], mode='arm', sourceCredit=0, providedCalls=0,
        functions=functions, signedInputVectors=len(chains), directFractionalVectors=len(direct),
        actualProperTopReturns=3 * len(chains) + len(direct), actualControlTopReturns=len(negative),
        independentBrokenHighWordRejections=rejected, unchangedControlPositives=len(negative) - rejected,
        nestedHelperReturnsNotCounted=True, nonstackWrites=0,
        physicalContracts=[dict(entry=hex(SIGNED_WIDEN), input='R0 signed32', output='Binary64 R0-low/R1-high',
            domain='Listed signed32 vectors including both extrema, power boundaries and deterministic samples'),
            dict(entry=hex(MULTIPLY), input='Binary64 R0-low/R1-high and R2-low/R3-high',
                output='Binary64 R0-low/R1-high', domain='Listed exact signed32 conversions multiplied by1.5'),
            dict(entry=hex(TRUNCATE), input='Binary64 R0-low/R1-high', output='Signed32 word in R0',
                domain='Listed finite values; truncation toward zero within range, native saturation outside range')],
        definedCastChains=sum(case['portableSignedCastDefined'] for case in chains),
        nativeOnlyOverflowChains=sum(not case['portableSignedCastDefined'] for case in chains),
        observedInstructionAddresses=sorted(observed),
        independentModel='IEEE binary64 signed32 conversion and exact multiply1.5, then mathematical truncation with native signed32 clipping',
        isolatedState='Fresh machine per chain; fresh poisoned registers and cleared guarded stack per call; callee saves and actual return required',
        trace=dict(path=trace.relative_to(ROOT).as_posix(), sha256=sha256(trace), decodedSha256=hashlib.sha256(raw).hexdigest()),
        dependencies=[dict(path='probe_main_float592_native_20261101.py', sha256=sha256(ROOT / 'probe_main_float592_native_20261101.py'))],
        limitations=['Native helper contracts only; no reconstructed source, source match or historical public prototype is claimed',
            'Multiplication is qualified here only for signed32-derived operands times1.5; arbitrary binary64 arithmetic is not generalized',
            'Out-of-range native conversion behavior is not a portable C signed cast and receives no defined-C-domain credit',
            'NaNs, infinities, signaling behavior, exception modes and negative-zero sign preservation are not covered',
            'The synthetic helper chain does not execute main02067E54 or establish its ordinary caller inputs or state reachability'])
    write_json(ROOT / 'evidence/abi/main-signed-double-chain601-20261101.json', report)
    print(dict(signedVectors=len(chains), directFractionalVectors=len(direct),
        properReturns=report['actualProperTopReturns'], controlReturns=len(negative),
        highWordRejections=rejected, nativeOnlyOverflowChains=report['nativeOnlyOverflowChains'], sourceCredit=0))


if __name__ == '__main__':
    execute()
