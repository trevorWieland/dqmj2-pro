from project import ROOT, configuration, verify_inputs, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure
import draft_forwarded_interfaces_20261031 as draft
import prove_forwarded_interfaces_20261031 as native
import check_forwarded_interfaces_windows_20261031 as windows


def main():
    inputs = verify_inputs(configuration())
    draft.main()
    native.main()
    windows.main()
    profile = read_json(ROOT / 'evidence/attempts/forwarded-interfaces-20261031.json')
    native_report = read_json(ROOT / 'evidence/verification/forwarded-interfaces-native-20261031.json')
    host_report = read_json(ROOT / 'evidence/verification/forwarded-interfaces-windows-20261031.json')
    assert len(profile['candidates']) == 29 and native_report['actualOuterReturns'] == 1856
    assert host_report['actualWindowsReturns'] == 928 and host_report['negativeWholeCCompiledAndLinked']
    matches = []
    for row in profile['candidates']:
        unit = dict(row['compiled'])
        assert unit['exactAfterRealMwLink'] and unit['bytes'] == 12
        unit.update(sourceDependencies=[], sourceLanguage='C', originalObjectScaffolding=False,
            interfaceMigration=dict(previous=row['previous'], callee=row['callee'],
                explicitParameterView=row['parameterView'], historicalPrototypeProven=False, newFunctionCredit=0, newByteCredit=0),
            boundaries=dict(instructionBytes=12, literalPoolBytes=0, configuredCompleteEntry=True),
            oracle=dict(pairs=32, actualOuterReturns=64, suppliedCalleeCompletions=64,
                nativeCalleeBodyReturns=0, verifiedReturn=True, isolatedState=True,
                relevantRegistersAndFlagsCompared=True, stackOutsideOwnedFramePreserved=True,
                windowsNativeReturns=32, callerForwardingOnly=True))
        matches.append(unit)
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='main',
        matches=matches, matchedFunctions=29, matchedBytes=348, nativeSymbolEntries={},
        generatorSources=[dict(path=path, sha256=sha256(ROOT / path)) for path in code_closure(['match_forwarded_interfaces_20261031.py'])],
        oracle=dict(actualOuterReturns=1856, suppliedCalleeCompletions=1856, nativeCalleeBodyReturns=0,
            actualWindowsReturns=928, windowsNegativeActualReturns=3, verifiedReturn=True, isolatedState=True),
        negativeControls=dict(kind='separately-clang-compiled-and-LLD-linked-Windows-whole-C', rejected=2, positiveControls=1,
            report='evidence/verification/forwarded-interfaces-windows-20261031.json',
            reportSha256=sha256(ROOT / 'evidence/verification/forwarded-interfaces-windows-20261031.json')),
        sourceCreditAcceptedByThisScript=0, wholeModuleLinked=False, inputsUnchanged=verify_inputs(configuration()) == inputs,
        limitations=['Explicit argument views reproduce original caller forwarding; historical declarations remain unproved',
            'Every target is an explicit provider boundary; no target body, real pointer object, hardware or scene is credited',
            'Same ARM bytes are recompiled/linked and executed in fresh machines; Windows also executes the explicit C interfaces',
            'Prospective zero-coverage migrations only; prior sources, objects and registry remain unchanged until coordinator acceptance'])
    assert report['inputsUnchanged']
    write_json(ROOT / 'evidence/matches/main-forwarded-interfaces-20261031.json', report)
    print(dict(functions=29, prospectiveMigrationBytes=348, actualOuterReturns=1856, actualWindowsReturns=928, newSourceCredit=0))


if __name__ == '__main__':
    main()
