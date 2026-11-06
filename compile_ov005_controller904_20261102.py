import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from project import ROOT,write_json,sha256
import match_runtime as C
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def execute():
    source=ROOT/'nonmatching/overlay-lane/20261102-controller903/explicit-descriptor-input/source.c'
    rows=[]
    original=C.FLAGS[:]
    profiles=[('base-o2-space','2',False,'2.0/base',True),('base-o3-speed','3',True,'2.0/base',True),('sp1p5-o2-speed','2',True,'2.0/sp1p5',True),('sp1p6-o2-speed','2',True,'2.0/sp1p6',True),('base-o2-speed-sym-off','2',True,'2.0/base',False),('base-o1-speed','1',True,'2.0/base',True)]
    for name,opt,speed,compiler,sym in profiles:
        C.FLAGS=original[:]
        C.FLAGS[C.FLAGS.index('-sym')+1]='on'if sym else'off'
        C.WORK=ROOT/'work/ol904'/name/'compile'
        result,unused=C.compare(source,'ov005',opt,'off',speed,compiler=ROOT/'tools/mwccarm/mwccarm'/compiler/'mwccarm.exe')
        row=dict(profile=name,sourceRows=result)
        rows.append(row)
        if result and not result[0].get('compileFailed'):
            try:
                row['genuineLink']=validate(result[0],qualified_bindings(result[0]),ROOT/'work/ol904'/name/'genuine')
            except ValueError as error:
                if not error.args or not isinstance(error.args[0],dict):
                    raise
                row['genuineLink']=error.args[0]
    C.FLAGS=original
    write_json(ROOT/'evidence/attempts/ov005-controller904-profiles-20261102.json',dict(sourceCredit=0,sourceSha256=sha256(source),source=source.relative_to(ROOT).as_posix(),rows=rows,nativePairedExecutions=0))
    print([(r['profile'],r.get('genuineLink',{}).get('linkedBytes'))for r in rows],flush=True)

if __name__=='__main__':
    execute()
