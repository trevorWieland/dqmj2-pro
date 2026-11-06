from project import ROOT, read_json, write_json, sha256, configuration
import wave20261102_battle_fifth_packet01 as First
import wave20261102_battle_fifth_packet02 as Adjacent

LANE=ROOT/'evidence/lanes/parallel-wave20261102/battle-fifth'


def main():
    inputs=LANE/'all-inputs.json'
    for pin in read_json(inputs)['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:
            raise ValueError(('Battle family frozen input changed',pin['path']))
    First.main()
    Adjacent.main()
    reports=[read_json(LANE/name)for name in ['packet01-match.json','packet02-match.json']]
    matches=[row for report in reports for row in report['matches']]
    if len(matches)!=3 or sum(row['bytes']for row in matches)!=1216 or len({row['name']for row in matches})!=3:
        raise ValueError('Battle family complete extent set differs')
    result=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=reports[0]['moduleSha256'],mainSha256=reports[0]['mainSha256'],allPassed=all(report['allPassed']for report in reports),matches=matches,canonicalMatchedFunctions=3,canonicalMatchedBytes=1216,sourceCreditPendingSharedAcceptance=True,producer='wave20261102_battle_fifth_all.py',producerSha256=sha256(__file__),inputs=dict(path=inputs.relative_to(ROOT).as_posix(),sha256=sha256(inputs)),freshlyCompiledAllObjectsOnEveryReplay=True,cases=sum(report['cases']for report in reports),actualNativeAndSourceCallerReturns=sum(report['actualNativeAndSourceCallerReturns']for report in reports),actualTopReturnsIncludingControls=sum(report['actualTopReturnsIncludingControls']for report in reports),actualNativeHelperReturns=0,completePhysicalRegistersCpsrRawCallsOrderedWritesAndAll8MiBRamEqual=True,independentRawByteWordModelsPassed=True,componentReports=[dict(path=(LANE/name).relative_to(ROOT).as_posix(),sha256=sha256(LANE/name))for name in ['packet01-match.json','packet02-match.json']],abiDebt=reports[0]['abiDebt'],limits=['Three independently reconstructed game-controller bodies with complete native extents and qualified typed host bindings. Every object and every real link is freshly rebuilt on this producer replay.', 'All raw phase bytes per function plus bounded cursor/actor word, low-byte return handling, signed counter rollover and sequential phase transition fixtures. Actual source/native caller returns are distinct from supplied external boundaries.', 'External code does not execute in these fixtures, receives zero source/execution credit, and raw field values carry no inferred game meaning. Original-helper ABI debt is preserved separately.', 'Whole-module/ROM acceptance and shared ledger publication remain coordinator-owned; no source-only ROM or host/device execution claim.'])
    write_json(LANE/'all-match.json',result)
    print(dict(functions=3,bytes=1216,cases=result['cases'],actualTopReturns=result['actualTopReturnsIncludingControls']),flush=True)


if __name__=='__main__':
    main()
