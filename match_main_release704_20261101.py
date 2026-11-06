import gzip
import json
import os
import struct
import subprocess
import match_runtime
from pathlib import Path
from elftools.elf.elffile import ELFFile
from project import ROOT,configuration,read_json,write_json,sha256
import match_main_oam_reference296_closed_20261101 as builder
from main_release704_fixture_v4_20261101 import execute,SPECS
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
from source_dependencies import dependencies_current

WORK=ROOT/"work/main-release704-qualified-20261101"
REPORT=ROOT/"evidence/matches/main-release704-20261101.json"


def witness(source,row,expressions,expected,label):
    generated=WORK/f"layout-{label}.c";obj=generated.with_suffix(".o")
    generated.write_text('#include "'+source.as_posix()+'"\nconst unsigned int layout[]={'+','.join(expressions)+'};\n',encoding="utf-8")
    compiler=ROOT/"tools/mwccarm/mwccarm/2.0/base/mwccarm.exe";assert sha256(compiler)==row["compilerSha256"]
    command=[str(compiler),*row["compilerFlags"],"-c",str(generated),"-o",str(obj)]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,
     env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/"tools/mwccarm/mwccarm/license.dat")))
    assert result.returncode==0,result.stdout+result.stderr
    with obj.open("rb")as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name(".symtab").iter_symbols()if s.name=="layout")
        data=elf.get_section(symbol["st_shndx"]).data()[symbol["st_value"]:symbol["st_value"]+symbol["st_size"]]
    values=list(struct.unpack("<"+str(len(expected))+"I",data));assert values==expected
    return dict(expressions=expressions,values=values,sourceSha256=sha256(generated),objectSha256=sha256(obj),
     command=command,historicalObjectExtentProven=False)


def main():
    WORK.mkdir(parents=True,exist_ok=True);builder.WORK=WORK
    config=configuration();assert sha256(config["rom"])==config["romSha256"]
    metadata,image,unused=measured_module("main")
    assert sha256(ROOT/metadata["binary"])=="ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f"
    matches=[];traces=[];summaries=[];controls=[];layouts=[]
    limits={0x0202E858:[],0x0202F358:[0x0202F3B4],0x0202F48C:[0x0202F4E4,0x0202F4F8],0x020321DC:[]}
    for entry,size in SPECS.items():
        source=ROOT/f"src/runtime/20261101_release704/native_main_{entry:08x}.c"
        text=source.read_text(encoding="utf-8")
        assert len(text.splitlines())<=500 and all(token not in text for token in["#include","/*","//","asm ","va_list"])
        row,proof,body=builder.build(source,f"correct-{entry:08x}",True)
        assert row["bytes"]==size and dependencies_current(row,{})
        row.update(exactBytes=size,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage="C",
         genuineLinkComparison=freeze_link(proof));matches.append(row)
        if entry==0x0202E858:
            expressions=["sizeof(u32)","sizeof(void*)","sizeof(NNSG3dAnmObj)",
             "(u32)&((NNSG3dResMdl*)0)->info.numNode","(u32)&((NNSG3dResMdl*)0)->info.numMat"]
            layouts.append(witness(source,row,expressions,[4,4,28,23,24],"animation"))
        if entry==0x0202F358:
            expressions=["(u32)&((NNSG3dResMdl*)0)->ofsMat","(u32)&((NNSG3dResMat*)0)->ofsDictPlttToMatList",
             "(u32)&((NNSG3dResDict*)0)->numEntry","(u32)&((NNSG3dResDict*)0)->ofsEntry",
             "(u32)&((NNSG3dResDictEntryHeader*)0)->data","(u32)&((NNSG3dResDictPlttToMatIdxData*)0)->flag"]
            layouts.append(witness(source,row,expressions,[8,2,1,6,4,3],"palette"))
        original=image[entry-0x02000000:entry-0x02000000+size];records=[];own=set();pool=set();helpers=0
        for index in range(264):
            native=execute(image,entry,original,index);rebuilt=execute(image,entry,body,index)
            assert native==rebuilt and native["modelPassed"],(hex(entry),index)
            records.append(native);own.update(native["ownedObserved"]);helpers+=native["actualHelperReturns"]*2
            for address,length,value in native["reads"]:
                if entry<=address and address+length<=entry+size:pool.update(range(address,address+length))
        missing=sorted(set(range(entry,entry+size,4))-own-{address&~3 for address in pool})
        assert missing==limits[entry],(hex(entry),missing)
        trace=ROOT/f"evidence/traces/main-release704-{entry:08x}-20261101.json.gz";trace.parent.mkdir(parents=True,exist_ok=True)
        trace.write_bytes(gzip.compress(json.dumps(dict(cases=records,actualOriginalReconstructedReturns=528),
         sort_keys=True,separators=(",",":")).encode(),mtime=0));traces.append(dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace)))
        summaries.append(dict(address=f"0x{entry:08X}",pairs=264,actualTopReturns=528,actualNativeHelperReturnsSeparate=helpers,
         observedInstructionBytes=len(own)*4,observedLiteralBytes=len(pool),unvisitedDefensiveInstructionAddresses=[f"0x{x:08X}"for x in missing]))
        if entry==0x0202E858:wrong=text.replace("sizeof(u16) *","sizeof(u32) *")
        elif entry==0x0202F358:wrong=text.replace("data->flag & 1","data->flag & 2")
        elif entry==0x0202F48C:wrong=text.replace("for (i = 0;","for (i = 1;")
        else:wrong=text.replace("if (texKey > 0)","if (texKey == 0)")
        assert wrong!=text
        bad_source=WORK/f"wrong-{entry:08x}.c";bad_source.write_text(wrong,encoding="utf-8")
        bad_row,bad_proof,bad_body=builder.build(bad_source,f"wrong-{entry:08x}",False)
        cases=[execute(image,entry,bad_body,index)for index in range(96)]
        rejected=sum(not c["modelPassed"]for c in cases);assert rejected>0
        controls.append(dict(address=f"0x{entry:08X}",sourceSha256=sha256(bad_source),objectSha256=bad_row["objectSha256"],
         actualReturningWrongCExecutions=96,independentModelRejections=rejected,positiveControls=96-rejected))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config["romSha256"],
     module="main",processor="arm9",program="",moduleSha256=metadata["sha256"],matches=matches,matchedFunctions=4,matchedBytes=704,
     oracle=dict(pairs=1056,actualTopReturns=2112,actualNativeHelperReturnsSeparate=sum(s["actualNativeHelperReturnsSeparate"]for s in summaries),
      providedCalls=0,fullRegistersFlagsMainResourcesStackReadsWritesCallsCompared=True,independentFieldAndCallbackModel=True),
     summaries=summaries,layoutWitnesses=layouts,negativeControls=controls,replayDependencies=traces,
     sourceOrigin=dict(referenceRevision="d636fb5d2b212e8736f09859fff447be2bd0ac85",historicalSdkRevisionProven=False,
      explicitSelectedUnsignedWordHelperFacades=True,sourceUintAndIntAre32Bit=True),
     reproductionCommand="python match_main_release704_20261101.py",scope=dict(sourceOnlyRom=False,windowsFullGame=False,
      androidDeviceExecutions=0,originalDataCredit=0,textureDictionariesEmpty=True,physicalVramAllocatorProven=False,
      originalDefaultRejectingFreeCallbacksExecuted=True,unvisitedDefensiveInstructionBytes=12,allOwnInstructionsExercised=False))
    write_json(REPORT,report);print(dict(functions=4,bytes=704,pairs=1056,actualReturns=2112,
     actualHelperReturns=report["oracle"]["actualNativeHelperReturnsSeparate"],providers=0))


if __name__=="__main__":
    main()
