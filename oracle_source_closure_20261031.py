import argparse
import ast
import hashlib
import json
import re
import subprocess
from project import ROOT,read_json,write_json,sha256
from static_json_reads_20261031 import required_json_reads

EXCLUDED={'build','work','extract','asm','logs','inputs','tools','deps','.git','__pycache__'}
SKIP={'results','vectors','traces','allExecutionResults','allExecutionTraces','rows','cases','allExecutionTraces'}
SEARCH=[ROOT,ROOT/'evidence/application',ROOT/'evidence/encounter',ROOT/'evidence/save',ROOT/'nonmatching/encounter']
EXTENSIONS={'.py','.c','.cpp','.h','.inc','.json','.md','.txt','.s'}


def collect():
    registry=read_json(ROOT/'recovery.json');pending=[];paths={};missing=[];reports=[];seen=set();oracle_reports=set();processed=0;static_reads=set()
    def add(value,parent=ROOT,required=False):
        if not isinstance(value,str) or not 0<len(value)<512 or '\n' in value or '\r' in value or '\0' in value:return
        value=value.replace('\\','/');path=None
        key=(value,str(parent),required)
        if key in seen:return
        seen.add(key)
        if not any(value.lower().endswith(ext) for ext in EXTENSIONS):return
        for base in dict.fromkeys([ROOT,parent,*SEARCH]):
            candidate=(base/value).resolve()
            if not candidate.is_relative_to(ROOT) or candidate.relative_to(ROOT).parts[0] in EXCLUDED:continue
            try:exists=candidate.is_file()
            except OSError:exists=False
            if exists:path=candidate;break
        if path is None:
            if required:missing.append(value)
            return
        if path.suffix.lower() not in EXTENSIONS:return
        relative=path.relative_to(ROOT).as_posix()
        if relative=='evidence/verification/oracle-source-closure-20261031.json' or relative.startswith('evidence/encounter/script-cfg-20261029/'):return
        if relative not in paths:paths[relative]=sha256(path);pending.append(path)
    def walk(value,parent,required_hashes=False):
        if isinstance(value,dict):
            for key,item in value.items():
                if (required_hashes or parent.relative_to(ROOT).parts and parent.relative_to(ROOT).parts[0] in {'nonmatching','config'}) and key in {'path','source','header','profile'} and isinstance(item,str) and any(isinstance(digest,str) and re.fullmatch(r'[0-9a-fA-F]{64}',digest) for label,digest in value.items() if label in {'sha256','sourceSha256','headerSha256','profileSha256'}):
                    candidate=ROOT/item.replace('\\','/')
                    if candidate.resolve().is_relative_to(ROOT) and candidate.relative_to(ROOT).parts[0] not in EXCLUDED:add(item,parent,required=True)
                if key not in SKIP:walk(item,parent,required_hashes)
        elif isinstance(value,list):
            for item in value:walk(item,parent,required_hashes)
        elif isinstance(value,str):add(value,parent)
    for name in ['run_checks.py','configure.py','validate_clean_checkout.py']:
        add(name,required=True)
    interpreted=read_json(ROOT/'interpreted-recovery.json') if (ROOT/'interpreted-recovery.json').is_file() else {}
    batches=[*registry.get('batches',[]),*interpreted.get('batches',[])]
    for oracle in [*registry['oracles'],*batches]:
        for token in oracle['reproduce']:
            if isinstance(token,str) and token.endswith('.py'):add(token,required=True)
        report=oracle['report'];reports.append(report);oracle_reports.add(report.replace('\\','/'));add(report,required=True)
        for relative in oracle.get('sourceHashes',{}):
            if relative.replace('\\','/').split('/')[0] not in EXCLUDED:add(relative,required=True)
    while pending:
        path=pending.pop();processed+=1
        if processed%250==0:print({'processed':processed,'discovered':len(paths),'pending':len(pending)},flush=True)
        if path.suffix=='.py':
            tree=ast.parse(path.read_text(encoding='utf-8-sig'))
            for relative in required_json_reads(tree,ROOT):
                if relative.split('/')[0] not in EXCLUDED:
                    newly_required=relative not in static_reads
                    static_reads.add(relative);add(relative,path.parent,required=True)
                    if newly_required and relative in paths and ROOT/relative not in pending:pending.append(ROOT/relative)
            for node in ast.walk(tree):
                modules=[x.name for x in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
                for name in modules:add(name.replace('.','/')+'.py',path.parent)
                if isinstance(node,ast.Constant) and isinstance(node.value,str):
                    value=node.value
                    if value.endswith(tuple(EXTENSIONS)):add(value,path.parent)
                    elif re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*',value):add(value.replace('.','/')+'.py',path.parent)
        elif path.suffix=='.json' and (path.relative_to(ROOT).as_posix() in oracle_reports|static_reads or path.relative_to(ROOT).parts[0] in {'nonmatching','config','provenance'}):
            try:document=read_json(path)
            except (ValueError,UnicodeError):continue
            pinned_files=path.relative_to(ROOT).as_posix() in static_reads and path.relative_to(ROOT).parts[0]!='provenance' and isinstance(document,dict) and isinstance(document.get('files'),list)
            walk(document,path.parent,pinned_files)
        elif path.suffix in ['.c','.cpp','.h','.inc']:
            for include in re.findall(r'^\s*#include\s+"([^"]+)"',path.read_text(encoding='utf-8-sig'),re.M):add(include,path.parent)
    return {'schemaVersion':2,'sourceCredit':0,'registrySha256':sha256(ROOT/'recovery.json'),'oracleCount':len(registry['oracles']),'registeredBatchCount':len(batches),'oracleReports':[row['report']for row in registry['oracles']],'registeredReports':reports,'staticJsonReads':sorted(static_reads),'sourceAndEvidenceHashes':dict(sorted(paths.items())),'missingRequiredPaths':sorted(set(missing)),
        'scope':'Native/interpreted batch and oracle commands/reports/source hashes, recursively resolved imports, static JSON reads, immutable pin files, nonmatching/config/provenance JSON inputs and quoted C includes','limitations':['Static discovery cannot prove dynamically constructed runtime inputs; clean execution remains required','Unreferenced historical evidence JSON is not recursively expanded','This does not replace accepted source hash checks, input/tool pins, current-product gates or fresh full-suite execution']}


def verify_commit(report):
    revision=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    names=sorted(report['sourceAndEvidenceHashes']);query=''.join(revision+':'+name+'\n' for name in names).encode()
    output=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=query,capture_output=True,check=True).stdout;offset=0;missing=[];changed=[]
    for name in names:
        end=output.index(b'\n',offset);header=output[offset:end].decode();offset=end+1
        if header.endswith(' missing'):missing.append(name);continue
        oid,kind,length=header.split();length=int(length);assert kind=='blob';payload=output[offset:offset+length];offset+=length+1
        if hashlib.sha256(payload).hexdigest()!=report['sourceAndEvidenceHashes'][name]:changed.append(name)
    assert offset==len(output)
    return {'commit':revision,'pathsChecked':len(names),'missingCommittedPaths':missing,'changedCommittedPaths':changed,'passed':not missing and not changed and not report['missingRequiredPaths']}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',action='store_true');parser.add_argument('--verify-commit',action='store_true');args=parser.parse_args()
    report=collect();output=ROOT/'evidence/verification/oracle-source-closure-20261031.json'
    if args.stage:
        names=sorted(report['sourceAndEvidenceHashes']);subprocess.run(['git','add','--pathspec-from-file=-','--pathspec-file-nul'],cwd=ROOT,input=b''.join(name.encode()+b'\0' for name in names),check=True)
    if args.verify_commit:report['committedVerification']=verify_commit(report)
    write_json(output,report)
    print({'oracles':report['oracleCount'],'discoveredPaths':len(report['sourceAndEvidenceHashes']),'missingRequired':report['missingRequiredPaths'],'staged':args.stage,'committed':report.get('committedVerification',{}).get('passed')})
    assert not report['missingRequiredPaths']
    if args.verify_commit:assert report['committedVerification']['passed'],report['committedVerification']


if __name__=='__main__':
    main()
