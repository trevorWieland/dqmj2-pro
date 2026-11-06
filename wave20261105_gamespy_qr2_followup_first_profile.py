from pathlib import Path
import match_runtime as C
import link_runtime_unit as L
from recover_linked_runtime import qualified_bindings
from project import ROOT,sha256
from wave20261105_gamespy_qr2_followup_first_fixtures import run
from wave20261105_gamespy_qr2_followup_first_models import cases


def prove(row,directory):
    assert row['address']=='0x20b8334';base=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe';assert sha256(base)==C.COMPILER_PINS[base.relative_to(ROOT).as_posix()]
    flags,work=C.FLAGS,C.WORK
    try:
        C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=directory/'base-C';rows,unused=C.compare(ROOT/row['source'],'main','4,p','on,noauto',False,thumb=True,compiler=base)
    finally:C.FLAGS,C.WORK=flags,work
    assert len(rows)==1 and rows[0]['compiledBytes']==64;bad=rows[0];bindings=qualified_bindings(bad);attempts=[];original=L.subprocess.run
    def observe(command,*args,**kwargs):
        p=original(command,*args,**kwargs)
        if command and str(command[0])==str(L.LINKER):attempts.append(dict(command=command,cwd=str(kwargs.get('cwd')),exitCode=p.returncode,stdout=p.stdout,stderr=p.stderr))
        return p
    try:
        L.subprocess.run=observe
        try:L.validate(bad,bindings,directory/'genuine-link')
        except ValueError as e:
            assert e.args and isinstance(e.args[0],dict)and len(attempts)==1 and attempts[0]['exitCode']==0;comparison=e.args[0]
        else:raise ValueError('Wrong base compiler profile unexpectedly matched')
    finally:L.subprocess.run=original
    body=(directory/'genuine-link/caller.bin').read_bytes();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();violations=[]
    for seed,vector in enumerate(cases(0x20b8334)):
        actual=run(image,row,body,vector,seed)
        if not actual['modelPassed']:violations.append(dict(seed=seed,vector=vector,actualReturningModelViolation=actual))
        if len(violations)==4:break
    assert violations
    return dict(status='rejected-wrong-compiler-profile',source=row['source'],sourceSha256=sha256(ROOT/row['source']),correctCompiler=row['compilerPath'],correctCompilerSha256=row['compilerSha256'],wrongCompiler=base.relative_to(ROOT).as_posix(),wrongCompilerSha256=sha256(base),wrongCompiledBytes=64,nativeAndCorrectCompiledBytes=76,object=bad['object'],objectSha256=bad['objectSha256'],originalRelocations=bad['relocations'],genuineLinkAttempt=attempts[0],completeNativeComparison= comparison,actualReturningModelRejections=len(violations),witnesses=violations,observation='Base emits direct Thumb stack-member loads/stores at0x78; sp1p5/original use extra large-offset address construction for len@1400. Same ordinary C input and declared type layout are retained; no object/instruction patches.',sourceOrExecutionCredit=0)
