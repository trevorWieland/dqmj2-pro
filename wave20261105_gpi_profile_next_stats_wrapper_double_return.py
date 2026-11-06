import argparse
import hashlib
import json
import random
from project import ROOT,read_json,write_json,sha256
from wave20261105_gpi_profile_next_stats_wrapper_paths import assert_owned,EVIDENCE,SOURCE,WORK
from wave20261105_gpi_profile_next_stats_wrapper_fixtures import run,helpers,vector


def main():
    assert_owned(EVIDENCE,SOURCE,WORK)
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);args=parser.parse_args();path=EVIDENCE/'inputs.json'
    if sha256(path)!=args.inputs_sha256:raise ValueError('Immutable stats input manifest differs')
    manifest=read_json(path)
    for pin in manifest['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable stats input changed:'+pin['path'])
    row=next(r for r in read_json(EVIDENCE/'match.json')['matches'] if r['address']=='0x20b3780');image=(ROOT/'extract/arm9/arm9.bin').read_bytes();a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
    if hashlib.sha256(native).hexdigest()!=row['targetSha256'] or native!=linked:raise ValueError('Fresh genuine complete double-return caller differs')
    rng=random.Random(0x11b3780);bits=[0,0x8000000000000000,0x3ff8000000000000,0x7ff0000000000000,0xfff0000000000000,0x7ff8000012345678,0x7ff0000000000001]+[1<<i for i in range(64)]+[rng.getrandbits(64) for _ in range(32)];records=[];allowed=helpers(image)
    for seed,value in enumerate(bits):
        v=vector(a,seed);v.update(mode=0,doubleBits=value);original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
        if original!=source or not original['modelPassed'] or not original['topReturned'] or original['actualOriginalHelperInvocations']:raise ValueError('Actual independent raw double fallback return differs')
        records.append(original)
    result=dict(status='passed',inputManifestSha256=sha256(path),address=row['address'],targetSha256=row['targetSha256'],sourceSha256=row['sourceSha256'],vectors=len(records),nativeAndCompiledReturningCalls=2*len(records),records=records,actualCalleeBodiesExecuted=0,providerBodiesExecuted=0,sourceCredit=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),limits=['Supplemental explicit103 actual entry/return pairs independently force no explicit/default game. Raw64bit R0/R1 returns cover both zeros,finite,positive/negative infinities,quiet/signaling NaN payloads,64 individual bits and32 deterministic random patterns.0numeric operations/provider returns/bodies/Windows execution.','Primary396-vector report120returns/672stops/432helperentries remains its unchanged original count. Its signed-zero/NaN frame claim is supplemented here with actual complete fallback returns; these206 actual returns are separate, never silently added to that report.'])
    write_json(EVIDENCE/'double-return-supplement.json',result);print(dict(status='passed',vectors=len(records),actualNativeAndSourceReturns=result['nativeAndCompiledReturningCalls'],traceSha256=result['traceSha256']))


if __name__=='__main__':main()
