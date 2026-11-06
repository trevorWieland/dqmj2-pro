import os
import shutil
import uuid
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256
import collector_path_lookup_epoch_20261106 as lookup_module
import oracle_source_closure_v3_20261106 as candidate
import wave20261105_source_capture_perf_bench as fixture_module
from qualify_oracle_path_cache_v3_20261106 import WORK,LANE,make_fixture
from collector_path_lookup_epoch_20261106 import PathLookupEpoch,LookupEpochChanged


def execute():
    if WORK!=ROOT/'work/w6pc' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/path-lookup-next':raise ValueError('Extra lookup-control paths differ')
    base=WORK/('extra-'+uuid.uuid4().hex[:12]);base.mkdir(parents=True);rows=[]
    def reject(name,cache):
        try:cache.verify()
        except LookupEpochChanged as error:rows.append(dict(case=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid extra lookup epoch accepted: '+name)
    root=base/'missing-dir';root.mkdir();p=root/'future';cache=PathLookupEpoch(root);cache.resolve(p);cache.is_file(p);p.mkdir();reject('missing-to-directory-even-though-is-file-stays-false',cache)
    root=base/'parent-replacement';root.mkdir();p=root/'parent';p.mkdir();cache=PathLookupEpoch(root);cache.resolve(p/'absent.py');p.rename(root/'old-parent');p.mkdir();reject('same-type-parent-directory-identity-replaced',cache)
    root=base/'observed-hash';root.mkdir();p=root/'unit.py';p.write_bytes(b'VALUE=1\n');cache=PathLookupEpoch(root);cache.hash(p);p.write_bytes(b'VALUE=2\n')
    try:cache.hash(p)
    except LookupEpochChanged:pass
    else:raise ValueError('Repeated actual content hash ignored a source mutation')
    p.write_bytes(b'VALUE=1\n');reject('observed-content-hash-change-then-restored',cache)
    root=base/'failed-hash';root.mkdir();p=root/'unit.py';p.write_bytes(b'VALUE=1\n');cache=PathLookupEpoch(root);cache.hash(p);p.unlink()
    try:cache.hash(p)
    except FileNotFoundError:pass
    else:raise ValueError('Actual missing content read did not fail')
    p.write_bytes(b'VALUE=1\n');reject('observed-content-read-failure-then-restored',cache)
    root=base/'json-race';root.mkdir();p=root/'input.json';write_json(p,dict(value=1));cache=PathLookupEpoch(root)
    def mutate_json(path):write_json(path,dict(value=2));return read_json(path)
    with patch.object(lookup_module,'read_json',mutate_json):
        try:cache.read_json(p)
        except LookupEpochChanged:pass
        else:raise ValueError('JSON content change during read was accepted')
    write_json(p,dict(value=1));reject('observed-json-read-content-change-then-restored',cache)
    root=base/'optional-json-race'
    with patch.object(fixture_module,'WORK',WORK):fixture_module.fixture(root,groups=1)
    for name in ['oracle_source_closure_20261031.py','oracle_source_closure_v2_20261106.py']:shutil.copyfile(ROOT/name,root/name)
    report=root/'evidence/reports/report000.json';original=report.read_bytes()
    def changed_optional(path):
        if path==report:write_json(path,dict(matches=[]))
        return read_json(path)
    with patch.object(candidate,'ROOT',root),patch.object(candidate,'SEARCH',[root,root/'evidence/application',root/'evidence/encounter',root/'evidence/save',root/'nonmatching/encounter']),patch.object(lookup_module,'read_json',changed_optional),patch('builtins.print'):
        try:candidate.collect()
        except LookupEpochChanged as error:rows.append(dict(case='optional-json-original-valueerror-skip-cannot-swallow-sticky-epoch-failure',rejected=True,reason=str(error)))
        else:raise ValueError('Original optional-JSON skip suppressed the final epoch guard')
    report.write_bytes(original)
    code=root/'oracle_source_closure_v2_20261106.py';original=code.read_bytes();code.write_bytes(b'X'+original[1:])
    with patch.object(candidate,'ROOT',root):
        try:candidate.collect()
        except ValueError as error:
            if 'Pinned qualifiedv2source' not in str(error):raise
            rows.append(dict(case='wrong-qualified-base-code-pin',rejected=True,reason=str(error)))
        else:raise ValueError('Wrong base-code pin accepted')
    code.write_bytes(original);write_json(LANE/'extra-v3-controls.json',dict(passed=True,sourceCredit=0,generatorSha256=sha256(__file__),lookupSha256=sha256(ROOT/'collector_path_lookup_epoch_20261106.py'),collectorSha256=sha256(ROOT/'oracle_source_closure_v3_20261106.py'),controls=rows,allMutationsPrivate=True,noFullRealEpochClaim=True));print(dict(passed=True,controls=len(rows),receiptSha256=sha256(LANE/'extra-v3-controls.json')))


if __name__=='__main__':execute()
