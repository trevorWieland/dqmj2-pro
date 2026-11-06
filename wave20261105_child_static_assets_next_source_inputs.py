import sys
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
LANE=ROOT/'evidence/lanes/parallel-wave20261105/child-static-assets-next/source'
LAYOUT='src/utility/parallel_wave20261105/child-static-assets-next/layout.json'


def prepare():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/child-static-assets-next/source' or (LANE/'ready.json').exists():raise ValueError('Wrong new input scope or already-frozen semantic data READY')
    layout=read_json(ROOT/LAYOUT);files=set(code_closure(['wave20261105_child_static_assets_next_source_proof.py']));files.update([LAYOUT,'project.json','tools/mwccarm/mwccarm/license.dat']);files.update(a['semanticSource'] for a in layout['assets'])
    tool=ROOT/'tools/mwccarm/mwccarm/2.0/base';files.update(p.relative_to(ROOT).as_posix() for p in tool.iterdir() if p.is_file() and (p.suffix.lower()=='.dll' or p.name in ['mwccarm.exe','mwldarm.exe']))
    for package in ['ndspy','elftools','unicorn']:
        files.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'deps/native'/package).rglob('*') if p.is_file() and p.suffix.lower() in ['.py','.dll'])
    files.update(['extract/files/dwc/utility.bin',layout['binary']]);pins=[dict(path=p,sha256=sha256(ROOT/p),role='private-comparison-input' if p.startswith('extract/') else 'actual-producer-source-runtime-or-tool-input') for p in sorted(files)]
    document=dict(schemaVersion=1,sourceCredit=0,files=pins,actualSemanticInputs=38,privateComparisonInputs=2,noOriginalOrExtractedReadsDuringSourceGeneration=True,pythonVersion=sys.version)
    write_json(LANE/'inputs.json',document);print(dict(actualInputs=len(pins),inputsSha256=sha256(LANE/'inputs.json')))


if __name__=='__main__':prepare()
