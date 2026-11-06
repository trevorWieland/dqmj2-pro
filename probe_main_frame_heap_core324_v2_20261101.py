import json
from pathlib import Path
import main_sdk_heap_attribute424_compile_20261101 as compiler
from project import ROOT,sha256,write_json

PROFILE=ROOT/'nonmatching/main-sdk-heap/20261101/lane-frame-core324-v2/profile.json'
WORK=ROOT/'work/main-sdk-heap/20261101/lane-frame-core324-v2'


def main():
    results=[]
    for pin in json.loads(PROFILE.read_text())['matches']:
        entry,bindings,link,mismatch,code=compiler.build(pin,WORK/pin['address'],strict=False)
        results.append(dict(entry=entry,bindings=bindings,realMainLink=link,mismatch=mismatch,compiledBytes=len(code),sourceCredit=0))
        print(json.dumps(dict(address=pin['address'],bytes=len(code),exact=bool(link),mismatch=mismatch)),flush=True)
    write_json(WORK/'first-links.json',dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),results=results,sourceCredit=0))


if __name__=='__main__':main()
