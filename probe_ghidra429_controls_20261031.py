import json
import subprocess
from project import ROOT,write_json,sha256

def run():
    baseline=ROOT/'evidence/verification/ghidra429-independent-frontend-20261031.json';report=json.loads(baseline.read_text());command=report['records'][0]['command'];index=command.index('-postScript');results=[]
    for name,program,module,reason in[('overlapping-program','ov001.bin','ov000','429 module identity differs'),('load-base','ov000.bin','main','429 module base differs')]:
        output=ROOT/'build/ghidra429/controls'/name;output.mkdir(parents=True,exist_ok=True)
        if(output/'export.json').exists():raise ValueError('429 stale negative export rejected')
        args=command[:];args[args.index('-process')+1]=program;args[index+2]=module;args[index+4]=str(output);args[args.index('-log')+1]=str(output/'headless.log');args[args.index('-scriptlog')+1]=str(output/'script.log')
        result=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,timeout=120);(output/'stdout.txt').write_text(result.stdout,encoding='utf-8');(output/'stderr.txt').write_text(result.stderr,encoding='utf-8');text=result.stdout+result.stderr
        if reason not in text or(output/'export.json').exists():raise ValueError(('429 expected identity control was not rejected',name,result.returncode,text[-3000:]))
        results.append(dict(name=name,command=args,returncode=result.returncode,requiredMessage=reason,rejectedBeforeDecompilation=True,exportProduced=False,stdoutSha256=sha256(output/'stdout.txt'),stderrSha256=sha256(output/'stderr.txt')))
    write_json(ROOT/'evidence/verification/ghidra429-identity-controls-20261031.json',dict(schemaVersion=1,sourceCredit=0,nativeExecutions=0,baselineReportSha256=sha256(baseline),generatorSha256=sha256(__file__),controls=results,reproductionCommand='python probe_ghidra429_controls_20261031.py',limits=['Ghidra headless can return0 after a script exception; explicit required failure message and absent export determine rejection','Only copied private project is opened read-only; no source/prototype adoption']))
    print(json.dumps(dict(identityControls=len(results),sourceCredit=0)))

if __name__=='__main__':run()
