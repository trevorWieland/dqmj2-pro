import copy
import subprocess
from pathlib import Path
from unittest.mock import patch
import verify_committed_source_inputs_v8_20261101 as original
from project import ROOT, read_json, write_json, sha256
from qualify_arm9_reference_packets_v2_20261105 import LEDGER, qualify_report
from qualify_msl_reference_inputs_20261105 import qualify as qualify_copied_msl
from qualify_arm9_overlay_reference_inputs_20261105 import qualify as qualify_overlay
import argparse
import sys


def output_path(cohort,name):
    assert cohort==157,'This v13 wrapper is qualified only for accepted source157; later modes/scopes require a composed auditor'
    output=(ROOT/name).resolve()
    lane=(ROOT/'evidence/lanes/parallel-wave20261105/overlay-reference-input-v13').resolve()
    canonical=(ROOT/f'evidence/verification/cohort{cohort}-committed-source-inputs-v13-20261105.json').resolve()
    assert output.is_relative_to(ROOT) and output.suffix=='.json' and (output.parent==lane or output==canonical),'Output must be new owned v13 audit evidence'
    return output


def main():
    own_hash=sha256(__file__)
    preserved=['verify_committed_source_inputs_v8_20261101.py','verify_committed_source_inputs_v11_20261105.py','verify_committed_source_inputs_v12_20261105.py']
    old_hashes={name:sha256(ROOT/name) for name in preserved}
    for name in preserved:assert subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT)==(ROOT/name).read_bytes()
    parser=argparse.ArgumentParser()
    parser.add_argument('--cohort',type=int,required=True)
    parser.add_argument('--output',default='evidence/lanes/parallel-wave20261105/overlay-reference-input-v13/committed-source-inputs-v13.json')
    options=parser.parse_args()
    output=output_path(options.cohort,options.output)
    actual_batches = original.batches()
    overlay_batches, overlay_proof=qualify_overlay(actual_batches, ROOT/'work/overlay-reference-v13/qualification')
    projected_batches, copied_msl = qualify_copied_msl(overlay_batches)
    ledger = read_json(ROOT / LEDGER)
    assert subprocess.check_output(['git', 'show', 'HEAD:' + LEDGER], cwd=ROOT) == (ROOT / LEDGER).read_bytes()
    projected, qualifications = {}, []
    for consumer in ledger['consumers']:
        if not consumer.get('sourceOnlyCompilerInputQualification'):
            continue
        proof = qualify_report(consumer['report'], consumer['expectedRanges'],
            ROOT / 'work/integration/overlay-reference-v13/arm9-existing' / str(len(qualifications)))
        assert proof['producerSha256'] == consumer['producerSha256'] == sha256(ROOT / consumer['producer'])
        report = copy.deepcopy(read_json(ROOT / consumer['report']))
        inputs = {p['address']: p['sourceOnlyCompilerInput'] for p in proof['proofs']}
        for row in report['matches']:
            assert 'sourceOnlyCompilerInput' not in row
            row['sourceOnlyCompilerInput'] = inputs[row['address']]
        projected[(ROOT / consumer['report']).resolve()] = report
        qualifications.append(proof)

    def qualified_read(path):
        path = Path(path).resolve()
        return projected[path] if path in projected else read_json(path)

    def qualified_write(path, document):
        document['explicitCopiedDependencyPaths'] += len(copied_msl)
        document.update(qualifiedCopiedReferenceInputs=copied_msl, exactFrozenRegistryUnmodified=True)
        document['limitations'].append('Four explicitly qualified external MSL text references are independently hash-checked as copied source-generation inputs; no production C/header or executable input is exempted')
        document.update(generator=Path(__file__).name, generatorSha256=sha256(__file__),
            previousEightInputVerifierUnchanged=True, previousV12VerifierUnchanged=True, freshCompilerInputQualifications=qualifications,
            sourceRegistrySourcesObjectsFlagsAndCanonicalReportsUnchanged=True)
        assert sha256(__file__)==own_hash and old_hashes=={name:sha256(ROOT/name) for name in preserved}
        document.update(preservedVerifierHashes=old_hashes)
        document['derivedExecutableInputs'].append(overlay_proof['overlay'])
        document.update(qualifiedOverlayReferenceInput=overlay_proof,overlayOriginalExecutableCompilerInput=False)
        document['limitations'].append('Only independently derived ov000 and its two committed main ARM callers are added; no blanket extract exception, Thumb relaxation, registry rewrite or executable blob commit')
        write_json(output, document)

    saved_argv=sys.argv
    try:
        sys.argv=[__file__,'--cohort',str(options.cohort)]
        with patch.object(original, 'batches', return_value=projected_batches), patch.object(original, 'read_json', side_effect=qualified_read), patch.object(original, 'write_json', side_effect=qualified_write):
            original.main()
    finally:sys.argv=saved_argv
    final=read_json(output)
    print(dict(passed=final['passed'],sourceCredit=0,qualifiedDerivedExecutableInputs=len(final['derivedExecutableInputs']),report=output.relative_to(ROOT).as_posix()))


if __name__ == '__main__':
    main()
