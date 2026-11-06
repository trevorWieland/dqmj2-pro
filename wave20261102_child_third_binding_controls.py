import copy
import utility_code
import utility_runtime
from wave20261102_child_third_link import qualify
from wave20261102_child_third_prepare import ROOT, LANE
from project import write_json, sha256


def main():
    spec = next(s for s in utility_code.candidates() if s['module'] == 'utility-child-arm9-main' and s['address'] == 0x0200bbc8)
    call = next(i for i in spec['instructions'] if i.mnemonic == 'bl' and i.operands[0].imm == 0x0200ba04)
    body = (ROOT / spec['binary']).read_bytes()[spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']]
    entry = dict(program=utility_runtime.PROGRAM, processor='arm9', module=spec['module'], mode='thumb',
        address=hex(spec['address']), bytes=spec['bytes'], targetSha256=utility_runtime.sha(body),
        relocations=[dict(symbol='native_utility_child_arm9_thumb_0200ba04', target='0x0200ba04',
            targetMode='thumb', type=10, offset=call.address - spec['address'], addend=0)])
    unused, qualified = qualify(entry)
    if len(qualified) != 1 or qualified[0]['calleeFunctionCredit'] != 0 or qualified[0]['calleeSourceBytes'] != 0:
        raise ValueError('Positive native-entry qualification failed')
    outcomes = []
    for kind in ['wrong-mode', 'wrong-target', 'wrong-program', 'wrong-cpu', 'wrong-span-hash']:
        altered = copy.deepcopy(entry)
        if kind == 'wrong-mode':
            altered['relocations'][0]['targetMode'] = 'arm'
        elif kind == 'wrong-target':
            altered['relocations'][0]['target'] = '0x0200ba06'
        elif kind == 'wrong-program':
            altered['program'] = 'host'
        elif kind == 'wrong-cpu':
            altered['processor'] = 'arm7'
        else:
            altered['targetSha256'] = '0' * 64
        try:
            qualify(altered)
        except ValueError as error:
            outcomes.append(dict(control=kind, rejected=True, reason=str(error)))
        else:
            raise ValueError('Native-entry negative control unexpectedly passed: ' + kind)
    write_json(LANE / 'native-callee-binding-controls.json', dict(generator=__file__, generatorSha256=sha256(__file__),
        positiveQualification=qualified, negativeControls=outcomes, originalCaller=entry,
        sourceCredit=0, functionCredit=0, callerReconstructionCredit=0, calleeReconstructionCredit=0,
        sourceRelocationProved=False, zeroCodeAnchorLinkPerformed=False,
        limitations=['This validates native target-entry evidence only; actual C object relocations and genuine linking remain separate mandatory gates']))
    print(dict(qualifiedEntries=len(qualified), rejectedControls=len(outcomes), sourceCredit=0))


if __name__ == '__main__':
    main()
