import concurrent.futures
import re
from project import ROOT,read_json,write_json,sha256,now
from native_global_width_contexts_20261031 import apply,preserve_declarations
from draft_main_breadth_lane_20261030 import options

WORK=ROOT/'work/main-global-width-pair-20261031'
REPORT=ROOT/'evidence/attempts/main-global-width-pair-20261031.json'


def worker(spec):
    import draft_runtime as unit
    import match_runtime as compiler
    from generated_word_type_hypotheses_20261031 import install
    context,contracts,rejected=apply(spec['context'],spec['assembly'])
    address=int(spec['address'],0)
    unit.WORK=WORK/f'{spec["mode"]}-{address:08x}'
    unit.OPTIONS=options();unit.OPTIONS.thumb=spec['mode']=='thumb';unit.OPTIONS.compiler_variants=True
    compiler.WORK=unit.WORK/'compile'
    unit.FUNCTION_INPUTS={spec['name']:(spec['assembly'],context)}
    unit.FUNCTION_ADDRESSES={spec['name']:f'{address:08x}'}
    unit.SOURCE_RETURNS=spec['sourceReturns']
    if not hasattr(unit,'_global_width_base'):
        install(unit)
        unit._global_width_base=unit.source_text
    unit.source_text=lambda draft,original:preserve_declarations(unit._global_width_base(draft,original),contracts)
    row=unit.one(spec['name'])
    attempts=row.get('attempts',[])
    compiled=[item for item in attempts if item.get('compiledBytes')]
    best=max(compiled,key=lambda item:item.get('matchingBytes',0),default={})
    row.update(module='main',processor='arm9',mode=spec['mode'],address=spec['address'],bytes=spec['bytes'],sourceCredit=0,
        accepted=False,generatedHypothesis=True,qualifiedGlobalObjectExtent=False,priorEvidence=spec['priorEvidence'],
        priorBestMatchingBytes=spec['priorBestMatchingBytes'],priorCompilable=spec['priorCompilable'],
        globalWidthHypotheses=contracts,rejectedGlobalWidthCandidates=rejected,inputHashes=spec['inputHashes'],
        compilable=bool(compiled),compilerExact=any(item.get('exactAfterDeclaredRelocation') for item in attempts),
        bestSameOffsetBytes=best.get('matchingBytes',0))
    return row


def queue():
    result=[];seen=set()
    for stem in ['main-expanded-breadth12-20261031','main-large-breadth13-20261031']:
        path=ROOT/f'evidence/attempts/{stem}.json'
        for previous in read_json(path)['results']:
            if not previous.get('draftSource') or previous['mode']!='arm':continue
            address=int(previous['address'],0)
            identity=(previous['mode'],address)
            if identity in seen:continue
            source=ROOT/previous['draftSource']
            directory=ROOT/'work'/stem/f'{previous["mode"]}-{address:08x}'/'functions'/previous['nativeAlias']
            asm=directory/'input.s';ctx=directory/'context.c'
            assembly=asm.read_text(encoding='utf-8');context=ctx.read_text(encoding='utf-8')
            _,hypotheses,_=apply(context,assembly)
            if not hypotheses:continue
            seen.add(identity)
            returns={f'func_{match[2]}':{'type':match[1].strip()} for match in re.finditer(r'^extern ([^;\n]*?)\s*native_fn_([0-9a-f]{8})\(\);',source.read_text(encoding='utf-8-sig'),re.M)}
            attempts=[item for item in previous.get('attempts',[]) if item.get('compiledBytes')]
            result.append(dict(name=previous['nativeAlias'],address=previous['address'],mode=previous['mode'],bytes=previous['bytes'],assembly=assembly,context=context,sourceReturns=returns,
                priorEvidence=path.relative_to(ROOT).as_posix(),priorBestMatchingBytes=max([item.get('matchingBytes',0) for item in attempts],default=0),priorCompilable=bool(attempts),
                inputHashes={item.relative_to(ROOT).as_posix():sha256(item) for item in [path,source,asm,ctx]}))
    return result


def main():
    items=queue()
    report=dict(createdUtc=now(),sourceCredit=0,uniqueNewBreadthFunctions=0,pairedFunctions=len(items),pairedNativeBytes=sum(item['bytes'] for item in items),
        compilerProcesses=3,results=[],generatorSha256=sha256(__file__),widthInferenceSha256=sha256(ROOT/'native_global_width_contexts_20261031.py'),
        limitations=['Access widths are candidate-local observations, not complete array or structure layouts',
            'No accepted source or declarations are edited; exact compiler results still require independent linking and native proof',
            'This repeats existing identities with only width-context and matching declaration changes; it adds no unique breadth'])
    write_json(REPORT,report);print({key:report[key] for key in ['pairedFunctions','pairedNativeBytes','sourceCredit']},flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        for row in pool.map(worker,items):
            report['results'].append(row)
            report['completedFunctions']=len(report['results'])
            report['compilerExactFunctions']=sum(item['compilerExact'] for item in report['results'])
            write_json(REPORT,report)
            print({key:report[key] for key in ['completedFunctions','compilerExactFunctions']},flush=True)
    report['finishedUtc']=now();write_json(REPORT,report)


if __name__=='__main__':main()
