import hashlib,json,re,subprocess,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
QUEUE=ROOT/'evidence/lanes/save-core/historical-exact95-profile-queue-20261031.json'
OUT=ROOT/'evidence/attempts/save-core-historical-exact95-fresh-20261031.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare():
 data=json.loads((ROOT/'evidence/attempts/save-core-next-profile95-selection-20261031.json').read_text());selected=[];seen=set()
 for row in data['candidates']:
  if row['historicalDiscrepancy']!=0:continue
  if row['address'] in seen:continue
  seen.add(row['address']);row=dict(row);base=ROOT/'nonmatching/save-core/20261031-exact95'/('u'+str(len(selected)).zfill(2));origin=Path(row['sourceOriginRoot']);initial=origin/row['source'];target=base/'a/a/a/a/a/a/a/a'/initial.name;pending=[(initial,target)];closure=[]
  for old,new in pending:
   if not new.resolve().is_relative_to(base.resolve()):raise ValueError('snapshot include escapes isolated input')
   if not old.resolve().is_relative_to(origin.resolve()):raise ValueError('original include escapes repository')
   raw=old.read_bytes();new.parent.mkdir(parents=True,exist_ok=True)
   if new.exists() and new.read_bytes()!=raw:raise ValueError('snapshot is frozen')
   new.write_bytes(raw);closure.append({'path':new.relative_to(ROOT).as_posix(),'sha256':sha(new),'origin':old.relative_to(origin).as_posix()})
   for inc in re.findall(r'^\s*#include\s+"([^"]+)"',raw.decode(),re.M):
    pair=((old.parent/inc).resolve(),(new.parent/inc).resolve())
    if pair not in pending:pending.append(pair)
  if sha(target)!=row['sourceSha256']:raise ValueError('snapshot source differs')
  row['snapshotSource']=target.relative_to(ROOT).as_posix();row['snapshotClosure']=closure;selected.append(row)
  if len(selected)>=32:break
 QUEUE.write_text(json.dumps({'sourceCredit':0,'selection':'Frozen existing historical exact-score source reuse only;current94 accepted intervals excluded;fresh compilation/link and native qualification still mandatory','rows':selected},indent=2)+'\n');return selected
def job(index):
 sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application')]
 import save_core_historical_link_20261031 as B
 from link_runtime_unit import measured_module
 row=json.loads(QUEUE.read_text())['rows'][index];B.MODE=row['mode'];B.ENTRY=int(row['address'],16);B.LENGTH=row['bytes'];B.SOURCE=row['snapshotSource'];B.NAME=row['name'] or 'native_main_'+f'{B.ENTRY:08x}';B.FLAGS=row['flags'];B.COMPILER=row['compilerPath'];B.COMPILER_HASH=row['compilerSha256'];B.WORK='work/sce95/'+f'{B.ENTRY:08x}'
 meta,raw,_=measured_module('main');native=raw[B.ENTRY-0x02000000:B.ENTRY-0x02000000+B.LENGTH]
 try:
  match,body=B.build(native);result={'input':row,'result':match,'linkedBytes':len(body),'sourceCredit':0}
 except Exception as e:result={'input':row,'error':str(e),'compile':B.LAST_COMPILE,'sourceCredit':0}
 p=ROOT/'evidence/attempts'/('save-core-historical-exact95-fresh-20261031-'+f'{B.ENTRY:08x}'+'.json');p.write_text(json.dumps(result,indent=2)+'\n');return p
if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1].isdigit():print(job(int(sys.argv[1])))
 else:
  selected=prepare() if '--snapshot-current' in sys.argv else json.loads(QUEUE.read_text())['rows']
  def run(i):return subprocess.run([sys.executable,str(Path(__file__).resolve()),str(i)],cwd=ROOT,capture_output=True,text=True,timeout=180)
  with ThreadPoolExecutor(max_workers=3) as pool:processes=list(pool.map(run,range(len(selected))))
  results=[]
  for row,p in zip(selected,processes):
   path=ROOT/'evidence/attempts'/('save-core-historical-exact95-fresh-20261031-'+row['address'][2:].zfill(8)+'.json')
   result=json.loads(path.read_text()) if path.exists() else {'input':row,'error':p.stdout+p.stderr,'exitCode':p.returncode,'sourceCredit':0};results.append(result);m=result.get('result',{});print(row['address'],m.get('compiledBytes'),m.get('sameOffsetBytes'),result.get('error','')[:100],flush=True)
  OUT.write_text(json.dumps({'sourceCredit':0,'concurrency':3,'counts':dict(identities=len(results),compiledAndLinked=sum('result' in r for r in results),exactLinked=sum(r.get('result',{}).get('exactByteEqual',False) for r in results),nativeValidated=0),'results':results},indent=2)+'\n')

