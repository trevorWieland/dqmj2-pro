import os
import struct
import subprocess
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,configuration,read_json,write_json,sha256
import match_main_oam_reference296_closed_20261101 as builder
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
from source_dependencies import dependencies_current
from main_material768_fixture_v2_20261101 import execute,SPECS

WORK=ROOT/"work/main-material768-qualified-v2-20261101"
REPORT=ROOT/"evidence/matches/main-material768-v2-20261101.json"
EXPECTED_UNOBSERVED={0x0202F520:[0x0202F58C,0x0202F5A0],0x0202F5C8:[0x0202F614,0x0202F628],
 0x0202F640:[0x0202F68C,0x0202F6A0],0x0202F6B8:[0x0202F704,0x0202F718],
 0x0202F730:[0x0202F77C,0x0202F790],0x0202F7A8:[0x0202F7F4,0x0202F808]}


def layout(source,row):
    generated=WORK/"layout.c";obj=WORK/"layout.o"
    expressions=["sizeof(u32)","sizeof(void*)","sizeof(NNSG3dResMdl)","sizeof(NNSG3dResMatData)",
     "(u32)&((NNSG3dResMdl*)0)->info.numMat","(u32)&((NNSG3dResMdl*)0)->ofsMat",
     "(u32)&((NNSG3dResMat*)0)->dict","(u32)&((NNSG3dResDict*)0)->ofsEntry",
     "(u32)&((NNSG3dResDictEntryHeader*)0)->data","(u32)&((NNSG3dResMatData*)0)->polyAttr",
     "(u32)&((NNSG3dResMatData*)0)->polyAttrMask"]
    generated.write_text('#include "'+source.as_posix()+'"\nconst unsigned int material_layout[]={'+','.join(expressions)+'};\n',encoding="utf-8")
    compiler=ROOT/"tools/mwccarm/mwccarm/2.0/base/mwccarm.exe";assert sha256(compiler)==row["compilerSha256"]
    command=[str(compiler),*row["compilerFlags"],"-c",str(generated),"-o",str(obj)]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,
     env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/"tools/mwccarm/mwccarm/license.dat")))
    assert result.returncode==0,result.stdout+result.stderr
    with obj.open("rb")as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name(".symtab").iter_symbols()if s.name=="material_layout")
        raw=elf.get_section(symbol["st_shndx"]).data()[symbol["st_value"]:symbol["st_value"]+symbol["st_size"]]
    values=list(struct.unpack("<11I",raw));assert values==[4,4,76,44,24,8,4,6,4,12,16]
    return dict(expressions=expressions,values=values,sourceSha256=sha256(generated),objectSha256=sha256(obj),
     command=command,originalObjectExtentOrHistoricalSdkVersionProven=False)


def main():
    builder.WORK=WORK;WORK.mkdir(parents=True,exist_ok=True)
    metadata,image,_=measured_module("main");matches=[];proofs=[];trials=[];controls=[];evidence=[];abi=None
    expected_main="ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f"
    assert sha256(ROOT/metadata["binary"])==expected_main
    config=configuration();assert sha256(config["rom"])==config["romSha256"]
    for entry,(size,mask,shift)in SPECS.items():
        source=ROOT/f"src/runtime/20261101_material768/native_main_{entry:08x}.c"
        row,proof,body=builder.build(source,f"qualified-{entry:08x}",True)
        assert row["bytes"]==size and dependencies_current(row,{})
        if abi is None:abi=layout(source,row)
        frozen=freeze_link(proof);row["genuineLinkComparison"]=frozen;matches.append(row);proofs.append(frozen)
        records=[];own=set()
        original=image[entry-0x02000000:entry-0x02000000+size]
        for index in range(192):
            native=execute(image,entry,original,index);reconstructed=execute(image,entry,body,index)
            assert native==reconstructed and native["modelPassed"]
            own.update(native["ownedObserved"]);records.append(native)
        missing=sorted(set(range(entry,entry+size,4))-own);assert missing==EXPECTED_UNOBSERVED[entry]
        path=ROOT/f"evidence/native-runs/main-material768-v2-{entry:08x}-20261101.json"
        write_json(path,dict(identity=dict(module="main",address=f"0x{entry:08X}",mode="arm"),results=records,
         independentModel=True,actualOriginalAndReconstructedReturns=384,providedCalls=0,actualHelperReturns=0,
         observedCodeBytes=len(own)*4,unvisitedNullOrInvalidDictionaryGuardInstructions=[f"0x{x:08X}"for x in missing]))
        evidence.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)))
        trials.append(dict(address=f"0x{entry:08X}",count=192,passed=True))
        text=source.read_text(encoding="utf-8")
        wrong=text.replace("|= mask","^= mask")if entry==0x0202F520 else text.replace("& ~","| ")
        assert wrong!=text
        wrong_source=WORK/f"wrong-{entry:08x}.c";wrong_source.write_text(wrong,encoding="utf-8")
        wrong_row,wrong_proof,wrong_body=builder.build(wrong_source,f"wrong-{entry:08x}",False)
        rejected=0
        for index in range(96):
            observed=execute(image,entry,wrong_body,index)
            rejected+=not observed["modelPassed"]
        assert rejected>0
        controls.append(dict(address=f"0x{entry:08X}",sourceSha256=sha256(wrong_source),objectSha256=wrong_row["objectSha256"],
         actualReturningWrongCExecutions=96,rejected=rejected,positiveControls=96-rejected,
         mutation="setting mask uses XOR"if entry==0x0202F520 else"bit clearing replaced by setting"))
    report=dict(matches=matches,nativeTrials=trials,genuineLinkComparisons=proofs,nativeEvidence=evidence,
     layoutWitness=abi,returningWrongCControls=controls,counts=dict(functions=6,matchingBytes=768,
      originalReconstructedPairs=1152,actualTopLevelReturns=2304,providedCalls=0,actualHelperReturns=0),
     originalMainSha256=expected_main,scope=dict(fullGame=False,sourceOnlyRom=False,windowsFullGame=False,
      androidDeviceExecutions=0,assembly=False,originalDataCredit=0,compilerLinkedExact=True,
      malformedResourceReturnCoverage=False,allOwnInstructionsExercised=False,unvisitedDefensiveInstructionBytes=48,
      sdkVoidReturnPreserved=True,rawReturnRegistersCompared=True))
    write_json(REPORT,report)
    print("Six material routines: 768 genuine linked bytes, 1152 pairs/2304 actual returns; guards remain explicitly unvisited")


if __name__=="__main__":
    main()
