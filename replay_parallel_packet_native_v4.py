import argparse
import copy
import hashlib
import importlib
import json
from pathlib import Path
import sys
import parallel_packet_binding_projection_v2 as projection
import parallel_packet_native_unit_identity_v1 as unit_identity


def pin(root,path):
    return dict(path=path.relative_to(root).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def invoke(root,descriptor_name,original):
    root=Path(root).resolve()
    descriptor_path=projection.local(root,descriptor_name)
    descriptor=json.loads(descriptor_path.read_bytes())
    target=root/descriptor['canonicalReport']
    if target.absolute()!=target.resolve()or not target.is_relative_to(root/'evidence/matches')or target.suffix!='.json':raise ValueError('Confined-generated-canonical-report')
    if not target.name.startswith('cohort176-parallel-wave20261107-f-'):raise ValueError('Only-newF-canonical-targets-not-oldB-or-C-or-D-or-E')
    if target==root/descriptor['workerReport']:raise ValueError('Frozen-worker-is-not-canonical-output')
    saved_writer,saved_argv=original.write_json,sys.argv
    writes=0
    def write(path,report):
        nonlocal writes
        if Path(path).resolve()!=target or writes:raise ValueError('Exactly-one-descriptor-canonical-write')
        bound=projection.project(root,report,descriptor['identities'])
        output=unit_identity.project(root,bound,descriptor['nativeUnitIdentities'])
        sources={}
        for row in output.get('generatorSources',[]):
            if row['path']in sources and sources[row['path']]!=row['sha256']:raise ValueError('Conflicting-generator-source-pins')
            sources[row['path']]=row['sha256']
        for source_path in(Path(__file__).resolve(),Path(projection.__file__).resolve(),Path(unit_identity.__file__).resolve()):
            record=pin(root,source_path)
            if record['path']in sources and sources[record['path']]!=record['sha256']:raise ValueError('Changed-canonical-schema-generator')
            sources[record['path']]=record['sha256']
        output['generatorSources']=[dict(path=name,sha256=value)for name,value in sorted(sources.items())]
        output['canonicalPacketSchemaAdapter']=dict(version=4,generatedMetadataOnly=True,sourceCredit=0,
            frozenWorkerReportUnmodified=descriptor['workerReport'],underlyingBridge='replay_parallel_packet.py')
        checked=copy.deepcopy(output)
        if 'generatorSources'in report:checked['generatorSources']=report['generatorSources']
        else:checked.pop('generatorSources',None)
        checked.pop('canonicalPacketSchemaAdapter',None)
        baseline=copy.deepcopy(report);baseline.pop('canonicalPacketSchemaAdapter',None)
        for old,row in zip(baseline['matches'],checked['matches']):
            if 'dsdSymbol'in old:row['dsdSymbol']=old['dsdSymbol']
            else:row.pop('dsdSymbol',None)
        projection.assert_allowed_delta(baseline,checked)
        identity_checked=copy.deepcopy(output)
        for field in ('generatorSources','canonicalPacketSchemaAdapter'):
            if field in bound:identity_checked[field]=bound[field]
            else:identity_checked.pop(field,None)
        unit_identity.assert_allowed_delta(bound,identity_checked,descriptor['nativeUnitIdentities'])
        if Path(path).absolute()!=target or Path(path).resolve()!=target:
            raise ValueError('Downstream-writer-must-receive-exact-canonical-target')
        writes+=1
        saved_writer(target,output)
    try:
        original.write_json=write
        sys.argv=[str(original.__file__),descriptor_name]
        original.main()
        if writes!=1:raise ValueError('Underlying-fresh-bridge-did-not-produce-one-report')
    finally:
        original.write_json=saved_writer
        sys.argv=saved_argv


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('descriptor')
    options=parser.parse_args()
    root=Path.cwd().resolve()
    if str(root)not in sys.path:sys.path.insert(0,str(root))
    original=importlib.import_module('replay_parallel_packet')
    invoke(root,options.descriptor,original)


if __name__=='__main__':
    main()
