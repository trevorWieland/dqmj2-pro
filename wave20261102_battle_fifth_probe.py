import match_runtime as C
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from wave20261102_ov000_fourth_probe import divergence, object_body

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/battle-fifth'
WORK = ROOT / 'work/parallel-wave20261102/battle-fifth/initial'
BASE = list(C.FLAGS)


def main():
    claim = read_json(LANE / 'claim.json')
    metadata, image, unused = measured_module('ov001')
    attempts = []
    for target in claim['claimedFunctions']:
        path = ROOT / target['sourceTarget']
        if sha256(path) != target['sourceSha256'] or sha256(path.with_name('context.h')) != target['headerSha256']:
            raise ValueError('Initial battle claim source changed')
        directory = WORK / format(int(target['address'],0),'08x')
        C.WORK = directory / 'compile'
        C.FLAGS = BASE
        rows, unused = C.compare(path,'ov001','2','off',True)
        result = dict(identity=target['id'],sourceCredit=0)
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
    write_json(LANE/'initial-probe.json',dict(schemaVersion=1,claimSha256=sha256(LANE/'claim.json'),moduleSha256=metadata['sha256'],sourceCredit=0,actualNativeFunctionReturns=0,attempts=attempts,exact=[row for row in attempts if row.get('exact')],limits=['Initial existing-draft/compiler/link diagnosis only. Complete semantic/ABI fixtures and host-wide linkage remain separate; every nonmatch and unsupported prototype retains zero credit.']))


if __name__=='__main__':
    main()
