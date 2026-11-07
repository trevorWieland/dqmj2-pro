import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from project import ROOT,read_json,write_json,sha256

LANE=ROOT/'evidence/lanes/parallel-wave20261107/resource-path-api-audit'
TARGETS={0x0202a8e0,0x0203cc3c}
FIELDS=('id','program','processor','module','mode','address','bytes','inputModuleSha256','inputBytesSha256','sourceUnit','sourceSha256','sourceDependencies','object','objectSha256','compilerSha256','compilerFlags','dependencies','evidence')


def target(d):
    value=d.get('targetAddress',d.get('target'))
    try:return int(value,0)if isinstance(value,str)else int(value)
    except (TypeError,ValueError):
        match=re.search(r'_([0-9a-f]{8})$',str(value),re.I)
        return int(match[1],16)if match else None


def reachable(source):
    paths=set();pending=[ROOT/source]
    while pending:
        path=pending.pop().resolve()
        if not path.is_relative_to(ROOT):raise ValueError('Source include escaped repository')
        name=path.relative_to(ROOT).as_posix()
        if name in paths:continue
        paths.add(name)
        for inc in re.findall(r'^\s*#\s*include\s*"([^"\n]+)"',path.read_text(encoding='utf-8-sig'),re.M):pending.append(path.parent/inc)
    return paths


def main():
    raw=(ROOT/'ledger/functions.jsonl').read_bytes();ledger=[json.loads(line)for line in raw.splitlines()]
    selected=[r for r in ledger if r['states']['functionMatched']]
    providers=[r for r in selected if not r.get('program')and r['processor']=='arm9'and r['module']=='main'and int(r['address'],0)in TARGETS]
    if len(providers)!=2:raise ValueError('Both canonical APIs must be selected accepted source')
    accepted173=read_json(ROOT/'evidence/verification/accepted-cohort173-identities-v2-20261101.json')
    baseline={(r.get('program')or'',r['processor'],r['module'],r['mode'],int(r['address'],0)if isinstance(r['address'],str)else r['address'])for r in accepted173['functions']}
    normalize=lambda r:((r.get('program')or''),r['processor'],r['module'],r['mode'],int(r['address'],0))
    users=defaultdict(list);paths={};calls=[];aliases={'native_fn_0202a8e0','native_main_0202a8e0','func_0202a8e0','native_fn_0203cc3c','native_main_0203cc3c','func_0203cc3c'}
    for r in selected:
        if sha256(ROOT/r['sourceUnit'])!=r['sourceSha256']:raise ValueError('Selected source changed during ABI audit')
        for d in r.get('sourceDependencies')or[]:
            if sha256(ROOT/d['path'])!=d['sha256']:raise ValueError('Selected source dependency changed')
        closure=reachable(r['sourceUnit'])|{d['path']for d in r.get('sourceDependencies')or[]}
        for p in closure:users[p].append(r);paths[p]=sha256(ROOT/p)
        if r.get('program')or r['processor']!='arm9':continue
        deps=[d for d in r.get('dependencies')or[]if target(d)in TARGETS]
        if deps:
            aliases.update(d['symbol']for d in deps)
            calls.append(dict(identity={k:r.get(k)for k in FIELDS},apiRelocations=deps,accepted173=normalize(r)in baseline))
    pattern=re.compile('|'.join(re.escape(s)for s in sorted(aliases,key=len,reverse=True)),re.I)
    provider_files=[];text_occurrences=[];affected={r['id']:r for r in providers};globals_affected={};selected_api_paths=set()
    for p in sorted(paths):
        lines=(ROOT/p).read_text(encoding='utf-8-sig').splitlines()
        hits=[dict(line=i+1,text=line)for i,line in enumerate(lines)if pattern.search(line)]
        if hits:
            selected_api_paths.add(p)
            entry=dict(path=p,sha256=paths[p],occurrences=hits,selectedConsumers=[r['id']for r in users[p]])
            text_occurrences.append(entry)
            declarations=[h for h in hits if re.match(r'^\s*(?:extern\s+)?(?:u32|s32|int|void|unsigned|const|char|u8|BOOL)\b',h['text'])and re.search(r'\b(?:native_(?:fn|main)_|func_)(?:0202a8e0|0203cc3c)\s*\(',h['text'])]
            if declarations:
                provider_files.append(dict(entry,declarations=declarations))
                affected.update((r['id'],r)for r in users[p])
        if any('native_data_020edec8'in line for line in lines):
            for r in users[p]:globals_affected[r['id']]=r
    affected.update((r['identity']['id'],next(x for x in selected if x['id']==r['identity']['id']))for r in calls)
    all_source_hits=[]
    for path in sorted((ROOT/'src').rglob('*')):
        if not path.is_file()or path.suffix.lower()not in('.c','.cpp','.h','.hpp','.cc','.cxx'):continue
        hits=[dict(line=i+1,text=line)for i,line in enumerate(path.read_text(encoding='utf-8-sig').splitlines())if re.search('(?:0202a8e0|0203cc3c)',line,re.I)]
        if hits:all_source_hits.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path),occurrences=hits,selected=path.relative_to(ROOT).as_posix()in paths))
    inventory=[]
    for r in sorted(affected.values(),key=lambda r:r['id']):
        item={k:r.get(k)for k in FIELDS};item.update(accepted173=normalize(r)in baseline,reportSha256=sha256(ROOT/r['evidence']),originalContainerAvailable=(ROOT/r['object']).exists())
        if item['originalContainerAvailable']and sha256(ROOT/r['object'])!=r['objectSha256']:raise ValueError('Selected reference object changed')
        inventory.append(item)
    downstream=[]
    for address in[0x0200bfe4,0x0203cb8c]:
        r=next(r for r in selected if not r.get('program')and r['processor']=='arm9'and r['module']=='main'and int(r['address'],0)==address)
        downstream.append(dict(identity={k:r.get(k)for k in FIELDS},sourceSignature=[line for line in(ROOT/r['sourceUnit']).read_text().splitlines()if re.search(r'\bnative_main_'+f'{address:08x}'+r'\s*\(',line)]))
    registered_pending=[];registry=read_json(ROOT/'recovery.json')
    selected_keys={normalize(r)for r in selected}
    for batch in registry['batches']:
        document=read_json(ROOT/batch['report']);entries=document.get('functionMatches',document.get('matches',document.get('functions',[])))
        if isinstance(entries,int):entries=document.get('matches',[])
        for row in entries:
            value={**document,**row}
            if value.get('program')or value.get('processor','arm9')!='arm9' or not value.get('address')or value.get('mode')not in('arm','thumb'):continue
            deps=[d for d in row.get('relocations',[])if target(d)in TARGETS]
            if deps and normalize(value)not in selected_keys:registered_pending.append(dict(report=batch['report'],reportSha256=sha256(ROOT/batch['report']),identity={k:value.get(k)for k in('program','processor','module','mode','address','bytes','source','sourceSha256')},apiRelocations=deps))
    source_hits={r['path']for r in all_source_hits};ready_source_uses=[]
    ready_paths=sorted((ROOT/'evidence').rglob('*ready*.json'))
    def referenced(value):
        if isinstance(value,dict):
            for k,v in value.items():
                if k in('source','sourceUnit','path')and isinstance(v,str)and v in source_hits:yield v
                yield from referenced(v)
        elif isinstance(value,list):
            for v in value:yield from referenced(v)
    for path in ready_paths:
        uses=sorted(set(referenced(read_json(path))))
        if uses:ready_source_uses.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path),apiSourceOrHeaderFiles=uses))
    if(ROOT/'ledger/functions.jsonl').read_bytes()!=raw:raise ValueError('Selection changed during pointer API audit')
    specification=read_json(ROOT/'cohort174-parallel-wave20261105-s-specification.json')
    prepared_keys={normalize(r)for r in specification['expectedAdditions']+specification['migrations']}
    prepared_inventory=[r for r in inventory if not r['accepted173']]
    if any(normalize(r)not in prepared_keys for r in prepared_inventory):raise ValueError('Unaccepted selection is outside frozen174')
    counts=dict(currentSelectedFunctionRows=len(selected),accepted173Functions=len(baseline),selectedActualCallerFunctions=len(calls),actualAccepted173CallerFunctions=sum(r['accepted173']for r in calls),selectedDeclarationProviderFiles=len(provider_files),minimumAffectedSelectedFunctions=len(inventory),affectedAccepted173=sum(r['accepted173']for r in inventory),affectedAccepted173Bytes=sum(r['bytes']for r in inventory if r['accepted173']),affectedPrepared174Functions=len(prepared_inventory),affectedPrepared174Bytes=sum(r['bytes']for r in prepared_inventory),affectedBytes=sum(r['bytes']for r in inventory),fileStatusGlobalConsumers=len(globals_affected))
    audit=dict(schemaVersion=1,status='read-only-pointer-API-scope-no-migration-authorized',sourceCredit=0,ledgerSha256=hashlib.sha256(raw).hexdigest(),baseline173=dict(path='evidence/verification/accepted-cohort173-identities-v2-20261101.json',sha256=sha256(ROOT/'evidence/verification/accepted-cohort173-identities-v2-20261101.json')),canonicalProviders=[{k:r.get(k)for k in FIELDS}for r in providers],counts=counts,actualCallers=calls,declarationProviderFiles=provider_files,minimumMigrationInventory=inventory,selectedSourceOccurrences=text_occurrences,allAuthoredSourceOccurrences=all_source_hits,aliases=sorted(aliases),fileStatusGlobalConsumers=[{k:r.get(k)for k in FIELDS}for r in globals_affected.values()],downstreamAcceptedInterfaces=downstream,consumedLayouts=['0202a8e0 saves the complete incomingR0 word as path, passes it to0200bfe4, owns an18-word/72B stack file record, subtracts word9/top(+36) from word10/bottom(+40), and writes status0/nonzero,3/empty,1/open-failure to020edec8.','0200bfe4 is already selected as BOOL(FSFile*,constchar*). The size wrapper header currentlydeclares(void*,u32), an inherited nominal/type-boundary conflict beyond the two top-level signatures.','0203cc3c forwards incomingR0 path andR1 heap unchanged, forcesR2 selector1 and tail-jumps to0203cb8c. No path bytes are dereferenced by the16B wrapper itself.','0203cb8c/160B is selected as u32(u32path,u32heap,u32selector), asks0202a8e0 forsize, rounds allocation size to4B, chooses alignment+4/-4, passes path to0202a818 and returns an owned buffer word or0.','Resource700 caller fixtures use32B filename buffers with measured signed%02d formats, actual formatter44B/native file-size116B/archive wrapper16B and explicit backend interfaces. Backend path-byte consumption is bounded service evidence, not a fresh original filesystem closure.'],proposedCanonicalOptions=[dict(type='u32(const void *path) and u32(const void *path,u32 heap)',assessment='Accepts existing signed/unsigned byte filename views without nominal char conflicts; requires every selected declaration and emitted caller to migrate consistently, plus explicit reviewed casts at remaining canonical word boundaries.'),dict(type='u32(const char *path) and u32(const char *path,u32 heap)',assessment='Matches the downstream SDK path convention, but unsigned byte format buffers require a reviewed char view. Typedef/layout/header compatibility and every existing source contract remain mandatory.')],requiredBeforeViews=['Coordinator must select one canonical type and exact atomic scope; caller-only aliases incompatible with accepted word definitions are not allowed.','Preserve all selected source/header/report/object references and all700B/656B/232B working packets; source views must be additive in a new admitted root.','Inventory is a minimum function/prototype closure. Any shared-header consumer belongs in the migration even if its function emits no call; multi-function source TUs must remain whole.','Prove every previously accepted allocated section/symbol/raw relocation and full native byte span unchanged, with proper-prototype negative controls and an input-only independent replay.','Pointer arguments may change address CSE in already matching callers. Any changed allocated code blocks a zero-credit migration; do not restore it through casts, wrappers, profile/register searches or object patches.','Downstream SDK FSFile/char-path declarations and the word path APIs0203cb8c/0202a818 require an explicit source-boundary decision; no claim to repair whole-program ISO C typing follows from two signatures.'],limits=['No pointer API source view was authored or compiled.','All selected source closures were searched, including dormant declaration providers. Unselected/working source occurrences are separately listed and remain unadopted.','No registry, preference, accepted header/source, frozen packet or Git state changed.'],producer=Path(__file__).name,producerSha256=sha256(__file__))
    audit['currentRegistryAudit']=dict(path='recovery.json',sha256=sha256(ROOT/'recovery.json'),batches=len(registry['batches']),additionalUnselectedApiCallers=registered_pending)
    audit['globalReadyAudit']=dict(filesScanned=len(ready_paths),apiSourceUses=ready_source_uses)
    audit['frozen174']=dict(path='cohort174-parallel-wave20261105-s-specification.json',sha256=sha256(ROOT/'cohort174-parallel-wave20261105-s-specification.json'))
    audit['prepared174MigrationInventory']=prepared_inventory
    audit['proposedViewRoot']='src/runtime/goal_resume20261107/resource_path_api/'
    audit['proposedPathMapping']='Mirror each affected original src-relative path beneath the proposed root, preserving quoted-include structure and file basenames. Add one declaration-only canonical API header after coordinator type/scope approval; do not rewrite any existing source/header.'
    audit['proposedSourceViewsCreated']=False
    write_json(LANE/'audit.json',audit)
    print(json.dumps(dict(audit=(LANE/'audit.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'audit.json'),counts=counts)))


if __name__=='__main__':main()
