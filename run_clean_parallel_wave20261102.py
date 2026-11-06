from pathlib import Path
from unittest.mock import patch
import validate_clean_checkout as replay
from project import ROOT, write_json


def main():
    target = ROOT.parent / 'j2p-clean-parallel-wave20261102'
    destination = ROOT / 'evidence/verification/parallel-wave20261102'

    def publish(path, document):
        path = Path(path).resolve()
        if path.parent != ROOT / 'evidence/verification' or not path.name.startswith('clean-checkout'):
            raise ValueError('Unexpected clean-checkout report publication')
        document['reportPublicationOnlyRedirected'] = True
        document['originalCleanReplayDriver'] = 'validate_clean_checkout.py'
        document['separateAcceptedSourceWave'] = 146
        write_json(destination / path.name, document)

    with patch.object(replay, 'write_json', publish):
        replay.main(target, 14400)


if __name__ == '__main__':
    main()
