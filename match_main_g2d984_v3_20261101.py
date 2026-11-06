import gzip
import json
from pathlib import Path
import match_runtime
from project import ROOT,configuration,read_json,write_json,sha256
import match_main_oam_reference296_closed_20261101 as builder
import match_main_release704_20261101 as layouts
from main_g2d984_machine_v3_20261101 import execute,SPECS
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
from source_dependencies import dependencies_current

WORK=ROOT/"work/main-g2d984-qualified-v3-20261101"
REPORT=ROOT/"evidence/matches/main-g2d984-v3-20261101.json"
NEW={0x02034480,0x020344C8,0x02034558,0x020348AC,0x02034AB8,0x02034988,0x02034A1C}


def layout_checks(rows):
    layouts.WORK=WORK
    definitions={
     0x02034558:(["sizeof(void*)","sizeof(u32)","sizeof(NNSG2dAnimBankData)","sizeof(NNSG2dAnimSequenceData)",
      "sizeof(NNSG2dAnimFrameData)","(u32)&((NNSG2dAnimBankData*)0)->pSequenceArrayHead",
      "(u32)&((NNSG2dAnimBankData*)0)->pFrameArrayHead","(u32)&((NNSG2dAnimBankData*)0)->pAnimContents",
      "(u32)&((NNSG2dAnimBankData*)0)->pExtendedData","(u32)&((NNSG2dAnimSequenceData*)0)->pAnmFrameArray",
      "sizeof(NNSG2dUserExAnimAttrBank)","sizeof(NNSG2dUserExAnimSequenceAttr)",
      "(u32)&((NNSG2dUserExAnimSequenceAttr*)0)->pAttr","(u32)&((NNSG2dUserExAnimSequenceAttr*)0)->pAnmFrmAttrArray"],
      [4,4,24,16,8,4,8,12,20,12,8,12,4,8]),
     0x020348AC:(["sizeof(NNSG2dBinaryFileHeader)","sizeof(NNSG2dBinaryBlockHeader)","sizeof(NNSG2dFontInformation)",
      "(u32)&((NNSG2dFontInformation*)0)->pGlyph","(u32)&((NNSG2dFontInformation*)0)->pWidth",
      "(u32)&((NNSG2dFontInformation*)0)->pMap","(u32)&((NNSG2dFontWidth*)0)->pNext",
      "(u32)&((NNSG2dFontCodeMap*)0)->pNext","(u32)&((NNSG2dFontGlyph*)0)->flags"],[16,8,20,8,12,16,4,8,7]),
     0x02034A1C:(["sizeof(Bank)","sizeof(Cell)","sizeof(CellBR)","sizeof(Transfer)",
      "(u32)&((Bank*)0)->cells","(u32)&((Bank*)0)->transfer","(u32)&((Bank*)0)->extended",
      "(u32)&((Cell*)0)->oam"],[24,8,16,8,4,12,20,4]),
     0x02034AB8:(["sizeof(NNSiG2dBitReader)","(u32)&((NNSiG2dBitReader*)0)->availableBits",
      "(u32)&((NNSiG2dBitReader*)0)->bits"],[8,4,5])}
    return [layouts.witness(ROOT/rows[address]["source"],rows[address],expr,values,f"g2d-{address:08x}")
     for address,(expr,values)in definitions.items()]


def main():
    WORK.mkdir(parents=True,exist_ok=True);builder.WORK=WORK
    config=configuration();assert sha256(config["rom"])==config["romSha256"]
    metadata,image,unused=measured_module("main")
    assert sha256(ROOT/metadata["binary"])=="ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f"
    matches=[];bodies={};by_address={};summaries=[];traces=[];controls=[]
    for address,size in SPECS.items():
        folder="20261101_g2d796"if address in NEW else"20261101_g2d796_callers"
        source=ROOT/f"src/runtime/{folder}/native_main_{address:08x}.c"
        row,proof,body=builder.build(source,f"correct-{address:08x}",True)
        assert row["bytes"]==size and dependencies_current(row,{})
        row.update(exactBytes=size,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage="C",
         genuineLinkComparison=freeze_link(proof));matches.append(row);bodies[address]=body;by_address[address]=row
    witnesses=layout_checks(by_address)
    for entry,size in SPECS.items():
        cases=[];own=set();pool=set();helpers=0
        for index in range(192):
            native=execute(image,entry,{},index);rebuilt=execute(image,entry,bodies,index)
            assert native==rebuilt and native["modelPassed"],(hex(entry),index)
            cases.append(native);own.update(native["ownedObserved"]);helpers+=native["actualNativeHelperReturns"]*2
            for address,length,value in native["reads"]:
                if entry<=address and address+length<=entry+size:pool.update(range(address,address+length))
        missing=sorted(set(range(entry,entry+size,4))-own-{address&~3 for address in pool})
        if entry in NEW:assert not missing,(hex(entry),missing)
        trace=ROOT/f"evidence/traces/main-g2d984-v3-{entry:08x}-20261101.json.gz";trace.parent.mkdir(parents=True,exist_ok=True)
        trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases,actualTopReturns=384),sort_keys=True,separators=(",",":")).encode(),mtime=0))
        traces.append(dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace)))
        summaries.append(dict(address=f"0x{entry:08X}",pairs=192,actualTopReturns=384,actualNativeHelperReturnsSeparate=helpers,
         instructionBytesObserved=len(own)*4,literalBytesObserved=len(pool),unvisitedInstructionAddresses=[f"0x{x:08X}"for x in missing]))
    for entry in sorted(NEW):
        source=ROOT/by_address[entry]["source"];text=source.read_text(encoding="utf-8")
        if entry==0x02034480:wrong=text.replace("pCursor->kind == signature","pCursor->kind != signature")
        elif entry==0x020344C8:wrong=text.replace("+ (u32) pCellAttrBank)","+ (u32) pCellAttrBank + 4)")
        elif entry==0x02034558:wrong=text.replace("(u32)(pData->pAnimContents) + (u32) pData)","(u32)(pData->pAnimContents) + (u32) pData + 4)")
        elif entry==0x020348AC:wrong=text.replace("+ (u32)pBase)","+ (u32)pBase + 4)")
        elif entry==0x02034AB8:wrong=text.replace("0xFF >>","0x7F >>")
        elif entry==0x02034988:wrong=text.replace("(CellBR *)bank->cells","(Cell *)bank->cells")
        else:wrong=text.replace("(u32)cell->oam + (u32)oam)","(u32)cell->oam + (u32)oam + 4)")
        assert wrong!=text,hex(entry)
        bad_source=WORK/f"wrong-{entry:08x}.c";bad_source.write_text(wrong,encoding="utf-8")
        row,proof,body=builder.build(bad_source,f"wrong-{entry:08x}",False)
        outcomes=[execute(image,entry,{entry:body},index)for index in range(96)]
        rejected=sum(not c["modelPassed"]for c in outcomes);assert rejected>0,hex(entry)
        controls.append(dict(address=f"0x{entry:08X}",actualWrongCReturns=96,rejected=rejected,positiveControls=96-rejected,
         sourceSha256=sha256(bad_source),objectSha256=row["objectSha256"]))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config["romSha256"],
     processor="arm9",program="",module="main",moduleSha256=metadata["sha256"],matches=matches,matchedFunctions=13,matchedBytes=1580,
     netNewFunctions=7,netNewBytes=984,existingMigrationFunctions=6,existingMigrationBytes=596,summaries=summaries,
     layoutWitnesses=witnesses,negativeControls=controls,replayDependencies=traces,
     oracle=dict(pairs=2496,actualTopReturns=4992,actualNativeHelperReturnsSeparate=sum(s["actualNativeHelperReturnsSeparate"]for s in summaries),
      providedCalls=0,wholeReconstructedHelperGroupExecuted=True,independentByteFieldAndBitStreamModels=True,
      fullRegistersFlagsResourcesMainStackReadsWritesCallsCompared=True,newOwnInstructionAndLiteralCoverageComplete=True),
     sourceOrigin=dict(referenceRevision="d636fb5d2b212e8736f09859fff447be2bd0ac85",historicalSdkRevisionProven=False,
      selectedCallerWordInterfacesCoherent=True,duplicateSelfAssignmentsRemoved=True),
     reproductionCommand="python match_main_g2d984_v3_20261101.py",
     limitations=["Synthetic referenced fields and nonoverlapping backing arrays are verified, not a complete binary-format or text/font validity proof",
      "Font caller versions100/101/102 only; malformed assertion paths and invalid pointers are unsupported",
      "Bit-reader domain0..8 requested/available bits; serialized pointers and layouts are32-bit",
      "No full Windows game, source-only ROM or Android device execution; existing596-byte alternatives add zero credit"])
    write_json(REPORT,report);print(dict(newFunctions=7,newBytes=984,existingMigrationBytes=596,actualTopReturns=4992,
     actualHelperReturns=report["oracle"]["actualNativeHelperReturnsSeparate"],providers=0))


if __name__=="__main__":
    main()
