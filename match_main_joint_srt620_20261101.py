import gzip
import json
from pathlib import Path
import match_runtime
from project import ROOT,configuration,write_json,sha256
import match_main_oam_reference296_closed_20261101 as builder
import match_main_release704_20261101 as layouts
from main_joint_srt620_fixture_20261101 import execute,SPECS
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

WORK=ROOT/"work/main-joint-srt620-qualified-20261101"
REPORT=ROOT/"evidence/matches/main-joint-srt620-20261101.json"


def main():
    WORK.mkdir(parents=True,exist_ok=True);builder.WORK=WORK;layouts.WORK=WORK
    config=configuration();assert sha256(config["rom"])==config["romSha256"]
    metadata,image,unused=measured_module("main");assert sha256(ROOT/metadata["binary"])=="ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f"
    matches=[];summaries=[];traces=[];controls=[];witness=None
    for entry,size in SPECS.items():
        source=ROOT/f"src/runtime/20261101_joint_srt620/native_main_{entry:08x}.c"
        row,proof,body=builder.build(source,f"correct-{entry:08x}",True);assert row["bytes"]==size
        row.update(exactBytes=size,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage="C",
         genuineLinkComparison=freeze_link(proof));matches.append(row)
        if witness is None:
            expressions=["sizeof(u32)","sizeof(s32)","sizeof(NNSG3dJntAnmResult)",
             "(u32)&((NNSG3dJntAnmResult*)0)->scale","(u32)&((NNSG3dJntAnmResult*)0)->scaleEx0",
             "(u32)&((NNSG3dJntAnmResult*)0)->scaleEx1","(u32)&((NNSG3dJntAnmResult*)0)->rot",
             "(u32)&((NNSG3dJntAnmResult*)0)->trans"]
            witness=layouts.witness(source,row,expressions,[4,4,88,4,16,28,40,76],"joint-result")
        original=image[entry-0x02000000:entry-0x02000000+size];cases=[];own=set();helpers=0
        for index in range(768):
            native=execute(image,entry,original,index);rebuilt=execute(image,entry,body,index)
            assert native==rebuilt and native["modelPassed"],(hex(entry),index)
            own.update(native["ownedObserved"]);helpers+=native["actualNativeHelperReturns"]*2;cases.append(native)
        assert own==set(range(entry,entry+size,4)),(hex(entry),sorted(set(range(entry,entry+size,4))-own))
        trace=ROOT/f"evidence/traces/main-joint-srt620-{entry:08x}-20261101.json.gz";trace.parent.mkdir(parents=True,exist_ok=True)
        trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases,actualTopReturns=1536),sort_keys=True,separators=(",",":")).encode(),mtime=0))
        traces.append(dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace)))
        summaries.append(dict(address=f"0x{entry:08X}",pairs=768,actualTopReturns=1536,
         actualNativeHelperReturnsSeparate=helpers,instructionBytesObserved=size))
        text=source.read_text(encoding="utf-8")
        if entry==0x0202CF80:wrong=text.replace(">> 12",">> 11")
        else:wrong=text.replace("0x1b ,","0x1c ,")
        assert wrong!=text
        bad=WORK/f"wrong-{entry:08x}.c";bad.write_text(wrong,encoding="utf-8")
        bad_row,bad_proof,bad_body=builder.build(bad,f"wrong-{entry:08x}",False)
        results=[execute(image,entry,bad_body,index)for index in range(768)]
        rejected=sum(not item["modelPassed"]for item in results);assert rejected>0
        controls.append(dict(address=f"0x{entry:08X}",actualWrongCReturns=768,rejected=rejected,
         positiveControls=768-rejected,sourceSha256=sha256(bad),objectSha256=bad_row["objectSha256"]))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config["romSha256"],
     processor="arm9",program="",module="main",moduleSha256=metadata["sha256"],matches=matches,matchedFunctions=3,matchedBytes=620,
     oracle=dict(pairs=2304,actualTopReturns=4608,actualNativeHelperReturnsSeparate=sum(s["actualNativeHelperReturnsSeparate"]for s in summaries),
      providedCalls=0,allOwnInstructionBytesObserved=620,independentCommandAndQ12Models=True,
      fullRegistersFlagsMainDataStackHardwareReadsWritesCallsCompared=True),summaries=summaries,layoutWitness=witness,
     negativeControls=controls,replayDependencies=traces,
     sourceOrigin=dict(referenceRevision="d636fb5d2b212e8736f09859fff447be2bd0ac85",historicalSdkRevisionProven=False,
      sizeofResult=88,scalarWidth=32,voidReturnPreserved=True),
     reproductionCommand="python match_main_joint_srt620_20261101.py",
     limitations=["Direct/empty-buffer static FIFO shadow and bounded pending-DMA command buffering only; no physical GPU or actual asyncDMA concurrency",
      "Original command-buffer/CPU-copy/send helpers execute without substitution but receive no new source credit",
      "No overflow-buffer flush, busy-wait completion, rendered image, scene, full Windows game, source-only ROM or Android device proof"])
    write_json(REPORT,report);print(dict(functions=3,bytes=620,pairs=2304,actualTopReturns=4608,
     actualNativeHelperReturns=report["oracle"]["actualNativeHelperReturnsSeparate"],providers=0))


if __name__=="__main__":
    main()
