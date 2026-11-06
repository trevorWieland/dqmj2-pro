import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_controller123_prefix_20261101 as P


def main():
    P.verify_inputs();r=json.loads((ROOT/'evidence/attempts/save-core-controller123-minimal-last-20261101.json').read_text())['match'];assert P.B.sha((ROOT/r['source']).read_bytes())==r['sourceSha256'];arm=P.B.measured_module('main')[1];P.B.MODULE='main';P.B.MODE='arm';P.B.ENTRY=P.ENTRY;P.B.LENGTH=716;P.B.NAME=r['name'];P.B.SOURCE=r['source'];P.B.WORK='work/scc123/preferred_prefix';P.B.FLAGS=r['flags'];P.B.COMPILER=r['compilerPath'];P.B.COMPILER_HASH=r['compilerSha256'];row,body=P.B.build(arm[0x70298:0x70564]);assert not row['exactByteEqual'] and row['sameOffsetBytes']==696;vectors=[]
    for p in P.profiles():
        a=P.Machine(arm,p).run();b=P.Machine(arm,p,body).run();P.validate(a);assert a==b;vectors.append(a)
    data=P.sidecar(vectors,'evidence/vectors/save-core-controller123-preferred-prefix-20261101.json.gz');out=dict(schemaVersion=1,match=row,cases=len(vectors),actualTopReturns=2*len(vectors),physicalNativeHelperReturns=2*sum(len(v['physicalNativeReturns']) for v in vectors),providers=0,vectorSidecar=data,nativeCaseDigest=data['uncompressedSha256'],sourceCredit=0,limits=['Preferred696/716 declaration-only hypothesis is separately replayed over the same796 original-RAM/default-state cases as earlier689/716;these are duplicate semantic contexts withzeroexact/module/new-source coverage.','Earlier golden/control reports remainunchanged. States0/1 andcompletecontroller behavior remainunsupported;alloriginal helper/code/data/backing/register/actual-return guards stayactive.']);path=ROOT/'evidence/functional/save-core-controller123-preferred-prefix-20261101.json';path.write_text(json.dumps(out,indent=2)+'\n');print(dict(cases=len(vectors),actualTopReturns=out['actualTopReturns'],sha256=P.B.sha(path.read_bytes())))


if __name__=='__main__':main()
