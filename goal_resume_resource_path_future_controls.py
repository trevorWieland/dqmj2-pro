import re
from project import ROOT,read_json,sha256
import goal_resume_resource_path_future_proof as proof

ORIGINAL_NEGATIVE=proof.negative_source


def negative(source,folder,before,after):
    if before!='0,0x900':return ORIGINAL_NEGATIVE(source,folder,before,after)
    text=source.read_text()
    if text.count(before)!=2:raise ValueError('The documented bitmap negative must change exactly two real transfer callsites')
    text=text.replace(before,after)
    text=re.sub(r'(^\s*#include\s+)"([^"]+)"',lambda m:m[1]+'"'+(source.parent/m[2]).resolve().as_posix()+'"',text,flags=re.M)
    folder.mkdir(parents=True,exist_ok=True);path=folder/source.name;path.write_text(text)
    return path


def main():
    for pin in read_json(proof.FUTURE_LANE/'inputs-controls.json')['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen future fixture-adapter input changed')
    proof.negative_source=negative
    proof.main()


if __name__=='__main__':main()
