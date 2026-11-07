import match_runtime
import bisect
import hashlib
import json
import re
import subprocess
from elftools.elf.elffile import ELFFile
from project import ROOT,read_json,write_json,sha256

REV='0da3da2f2eaf3888774e1d2f0cd572c6db3e2cfb'
LANE=ROOT/'evidence/lanes/parallel-wave20261106/nns-primary-scout'


def blob(path):return subprocess.check_output(['git','show',REV+':'+path],cwd=ROOT)


def intervals(node,parent=None):
    parent=parent or{}
    if isinstance(node,list):
        for item in node:yield from intervals(item,parent)
    elif isinstance(node,dict):
        context={k:node.get(k)or parent.get(k)for k in['program','processor','module']};module=context['module'];size=node.get('storedBytes',node.get('bytes',node.get('size')))
        if module and node.get('address')is not None and size:
            try:a=int(node['address'],0)if isinstance(node['address'],str)else node['address'];n=int(size,0)if isinstance(size,str)else size
            except(ValueError,TypeError):pass
            else:
                if type(n)is int and n>0:yield(context['program']or('dwc/utility.bin/move/child.srl'if module.startswith('utility-child-')else''),context['processor']or('arm7'if'arm7'in module else'arm9'),module,a,a+n)
        for value in node.values():yield from intervals(value,context)


def masked(data,offsets):
    body=bytearray(data)
    for offset in offsets:
        if not 0<=offset<=len(body)-4:raise ValueError('Declared relocation escaped whole span')
        body[offset:offset+4]=bytes(4)
    return hashlib.sha256(body).hexdigest()


def main():
    if LANE.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/nns-primary-scout').resolve():raise ValueError('Exact read-only source/evidence scope differs')
    raw=blob('ledger/functions.jsonl');rows=[json.loads(line)for line in raw.splitlines()];manifest_raw=blob('manifest.json');modules={(m.get('program')or'',m['processor'],m['name']):m for m in json.loads(manifest_raw)['modules']};pins={};gitpins={};protect=[]
    def pin(path):
        h=sha256(ROOT/path)
        if path in pins and pins[path]!=h:raise ValueError('Input changed while reading')
        pins[path]=h;return h
    protected_paths=sorted(set((ROOT/'evidence/lanes').rglob('claim.json'))|set((ROOT/'evidence/lanes').rglob('data-claim.json'))|set(ROOT.glob('cohort*-*specification.json')))
    for path in protected_paths:
        name=path.relative_to(ROOT).as_posix();pin(name);protect.extend((*r,name)for r in intervals(read_json(path)))
    for path,key in[('ledger/data.json','records'),('ledger/linkage.json','regions')]:
        content=blob(path);gitpins[REV+':'+path]=hashlib.sha256(content).hexdigest();protect.extend((*r,REV+':'+path)for r in intervals(json.loads(content)[key]))
    protect.extend((*r,REV+':ledger/functions.jsonl')for row in rows if row['states']['functionMatched']or row.get('sourceUnit')for r in intervals(row));groups={}
    for program,cpu,module,a,b,origin in protect:groups.setdefault((program,cpu,module),[]).append((a,b,origin))
    native={};targets={};eligible=[];blocked=[]
    for row in rows:
        if row['processor']!='arm9'or row['mode']!='arm'or row['states']['functionMatched']or not row.get('bytes')or row['bytes']<128:continue
        ns=(row.get('program')or'',row['processor'],row['module']);m=modules[ns]
        if ns not in native:
            pin(m['binary']);image=(ROOT/m['binary']).read_bytes()
            if hashlib.sha256(image).hexdigest()!=m['sha256']:raise ValueError('Pinned original native module differs')
            sym=m.get('symbolsFile')or('config/arm9/symbols.txt'if row['module']=='main'else'config/'+row['module']+'/symbols.txt');rel=str((ROOT/sym).with_name('relocs.txt').relative_to(ROOT).as_posix())
            if not(ROOT/rel).exists():native[ns]=None;continue
            pin(sym);pin(rel);records=[]
            for line in(ROOT/rel).read_text(encoding='utf-8').splitlines():
                found=re.match(r'from:(0x[0-9a-f]+) kind:(\S+)',line)
                if found:records.append((int(found[1],0),found[2],line))
            records.sort();native[ns]=(image,records,[r[0]for r in records])
        if native[ns]is None:continue
        image,records,addresses=native[ns];a=int(row['address'],0);n=row['bytes'];offset=a-int(m['base'],0);body=image[offset:offset+n]
        if len(body)!=n:raise ValueError('Configured whole function escaped original module')
        outgoing=records[bisect.bisect_left(addresses,a):bisect.bisect_left(addresses,a+n)];offsets=tuple(r[0]-a for r in outgoing)
        if any(not 0<=i<=n-4 for i in offsets):continue
        conflicts=[dict(start=hex(x),end=hex(y),path=p)for x,y,p in groups.get(ns,[])if max(x,a)<min(y,a+n)]
        record=dict(identity=row,originalRelocationRecords=[r[2]for r in outgoing],physicalConflicts=conflicts)
        targets.setdefault((n,offsets,masked(body,offsets)),[]).append(record);(blocked if conflicts else eligible).append(record)
    objects=[];found=[];span_count=0
    roots=[ROOT/'work/main-nitrosystem-breadth-20261101',ROOT/'work/main-nitrosdk-breadth-20261102']
    for path in sorted(p for root in roots for p in root.rglob('compiled.o')):
        slug=path.relative_to(path.parents[1]).as_posix()if len(path.parents)>1 else path.name
        if not any(k in str(path).lower()for k in['g3d','g2d','fx-src-fx','gx-src-g3','gx-src-gx_load']):continue
        relative=path.relative_to(ROOT).as_posix();digest=pin(relative);objects.append(dict(path=relative,sha256=digest))
        with path.open('rb')as stream:
            elf=ELFFile(stream);table=elf.get_section_by_name('.symtab');rels={}
            for section in elf.iter_sections():
                if section['sh_type']in['SHT_REL','SHT_RELA']:rels.setdefault(section['sh_info'],[]).extend(r['r_offset']for r in section.iter_relocations())
            for symbol in table.iter_symbols():
                if symbol['st_info']['type']!='STT_FUNC'or not isinstance(symbol['st_shndx'],int)or symbol['st_size']<128 or symbol['st_value']&1:continue
                span_count+=1;start=symbol['st_value'];size=symbol['st_size'];body=elf.get_section(symbol['st_shndx']).data()[start:start+size];offsets=tuple(sorted(at-start for at in rels.get(symbol['st_shndx'],[])if start<=at<start+size))
                for target in targets.get((len(body),offsets,masked(body,offsets)),[]):found.append(dict(**target,referenceFunction=symbol.name,referenceObject=relative,referenceObjectSha256=digest,maskedWholeBodySha256=masked(body,offsets),originUsedAsCompilerOrLinkInput=False,sourceCredit=0,boundaryOrInterfaceProven=False))
    final_paths={p.relative_to(ROOT).as_posix()for p in set((ROOT/'evidence/lanes').rglob('claim.json'))|set((ROOT/'evidence/lanes').rglob('data-claim.json'))|set(ROOT.glob('cohort*-*specification.json'))};initial_paths={p.relative_to(ROOT).as_posix()for p in protected_paths};changed=[p for p,h in pins.items()if not(ROOT/p).is_file()or sha256(ROOT/p)!=h]
    if changed or final_paths!=initial_paths:
        write_json(LANE/'failed-changing-epoch.json',dict(status='failed-changing-protection-or-source-epoch',changed=changed,newPaths=sorted(final_paths-initial_paths),removedPaths=sorted(initial_paths-final_paths),sourceCredit=0));raise ValueError('Fresh protection epoch changed')
    output=dict(status='passed-read-only-existing-primary-object-correspondence',sourceRevision=REV,sourceCredit=0,sourceOwnershipGranted=False,compilerInvoked=False,reconstructionSourceWrites=False,ledgerSha256=hashlib.sha256(raw).hexdigest(),manifestSha256=hashlib.sha256(manifest_raw).hexdigest(),eligibleUnclaimedWholeArmFunctions=len(eligible),reservedOrAcceptedDataOverlapWholeArmFunctions=len(blocked),existingReferenceObjects=objects,existingReferenceFunctionSpans=span_count,matches=found,actualInputPins=[dict(path=p,sha256=h)for p,h in sorted(pins.items())],gitPins=[dict(gitObject=p,sha256=h)for p,h in sorted(gitpins.items())],generatorSha256=sha256(__file__),limits=['Only existing primary-generated object metadata is read; no object is a reconstruction compiler/link/runtime input.','Whole masked body/relocation sequence only supplies source/version correspondence hypothesis; no boundary,ABI,mode,flow,literal or cross-overlay proof.','Every current/historical claim and all cohort specifications remain protected; inactive matches require exact Root resumption admission.'])
    write_json(LANE/'existing-primary-object-census.json',output);print(dict(eligible=len(eligible),reserved=len(blocked),objects=len(objects),referenceSpans=span_count,matches=len(found),unclaimedMatches=sum(not r['physicalConflicts']for r in found)),flush=True)


if __name__=='__main__':main()
