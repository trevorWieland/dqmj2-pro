import copy
from unittest.mock import patch
import seal_recovery_evidence_20261031 as seal
from project import ROOT,read_json,write_json,sha256


def main():
    path='evidence/matches/mechanics-save-20261030-lane-word-arrays.json'
    original=read_json(ROOT/path)
    controls=[]
    model='evidence/application/save_core_word_array_machine_20261030.py'
    for kind in ['stale-declared-model','changed-frozen-model','inconsistent-function-summary']:
        document=copy.deepcopy(original)
        if kind=='stale-declared-model':
            document['replayDependencies'].append({'path':model,'sha256':'0'*64})
        elif kind=='changed-frozen-model':
            document['generatorSources']=[{'path':model,'sha256':'0'*64}]
        else:
            document['functionMatches']=len(document['matches'])+1
        try:
            with patch.object(seal,'read_json',return_value=document),patch.object(seal,'write_json',side_effect=AssertionError('Invalid seal was written')):
                seal.seal(path,['match_mechanics_save_20261030_lane_word_arrays.py'])
        except ValueError as error:
            controls.append({'name':kind,'rejected':True,'reason':str(error)})
        else:
            raise AssertionError(kind)
    try:
        seal.code_closure(['../outside.py'])
    except ValueError as error:
        controls.append({'name':'outside-code-path','rejected':True,'reason':str(error)})
    else:
        raise AssertionError('Escaping code accepted')
    assert read_json(ROOT/path)==original
    report={'passed':True,'controls':controls,'acceptedInputsModified':False,'sourceCredit':0,
        'generatorSha256':sha256(ROOT/'seal_recovery_evidence_20261031.py'),
        'validatorSha256':sha256(ROOT/'verify_replay_code_seal_20261031.py')}
    write_json(ROOT/'evidence/verification/replay-code-seal-controls-20261031.json',report)
    print({'sealRejectionControls':len(controls),'passed':True})


if __name__=='__main__':
    main()
