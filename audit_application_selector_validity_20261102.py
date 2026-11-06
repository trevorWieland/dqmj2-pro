import hashlib
from pathlib import Path
import match_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, image, _ = measured_module('ov001')
    base = int(metadata['base'], 0)
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    entries = [(0x021FBE70, 24), (0x021FBD6C, 260), (0x022095F4, 400)]
    functions = []
    for address, size in entries:
        body = image[address - base:address - base + size]
        instructions = list(decoder.disasm(body, address))
        calls = []
        for index, ins in enumerate(instructions):
            if ins.mnemonic != 'bl' or not ins.operands or ins.operands[0].type != 2: continue
            if ins.operands[0].imm not in [0x021FBE70, 0x021FB960]: continue
            calls.append(dict(instruction=hex(ins.address), destination=hex(ins.operands[0].imm),
                surrounding=[dict(address=hex(q.address), mnemonic=q.mnemonic, operands=q.op_str)
                    for q in instructions[max(0, index - 1):index + 5]]))
        functions.append(dict(module='ov001', processor='arm9', mode='arm', address=hex(address), bytes=size,
            inputSpanSha256=hashlib.sha256(body).hexdigest(), directRelevantCalls=calls,
            instructions=[dict(address=hex(q.address), mnemonic=q.mnemonic, operands=q.op_str)
                for q in instructions] if size == 24 else None))
    assert len(functions[2]['directRelevantCalls']) == 8
    assert len(functions[1]['directRelevantCalls']) == 1
    assert functions[1]['directRelevantCalls'][0]['instruction'] == '0x21fbe44'
    write_json(ROOT / 'evidence/abi/application-selector-validity-static-audit-20261102.json',
        dict(sourceCredit=0, evidenceClass='Static original-byte/callsite audit; not native scene execution',
            generator=Path(__file__).name, generatorSha256=sha256(__file__), romSha256=config['romSha256'],
            inputModuleSha256=metadata['sha256'], functions=functions,
            globalGetterValidityByte='ov0010x02239abc+0x67', selectorDispatchByte='ov0010x02239a14+0x0a',
            sceneReachability=False, persistentSaveOffsetEstablished=False, rngSceneStateEstablished=False))
    print(dict(module='ov001', completedCommitCallsGetter=8, rawCase14Callsite='0x021fbe44', sourceCredit=0))


if __name__ == '__main__':
    main()
