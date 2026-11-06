import argparse
from project import ROOT,read_json,write_json,sha256,now


LANE=ROOT/'evidence/lanes/parallel-wave20261106/selection-snapshot-next'
OUTPUT=LANE/'prototype-qualification.json'
SOURCES=['probe_source_selection_snapshot_20261106.py','guard_source_selection_snapshot_20261106.py','verify_source_selection_snapshot_guards_20261106.py','compare_source_selection_snapshot_full_20261106.py','freeze_source_selection_snapshot_20261106.py']
RECEIPTS=['bounded-real-policy-equivalence.json','snapshot-guard-controls.json','full-real-selection-equivalence.json']


def validate():
    full=read_json(LANE/RECEIPTS[2]);controls=read_json(LANE/RECEIPTS[1]);bounded=read_json(LANE/RECEIPTS[0])
    if not all(r['passed'] and r['sourceCredit']==0 for r in [full,controls,bounded]):raise ValueError('Qualified receipt failed or claims source credit')
    if len(controls['controls'])!=10 or not all(r['rejected'] for r in controls['controls']):raise ValueError('Snapshot mutation controls are incomplete')
    if not all(r['passed'] and r['preferences']==129 and r['reportOrders']==258 and r['controls']==269 for r in full['samples']):raise ValueError('Full unchanged verifier scope differs')
    if full['samples'][0]['privateOutputSha256']!=full['samples'][1]['privateOutputSha256']:raise ValueError('Full reports are not byte-identical')
    for row in full['sourcePins']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Qualified source changed: '+row['path'])
    if controls['generatorSha256']!=sha256(ROOT/SOURCES[2]) or controls['snapshotImplementationSha256']!=sha256(ROOT/SOURCES[1]):raise ValueError('Mutation-control implementations changed')
    if full['generatorSha256']!=sha256(ROOT/SOURCES[3]) or bounded['generatorSha256']!=sha256(ROOT/SOURCES[0]):raise ValueError('Comparison implementations changed')
    return full


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args();full=validate()
    if args.verify:
        bundle=read_json(OUTPUT)
        for row in bundle['files']:
            if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozen qualification file changed: '+row['path'])
    else:
        if OUTPUT.exists():raise ValueError('Qualification already frozen; use --verify')
        names=SOURCES+[(LANE/name).relative_to(ROOT).as_posix() for name in RECEIPTS]
        write_json(OUTPUT,dict(passed=True,sourceCredit=0,frozenUtc=now(),files=[dict(path=name,sha256=sha256(ROOT/name)) for name in names],originalSourcePins=full['sourcePins'],fullPreferences=129,reportOrders=258,originalControls=269,additionalMutationControls=10,originalSeconds=full['samples'][0]['elapsedSeconds'],snapshotBodySeconds=full['samples'][1]['elapsedSeconds'],recordedSnapshotConstructionSeconds=full['snapshotBuildSeconds'],observedRatio=full['observedFullSpeedRatio'],savedSeconds=full['savedSeconds'],timeReductionPercent=full['timeReductionPercent'],fullOutputByteIdentical=True,freshSourceObjectChecksAcrossBothPasses=340256,actualInputFiles=full['trackedFiles'],resolvedPathFacts=full['trackedResolutionFacts'],productionAdopted=False,limits=['The timing pair includes common input-tracking instrumentation in both phases. Shared before/after epoch guard time and imports are excluded; the recorded constructor timer excludes its initial two hash calls. These are comparison timings, not a forecast of an uninstrumented production command.','Registry/default-policy snapshots alone are cached. All source/object/dependency/report-order/custom-negative checks remain fresh and original.','Guard fixtures mutate only private copies, including a real same-content Windows junction retarget. File times are change detectors; final exact SHA and resolved targets remain required.','Prototype and comparison helpers are frozen diagnostic tooling. Any production CLI requires independent qualification and coordinator adoption.']))
    print(dict(passed=True,path=OUTPUT.relative_to(ROOT).as_posix(),sha256=sha256(OUTPUT)))


if __name__=='__main__':main()
