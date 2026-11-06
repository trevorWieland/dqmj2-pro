from collections import Counter
import run_checks as original
from project import ROOT, sha256, write_json

EXPECTED = '95ecfe1499a1b084bb62bf2acb73e966e65ff02071e09566ad3391607dfa1aa3'


def producer_first(accepted_oracles, interpreted_batches):
    commands = original_oracle_commands(accepted_oracles, interpreted_batches)
    producers = {tuple(row['reproduce']) for row in interpreted_batches}
    assert producers <= {tuple(command) for command in commands}
    prefix = [command for command in commands if tuple(command) in producers]
    suffix = [command for command in commands if tuple(command) not in producers]
    reordered = prefix + suffix
    assert Counter(map(tuple, commands)) == Counter(map(tuple, reordered))
    assert all(tuple(command) in producers for command in reordered[:len(prefix)])
    write_json(ROOT / 'evidence/verification/interpreted-producer-first-order-20261101.json',
        dict(sourceCredit=0, originalRunnerSha256=EXPECTED, adapterSha256=sha256(__file__),
            originalCommands=commands, reorderedCommands=reordered,
            commandMultiplicityPreserved=True, sourceProducersBeforeAllOracleConsumers=True,
            sourceAndValidatorChanges=False, timeoutAndAcceptanceChanges=False))
    return reordered


assert sha256(ROOT / 'run_checks.py') == EXPECTED
original_oracle_commands = original.oracle_commands


if __name__ == '__main__':
    original.oracle_commands = producer_first
    raise SystemExit(original.main())
