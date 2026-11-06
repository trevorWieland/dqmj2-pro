import json
from project import ROOT,sha256,configuration
from link_runtime_unit import measured_module
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM


def verify():
    path=ROOT/'evidence/verification/ov005-constructor505-pointer-consumption-20261101.json';proof=json.loads(path.read_text());meta,arm,unused=measured_module('main');overlayMeta,overlay,unused=measured_module('ov005')
    if proof['romSha256']!=configuration()['romSha256']or proof['verifierSha256']!=sha256(__file__):raise ValueError('505 verifier/build differs')
    import hashlib
    for row in proof['functions']:
        a=int(row['address'],0);body=arm[a-0x02000000:a-0x02000000+row['bytes']]
        if row['moduleSha256']!=meta['sha256']or hashlib.sha256(body).hexdigest()!=row['sha256']:raise ValueError('505 native body differs')
    expected={0x0204864C:('mov','r4, r1'),0x02048650:('ldrb','r3, [r4, #0x61]'),0x02048668:('ldr','r0, [r4, #0x10]'),0x02048678:('ldr','r2, [r4, #0x14]'),0x02035000:('str','r3, [r0, #0x28]'),0x02035004:('str','r2, [r0, #0x24]'),0x02048A5C:('bx','lr')};decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    for pc,view in expected.items():
        ins=next(decoder.disasm(arm[pc-0x02000000:pc-0x02000000+4],pc))
        if(ins.mnemonic,ins.op_str)!=view:raise ValueError(('505 opcode differs',hex(pc)))
    caller=proof['caller'];a=int(caller['address'],0);body=overlay[a-0x021D7240:a-0x021D7240+caller['bytes']]
    if caller['moduleSha256']!=overlayMeta['sha256']or hashlib.sha256(body).hexdigest()!=caller['sha256']:raise ValueError('505 caller differs')
    calls=[hex(i.address)for i in decoder.disasm(body,a)if i.mnemonic=='bl'and i.op_str=='#0x2048644']
    if calls!=[r['pc']for r in caller['qualifiedCallSites']]:raise ValueError('505 caller edges differ')
    return dict(staticCallSites=len(calls),sourceCredit=0,nativeExecutions=0)

if __name__=='__main__':print(json.dumps(verify()))
