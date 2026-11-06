import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from project import ROOT,write_json,sha256
import match_runtime as C
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

def execute():
    source=ROOT/'nonmatching/overlay-lane/20261102-template940/ordinary-c/source.c'
    rows=[]
    for name,compiler,opt,speed in [('base-o2-space','2.0/base','2',False),('base-o3-speed','2.0/base','3',True),('sp1p5-o2-speed','2.0/sp1p5','2',True),('sp1p6-o2-speed','2.0/sp1p6','2',True),('v12-o2-speed','1.2/base','2',True)]:
        executable=ROOT/'tools/mwccarm/mwccarm'/compiler/'mwccarm.exe'
        C.WORK=ROOT/'work/ol943'/name/'compile'
        row=dict(profile=name,compiler=dict(path=executable.relative_to(ROOT).as_posix(),sha256=sha256(executable)),optimization=opt,speed=speed)
        rows.append(row)
        try:results,unused=C.compare(source,'ov001',opt,'off',speed,compiler=executable)
        except Exception as error:
            row['unqualifiedCompilerBindingFailure']=dict(type=type(error).__name__,message=str(error))
            continue
        row['sourceRows']=results
        if results and not results[0].get('compileFailed'):
            try:row['genuineLink']=validate(results[0],qualified_bindings(results[0]),ROOT/'work/ol943'/name/'genuine')
            except ValueError as error:
                if not error.args or not isinstance(error.args[0],dict):raise
                row['genuineLink']=error.args[0]
    write_json(ROOT/'evidence/attempts/ov001-template943-compiler-groups-20261102.json',dict(sourceCredit=0,source=dict(path=source.relative_to(ROOT).as_posix(),sha256=sha256(source)),rows=rows,nativePairedExecutions=0,limits=['Compiler-helper relocation-site failures are preserved as unqualified bindings, not silently rebound to a guessed runtime entry.','Other compiler profiles are byte experiments only; none are accepted as functional by this profile probe.']))
    print(dict(profiles=len(rows),genuineLinks=sum('genuineLink'in r for r in rows),exactMatches=sum(bool(r.get('genuineLink',{}).get('exactCallerBytes'))for r in rows),sourceCredit=0))

if __name__=='__main__':execute()
