import gzip
import json
from pathlib import Path
import match_runtime
from project import ROOT,configuration,write_json,sha256
import match_main_oam_reference296_closed_20261101 as builder
import main_rng_scene_fixture_20261101 as fixture
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

SOURCE=ROOT/"src/runtime/20261101_rng_scene_explicit/native_main_02043844.c"
REPORT=ROOT/"evidence/matches/main-rng-scene-explicit-20261101.json"
TRACE=ROOT/"evidence/traces/main-rng-scene-explicit-20261101.json.gz"


def main():
    config=configuration();assert sha256(config["rom"])==config["romSha256"]
    metadata,image,unused=measured_module("main")
    assert sha256(ROOT/metadata["binary"])=="ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f"
    builder.WORK=ROOT/"work/main-rng-scene-explicit-20261101"
    row,proof,body=builder.build(SOURCE,"correct",True);assert row["bytes"]==96
    original=image[fixture.ENTRY-0x02000000:fixture.ENTRY-0x02000000+96]
    records=[];own=set();helper_returns=0;provided=0
    for index in range(1152):
        native=fixture.execute(image,original,index);rebuilt=fixture.execute(image,body,index)
        assert native==rebuilt and native["modelPassed"],index
        records.append(native);own.update(native["ownedObserved"]);helper_returns+=native["actualNativeHelperReturns"]*2
        provided+=len(native["providedCalls"])*2
    assert own==set(range(fixture.ENTRY,fixture.ENTRY+92,4))
    text=SOURCE.read_text(encoding="utf-8");needle="native_fn_0203d2ec(native_fn_0204457c());";assert text.count(needle)==1
    controls=[]
    for label,replacement in[("wrong-seed","native_fn_0203d2ec(native_fn_0204457c() + 1U);"),
     ("omit-setter","native_fn_0204457c();")]:
        wrong=builder.WORK/f"{label}.c";wrong.parent.mkdir(parents=True,exist_ok=True);wrong.write_text(text.replace(needle,replacement),encoding="utf-8")
        bad_row,bad_proof,bad_body=builder.build(wrong,label,False)
        outcomes=[fixture.execute(image,bad_body,index)for index in range(1024,1056)]
        rejected=sum(not item["modelPassed"]for item in outcomes);assert rejected==32
        controls.append(dict(label=label,actualWrongCReturns=32,rejected=rejected,sourceSha256=sha256(wrong),objectSha256=bad_row["objectSha256"]))
    TRACE.parent.mkdir(parents=True,exist_ok=True);TRACE.write_bytes(gzip.compress(json.dumps(dict(cases=records),sort_keys=True,separators=(",",":")).encode(),mtime=0))
    row.update(exactBytes=96,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage="C",genuineLinkComparison=freeze_link(proof))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config["romSha256"],
     processor="arm9",program="",module="main",moduleSha256=metadata["sha256"],matches=[row],matchedFunctions=1,matchedBytes=96,
     netNewFunctions=0,netNewBytes=0,primaryReplacementCandidate=True,previousSource="src/runtime/runtime03/native_main_02043844.c",
     previousSourceSha256=sha256(ROOT/"src/runtime/runtime03/native_main_02043844.c"),
     oracle=dict(pairs=1152,actualTopReturns=2304,actualNativeHelperReturnsSeparate=helper_returns,
      explicitlyProvidedOverlayServiceCalls=provided,allOwnInstructionsObserved=True,observedInstructionBytes=92,generatedLiteralBytes=4,
      seedIsMirrorExactlyWhenByte24Equals2=True,independentFullMainStateModel=True,modeByteValues=256,mode2Cases=132),
     negativeControls=controls,replayDependencies=[dict(path=TRACE.relative_to(ROOT).as_posix(),sha256=sha256(TRACE))],
     selectedHelperInterfacesPreserved=True,unselectedOverlayServiceFormalsUnproved=True,
     reproductionCommand="python match_main_rng_scene_explicit_20261101.py",
     limitations=["Overlay initialization services are explicitly provided and do not mutate the synthetic frame; actual scene effects and reachability are unproved",
      "Native actual RNG mode/getter/seed-mirror/setter chain executes; mirror provenance, persistence and player control are unproved",
      "This96-byte existing-source migration adds zero function/byte credit and is not a full Windows game or source-only ROM proof"])
    write_json(REPORT,report);print(dict(existingBytes=96,newBytes=0,pairs=1152,actualReturns=2304,actualNativeHelperReturns=helper_returns,provided=provided))


if __name__=="__main__":
    main()
