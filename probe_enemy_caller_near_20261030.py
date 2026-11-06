from project import ROOT, now, sha256, write_json
import match_runtime as compiler
from recover_linked_runtime import qualified_bindings
from link_runtime_unit import validate

SOURCE = 'nonmatching/encounter/20261030-enemy-caller/locals-index-species-row-count.c'
SOURCE_SHA = '99af89404fdeb9939607a4e8c14795cf0288d822e72926ce10de4449b1d2f511'


def main():
    if sha256(ROOT / SOURCE) != SOURCE_SHA:
        raise ValueError('Frozen nonmatching caller source changed')
    rows, exact = compiler.compare(ROOT / SOURCE, 'main', 3, 'off')
    if exact or len(rows) != 1 or rows[0]['compiledBytes'] != 344 or rows[0]['matchingBytes'] != 331:
        raise ValueError('Failed caller experiment changed; record a new qualified attempt')
    row = rows[0]
    bindings = qualified_bindings(row)
    directory = ROOT / 'work/main-enemy-caller/20261030/near-link'
    try:
        validate(row, bindings, directory)
    except ValueError as error:
        failure = str(error)
        if "'matchingBytes': 331" not in failure or "'linkedBytes': 344" not in failure:
            raise ValueError('Unexpected link failure: ' + failure) from error
    else:
        raise ValueError('Previously rejected source unexpectedly passed exact linking')
    result = {'createdUtc': now(), 'evidenceClass': 'unaccepted-ordinary-C-caller-hypothesis',
              'generator': __file__.split('\\')[-1].split('/')[-1], 'generatorSha256': sha256(__file__),
              'reproductionCommand': ['python', 'probe_enemy_caller_near_20261030.py'],
              'sourceCredit': 0, 'source': row, 'bindings': bindings, 'exactLinkRejected': True,
              'failure': failure, 'nativeBehavioralExecutionClaimed': False,
              'ordinarySceneReachabilityClaimed': False,
              'unresolved': 'Complete 344-byte C body differs in internal register allocation; exact source gate remains failed'}
    write_json(ROOT / 'evidence/attempts/main-enemy-caller-near-link-20261030.json', result)
    print({'failedExperimentReproduced': True, 'linkedBytes': 344, 'matchingBytes': 331, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
