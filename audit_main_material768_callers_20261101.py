import re
from project import ROOT,read_json,write_json,sha256


def main():
    entries=[0x0202F520,0x0202F5C8,0x0202F640,0x0202F6B8,0x0202F730,0x0202F7A8]
    snapshot=ROOT/"evidence/verification/accepted-cohort123-identities-v2-20261101.json"
    assert sha256(snapshot)=="29a8dd0d95d7045fffe84f990fa409894e0e1aebb145286f948ebe504d48dc4e"
    rows=read_json(snapshot)["functions"];sources={row["source"]:row["sourceSha256"]for row in rows}
    specifications=["cohort124-pure-and-connected-specification-v2-20261101.json",
     "cohort125-larger-sdk-and-controller-specification-20261101.json"]
    for name in specifications:
        for packet in read_json(ROOT/name)["packets"]:
            for row in read_json(ROOT/packet["report"])["matches"]:sources[row["source"]]=row["sourceSha256"]
    found=[]
    for path,digest in sorted(sources.items()):
        assert sha256(ROOT/path)==digest,path
        text=(ROOT/path).read_text(encoding="utf-8").lower()
        for entry in entries:
            if re.search(r"\b(?:native_fn_|native_main_|func_|sub_)"+f"{entry:08x}"+r"\b",text):
                found.append(dict(source=path,address=hex(entry)))
    assert not found,found
    write_json(ROOT/"evidence/abi/main-material768-selected-caller-scan-20261101.json",dict(passed=True,
     generatorSha256=sha256(__file__),sourceCredit=0,selected123SnapshotSha256=sha256(snapshot),
     additionalCandidateCohorts=[124,125],uniqueSourceFiles=len(sources),directNamedReferences=found,
     indirectCallsAndUnrecognizedSymbolSpellingsNotProven=True,sdkVoidFormalsRetained=True,
     reproductionCommand="python audit_main_material768_callers_20261101.py"))
    print(dict(uniqueSourceFiles=len(sources),namedIncomingMaterialCalls=len(found)))


if __name__=="__main__":
    main()
