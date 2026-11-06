import argparse
from project import ROOT,read_json,write_json,sha256,now
from qualify_oracle_path_cache_v3_20261106 import LANE,ast_proof


OUTPUT=LANE/'collector-v3-qualification.json'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args();proof=ast_proof();bounded=read_json(LANE/'bounded-v3-equivalence.json');extra=read_json(LANE/'extra-v3-controls.json');full=read_json(LANE/'full-real-v3-equivalence.json')
    if not all(r['passed'] and r['sourceCredit']==0 for r in [bounded,extra,full]) or bounded['astProof']!=proof or full['astProof']!=proof:raise ValueError('Full/bounded/code qualification differs')
    if len(bounded['mutationControls'])!=9 or len(extra['controls'])!=7 or not all(c['rejected'] for c in extra['controls']):raise ValueError('Required lookup controls missing')
    if not full['completeOutputByteIdentical'] or full['candidate']['paths']!=22833 or full['candidate']['outputSha256']!='33c6cb2ca2e601eb675b1e9c8d751927e0ead32282acb01fde92edab40c30f69':raise ValueError('Complete real output differs')
    for name,digest in full['sourcePins'].items():
        if sha256(ROOT/name)!=digest:raise ValueError('Full-run implementation changed: '+name)
    if extra['lookupSha256']!=proof['lookupSha256'] or extra['collectorSha256']!=proof['candidateSha256']:raise ValueError('Extra-control implementation differs')
    for receipt,generator in [(bounded,'qualify_oracle_path_cache_v3_20261106.py'),(extra,'verify_oracle_path_cache_extra_20261106.py')]:
        if receipt['generatorSha256']!=sha256(ROOT/generator):raise ValueError('Qualification control source changed')
    if args.verify:
        result=read_json(OUTPUT)
        for row in result['files']:
            if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozenv3qualification file changed: '+row['path'])
    else:
        if OUTPUT.exists():raise ValueError('Collectorv3qualification already frozen; use --verify')
        names=['oracle_source_closure_v3_20261106.py','collector_path_lookup_epoch_20261106.py','materialize_oracle_path_cache_v3_20261106.py','qualify_oracle_path_cache_v3_20261106.py','verify_oracle_path_cache_extra_20261106.py','compare_oracle_path_cache_real_20261106.py','freeze_oracle_path_cache_v3_20261106.py','oracle_source_closure_v2_20261106.py','oracle_source_closure_20261031.py','static_json_reads_20261031.py','project.py','compare_oracle_context_cache_real_20261106.py','qualify_oracle_context_cache_v2_20261106.py','wave20261105_source_capture_perf_bench.py']+[(LANE/name).relative_to(ROOT).as_posix() for name in ['bounded-v3-equivalence.json','extra-v3-controls.json','full-real-v3-equivalence.json']]
        write_json(OUTPUT,dict(passed=True,sourceCredit=0,frozenUtc=now(),files=[dict(path=name,sha256=sha256(ROOT/name)) for name in names],astProof=proof,fullRealSnapshot=full['snapshot'],fullClosurePaths=22833,fullClosureSha256=full['candidate']['outputSha256'],boundedCompleteOutputAndBehaviorEquality=True,meaningfulControls=16,fullCandidateTiming=full['candidate'],historicalQualifiedV2Timing=full['baseline']['timing'],historicalUnpairedRatio=full['historicalBaselineRatio'],productionAdopted=False,coordinatorSteps=['Review the conservative resolution/type/miss/directory/content guard semantics and exact AST delta.','If adopting, create a new pinned stage delegate to selectv3; preserve every qualifiedv2/v8/original collector and active job.','Require success status and full current-input guards during future staging.'],limits=full['limits']+['This establishes guarded static source-closure output equivalence and performance only; it is not a clean ROM replay, a source-acceptance increment or proof of unrestricted concurrent filesystem equivalence.']))
    print(dict(passed=True,path=OUTPUT.relative_to(ROOT).as_posix(),sha256=sha256(OUTPUT)))


if __name__=='__main__':main()
