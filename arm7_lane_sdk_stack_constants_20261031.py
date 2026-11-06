import copy
from pathlib import Path
from project import ROOT,sha256,write_json

MODULE_SHA='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
TARGET_SHA='c3882aec6f9cdfe285e95c9f44f2dad9acbbb95080b053be5adf6e55d740c5f1'
IDENTITY=('', 'arm7','arm7-wram','arm','0x37fbf64',240)
ROLES={'SDK_SYS_STACKSIZE':dict(offset=0xCC,storage='0x037fc030',load='0x037fbfa0',uses=['0x037fbfb4','0x037fbfc8']),
    'SDK_IRQ_STACKSIZE':dict(offset=0xD8,storage='0x037fc03c',load='0x037fbfcc',uses=['0x037fbfd8'])}


def qualify(entry,relocation,target,native):
    identity=tuple(entry.get(key,'') for key in ('program','processor','module','mode','address','bytes'))
    if identity!=IDENTITY or entry.get('inputModuleSha256')!=MODULE_SHA or entry.get('targetSha256')!=TARGET_SHA:
        raise ValueError('Absolute SDK integer symbol lacks its exact qualified caller')
    if __import__('hashlib').sha256(native).hexdigest()!=TARGET_SHA:
        raise ValueError('Absolute SDK integer role original body differs')
    module=ROOT/'extract/arm7/runtime/arm7-wram.bin'
    if sha256(module)!=MODULE_SHA or sha256(ROOT/'link_arm7_bulk_20261030.py')!='f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c':
        raise ValueError('Measured SDK constant input/base linker policy differs')
    name=relocation.get('symbol')
    if name not in ROLES:
        raise ValueError('Unqualified absolute SDK symbol name')
    expected=dict(symbol=name,offset=ROLES[name]['offset'],type=2,format='SHT_RELA',explicitAddend=0,originalEncodedWord='00000000')
    if any(relocation.get(key)!=value for key,value in expected.items()) or target!=0x400:
        raise ValueError('Absolute SDK integer symbol offset/addend/encoded word/value differs')
    if int.from_bytes(native[relocation['offset']:relocation['offset']+4],'little')!=0x400:
        raise ValueError('Original SDK absolute integer literal differs')
    return dict(program='',processor='arm7',module='absolute-sdk-linker-integer',kind='constant',mode='constant',address='0x400',
        region='numeric-symbol-no-memory-storage',storageBytes=0,sourceCredit=0,callerIdentity=dict(zip(
            ('program','processor','module','mode','address','bytes'),IDENTITY)),role=dict(ROLES[name],symbol=name,numericValue=1024,
            dereferenced=False,sourceMeaning='Extern linker-symbol address cast to integer stack length; no object memory access'),
        qualifier=Path(__file__).name,qualifierSha256=sha256(__file__))


def main():
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()[0x3F64:0x3F64+240]
    entry=dict(zip(('program','processor','module','mode','address','bytes'),IDENTITY),inputModuleSha256=MODULE_SHA,targetSha256=TARGET_SHA)
    bindings=[]
    controls=[]
    def reject(name,operation):
        try:
            operation()
        except ValueError as error:
            controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:
            raise ValueError('Invalid absolute constant role accepted: '+name)
    for name,role in ROLES.items():
        rel=dict(symbol=name,offset=role['offset'],type=2,format='SHT_RELA',explicitAddend=0,originalEncodedWord='00000000')
        bindings.append(qualify(entry,rel,0x400,raw))
        for field,value in (('program','utility-child'),('processor','arm9'),('module','arm7-main'),('mode','thumb'),
            ('address','0x37fc054'),('bytes',244),('inputModuleSha256','0'*64),('targetSha256','0'*64)):
            changed=dict(entry,**{field:value})
            reject(name+'-wrong-'+field,lambda changed=changed:qualify(changed,rel,0x400,raw))
        for field,value in (('symbol','SDK_OTHER'),('offset',role['offset']+4),('type',28),('format','SHT_REL'),
            ('explicitAddend',4),('originalEncodedWord','04000000')):
            changed=dict(rel,**{field:value})
            reject(name+'-wrong-'+field,lambda changed=changed:qualify(entry,changed,0x400,raw))
        reject(name+'-wrong-value',lambda:qualify(entry,rel,0x404,raw))
        changed=bytearray(raw)
        changed[role['offset']]^=1
        reject(name+'-wrong-original-byte',lambda:qualify(entry,rel,0x400,bytes(changed)))
    report=ROOT/'evidence/arm7/sdk-stack-linker-constants-20261031.json'
    write_json(report,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),bindings=bindings,controls=controls,allPassed=True,
        initializedDataBytes=0,sourceCredit=0,calleeSourceCredit=0,memoryMappingCredit=0,wholeModuleCredit=0,
        limitations=['Two exact integer-symbol roles for one measured ARM caller only; no general low-address binding or memory permission',
            'Native dataflow uses loaded1024 for comparison/subtraction before overwrite, with no dereference of that value',
            'The positive fixed length excludes the alternate nonpositive linker-length branch; no injected length or forced-PC coverage',
            'Integer roles alone provide no compiled function, native-return, module or ROM reconstruction credit']))
    print(dict(report=report.relative_to(ROOT).as_posix(),sha256=sha256(report),controls=len(controls),sourceCredit=0))


if __name__=='__main__':
    main()
