import re

import match_runtime as C
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from sequential_state_shapes import variants
from wave20261102_ov000_fourth_probe import divergence, object_body

LANE=ROOT/'evidence/lanes/parallel-wave20261102/battle-fifth'
SOURCE=ROOT/'src/ov001/parallel_wave20261102/battle-fifth/typed'
WORK=ROOT/'work/parallel-wave20261102/battle-fifth/typed'
BASE=list(C.FLAGS)


def prepare(target):
    original=ROOT/target['sourceTarget']
    text,header=original.read_text(),original.with_name('context.h').read_text()
    address=format(int(target['address'],0),'08x')
    changes=[]
    if address=='021de254':
        header=header.replace('extern u8 native_data_ov001_02238a0c[];','extern u32 native_data_ov001_02238a0c[];')
        text=text.replace('native_data_ov001_02238a0c + (native_data_ov001_022388ec.field_1c * 8)','native_data_ov001_02238a0c + (native_data_ov001_022388ec.field_1c * 2)')
        text=text.replace('void native_ov001_021de254','u32 native_ov001_021de254').rstrip()[:-1]+'    return 0U;\n}\n'
        changes.extend(['Native LDR actor word at8-byte script stride, while command column retains LDRB','Native epilogue returns R0 zero'])
    if address=='021dff00':
        header=header.replace('extern u8 native_data_ov001_0223896c[];','extern u32 native_data_ov001_0223896c[];')
        text=text.replace('native_data_ov001_022388ec.field_2b * 4','native_data_ov001_022388ec.field_2b')
        changes.append('Native actor-table LDR uses signed-byte index scaled by4')
    if address=='021dfd74':
        text=text.replace('void native_ov001_021dfd74','u32 native_ov001_021dfd74').rstrip()[:-1]+'    return 0U;\n}\n'
        changes.append('Native controller epilogue returns R0 zero')
    if address=='021dda80':
        text=text.replace('native_fn_ov001_021dc3c4();','native_fn_ov001_021dc3c4(0);')
        changes.append('Explicit side0 in native call sites formerly missing the first argument')
    linear=list(variants(text))
    if linear:
        text=linear[-1][1]
        changes.append('Sequential phase dispatch preserves one selected arm and matches native compare ordering')
    directory=SOURCE/address
    directory.mkdir(parents=True,exist_ok=True)
    path=directory/original.name
    path.write_text(text)
    path.with_name('context.h').write_text(header)
    return path,changes


def main():
    metadata,image,unused=measured_module('ov001')
    attempts=[]
    for target in read_json(LANE/'claim.json')['claimedFunctions']:
        path,changes=prepare(target)
        directory=WORK/format(int(target['address'],0),'08x')
        C.WORK=directory/'compile'
        C.FLAGS=BASE
        rows,unused=C.compare(path,'ov001','2','off',True)
        result=dict(identity=target['id'],changes=changes,sourceCredit=0)
        if len(rows)!=1 or rows[0].get('compileFailed'):
            result['compilerRefusal']=rows
            attempts.append(result)
            continue
        row=rows[0]
        row['sourceDependencies']=[dict(path=path.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(path.with_name('context.h')))]
        result['entry']=row
        try:
            bindings=qualified_bindings(row)
            result.update(realLink=validate(row,bindings,directory/'link'),exact=True)
            row['nativeSymbolEntries']=bindings
        except Exception as error:
            result.update(exact=False,linkRefusal=error.args[0]if error.args else str(error))
        linked=directory/'link/caller.bin'
        offset=int(target['address'],0)-0x21D7240
        result['divergence']=divergence(image[offset:offset+target['bytes']],linked.read_bytes()if linked.exists()else object_body(row),int(target['address'],0))
        attempts.append(result)
        print(target['address'],target['bytes'],row['compiledBytes'],row['matchingBytes'],result['exact'],flush=True)
    write_json(LANE/'typed-probe.json',dict(schemaVersion=1,claimSha256=sha256(LANE/'claim.json'),moduleSha256=metadata['sha256'],sourceCredit=0,actualNativeFunctionReturns=0,attempts=attempts,exact=[row for row in attempts if row.get('exact')]))


if __name__=='__main__':
    main()
