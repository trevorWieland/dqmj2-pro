import re

from project import ROOT, read_json, write_json, sha256

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/battle-fifth'
SOURCE = ROOT / 'src/ov001/parallel_wave20261102/battle-fifth'
SELECTED = ['021dda80','021de254','021de40c','021de644','021de984','021dee18','021df680','021dfd74','021dff00','021e08e4']


def main():
    rows = [__import__('json').loads(line)for line in(ROOT/'ledger/functions.jsonl').read_text().splitlines()]
    candidates = {format(int(row['address'],0),'08x'):row for row in rows if row['module']=='ov001'and row['processor']=='arm9'and not row.get('program')}
    exclusions = '\n'.join(path.read_text()for path in ROOT.glob('cohort1[45][7890]*specification.json'))
    claims = []
    for path in(ROOT/'evidence/lanes/parallel-wave20261102').rglob('claim.json'):
        value = read_json(path)
        for row in value.get('claimedFunctions',value.get('functions',[])):
            if row.get('module',value.get('module'))=='ov001'and row.get('processor',value.get('processor','arm9'))=='arm9'and not row.get('program',value.get('program')):
                start = int(row['address'],0)
                claims.append((start,start+int(row.get('bytes',row.get('size',0))),str(path)))
    selected = []
    for address in SELECTED:
        row = candidates[address]
        if row['states']['functionMatched']or row['id']in exclusions:
            raise ValueError(('Accepted or pending',address))
        start = int(row['address'],0)
        if any(start<b and a<start+row['bytes']for a,b,path in claims):
            raise ValueError(('Another claimed interval',address))
        broad = ROOT/f'nonmatching/ov001/20261029-broad01/native_ov001_{address}.c'
        draft = ROOT/f'nonmatching/overlay-lane/20261102-sequential844/{address}/source.c'
        if not draft.exists():
            draft = ROOT/f'nonmatching/overlay-lane/20261102-battle816/{address}/strong/source.c'
        if address=='021dee18':
            draft = ROOT/'nonmatching/ov001/20261030-turn-controller01/021dee18/measured-sequential-state-chain-1.c'
        if not draft.exists():
            draft = broad
        text = draft.read_text()
        if text.startswith('#include "context.h"'):
            header = draft.with_name('context.h').read_text()
        else:
            match = re.search(r'^(?:u32|s32|int|void|u8|s8) native_ov001_'+address+r'\(',text,re.M)
            if not match:
                raise ValueError(('Standalone draft shape',str(draft)))
            header,text = text[:match.start()],'#include "context.h"\n'+text[match.start():]
        directory = SOURCE/address
        directory.mkdir(parents=True,exist_ok=True)
        target = directory/f'native_ov001_{address}.c'
        target.write_text(text)
        target.with_name('context.h').write_text(header)
        selected.append({key:row[key]for key in ['id','processor','module','mode','address','bytes','inputModuleSha256','inputBytesSha256']}|dict(program='',sourceTarget=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),headerSha256=sha256(target.with_name('context.h')),draft=draft.relative_to(ROOT).as_posix(),draftSha256=sha256(draft)))
    LANE.mkdir(parents=True,exist_ok=True)
    write_json(LANE/'claim.json',dict(schemaVersion=1,owner='ds_tooling_research/battle-fifth',acceptedBaselineCohort=148,module='ov001',processor='arm9',program='',sourceRoot=SOURCE.relative_to(ROOT).as_posix(),workRoot='work/parallel-wave20261102/battle-fifth',sourceCredit=0,claimedFunctions=selected,nativeOpportunityBytes=sum(row['bytes']for row in selected),scope='Battle state/controller family surrounding accepted628-byte021e00b4; signed-byte phases, word actor pointers and complete measured callee input interfaces remain explicit hypotheses until compiled/link/behavior proof'))
    print(dict(functions=len(selected),bytes=sum(row['bytes']for row in selected),claimSha256=sha256(LANE/'claim.json')))


if __name__=='__main__':
    main()
