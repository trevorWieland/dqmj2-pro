import gzip
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from inspect_windows_native_link_frontier111_20261101 import coff
from check_save_core_explicit_clear_windows32_20261101 import LINKER_SHA


def unpack(report):
    path = ROOT / report['details']['path']
    assert sha256(path) == report['details']['sha256']
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == report['details']['decodedSha256']
    return json.loads(raw)


def main():
    candidate_path = ROOT / 'evidence/portability/windows-qualified-alias111-20261101.json'
    candidate_report = read_json(candidate_path)
    candidates = unpack(candidate_report)['aliases']
    catalogue = ROOT / candidate_report['catalogue']['path']
    assert sha256(catalogue) == candidate_report['catalogue']['sha256']
    for row in candidate_report['measuredArmReports']:
        assert sha256(ROOT / row['path']) == row['sha256'], row['path']
    frontier_path = ROOT / 'evidence/portability/windows-selected-link-frontier111-v3-20261101.json'
    frontier = read_json(frontier_path)
    objects = unpack(frontier)['objects']
    shared_path = ROOT / 'evidence/portability/windows-itcm-shared-data72-20261101.json'
    shared = read_json(shared_path)
    variant = shared['windowsReferenceVariant']
    assert sha256(ROOT / variant['source']) == variant['sourceSha256']
    assert sha256(ROOT / variant['object']) == variant['objectSha256']
    host, definitions, undefined = {}, {}, set()
    for row in objects:
        if not any(processor == 'arm9' and not program for processor, program, module in row['scopes']):
            continue
        path = ROOT / (variant['object'] if row['source'] == variant['originalSource'] else row['object'])
        expected = variant['objectSha256'] if row['source'] == variant['originalSource'] else row['objectSha256']
        assert sha256(path) == expected
        host[row['source']] = path
        parsed = coff(path)
        for symbol in parsed['definitions']:
            if symbol['function']:
                assert symbol['name'] not in definitions
                definitions[symbol['name']] = row['source']
        undefined.update(symbol['name'] for symbol in parsed['undefined'])
    accepted, rejected = [], []
    for row in candidates:
        if row['classification'] != 'type-and-qualified-identity-candidate':
            continue
        alias, provider = row['alias'], row['providerSymbol']
        valid = all(re.fullmatch(r'_[A-Za-z_]\w*', name) for name in [alias, provider])
        valid &= alias in undefined and alias not in definitions
        valid &= definitions.get(provider) == row['providerSource']
        if not valid:
            rejected.append(dict(alias=alias, provider=provider, reason='Native symbol ownership or actual unresolved reference not unique'))
            continue
        accepted.append(dict(alias=alias, provider=provider, providerSource=row['providerSource'],
            physicalTarget=row['qualifiedTargets'], compatibleSignature=row['providerSignature'],
            observedConsumers=row['consumerSources']))
    assert accepted
    work = ROOT / 'work/windows-qualified-alias111-20261101'
    work.mkdir(parents=True, exist_ok=True)
    output = work / 'host-arm9.dll'
    assert not output.exists()
    linker = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/ld.lld.exe'
    assert sha256(linker) == LINKER_SHA
    arguments = ['/dll', '/noentry', '/machine:x86', '/nodefaultlib', '/safeseh:no',
        '/timestamp:0', '/errorlimit:0', '/opt:noref', '/out:' + str(output)]
    arguments.extend('/alternatename:' + row['alias'] + '=' + row['provider'] for row in accepted)
    arguments.extend(str(path) for name, path in sorted(host.items()))
    response = work / 'host-arm9.rsp'
    response.write_text('\n'.join(subprocess.list2cmdline([value]) for value in arguments) + '\n', encoding='utf-8')
    command = [str(linker), '-flavor', 'link', '@' + str(response)]
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    run = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
        timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
    diagnostic = run.stdout + run.stderr
    text = diagnostic.decode(errors='replace')
    missing = sorted(set(re.findall(r'undefined symbol: (.+)', text)))
    duplicates = text.count('duplicate symbol:')
    assert run.returncode != 0 and not output.exists() and missing and duplicates == 0
    log = ROOT / 'evidence/portability/windows-qualified-alias111-link-diagnostic-20261101.txt.gz'
    log.write_bytes(gzip.compress(diagnostic, mtime=0))
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        candidates=dict(path=candidate_path.relative_to(ROOT).as_posix(), sha256=sha256(candidate_path)),
        sharedDataQualification=dict(path=shared_path.relative_to(ROOT).as_posix(), sha256=sha256(shared_path)),
        hostObjectUnits=len(host), aliasesApplied=len(accepted), aliasRecords=accepted,
        rejectedAtNativeOwnershipGate=rejected, actualLinkExitCode=run.returncode,
        actualDuplicateSymbolDiagnostics=duplicates, remainingUndefinedSymbols=len(missing),
        unresolvedSymbols=missing, command=command,
        responseFile=dict(path=response.relative_to(ROOT).as_posix(), sha256=sha256(response)),
        diagnostic=dict(path=log.relative_to(ROOT).as_posix(), sha256=sha256(log), decodedSha256=hashlib.sha256(diagnostic).hexdigest()),
        nativeExecutionCount=0, sourceCredit=0, generatedStubs=0, sourceBodiesModified=False,
        linkerErrorsSuppressed=False, outputProduced=False, fullWindowsGameProven=False,
        limitations=['Only host ARM9 aliases with unique measured native targets and compatible primitive C call contracts are applied',
            'Default-prototype escapes, incomplete targets, aggregate/callback types and mismatches remain unresolved',
            'No entry point, original ARM code or missing implementation is supplied; the diagnostic link remains a hard failure',
            'Native runtime behavior, logical code-pointer identity, overlay lifetime and coherent shared data still need qualification',
            'Source111 corpus only; later cohorts, blocked C units and ARM assembly remain separate'])
    write_json(ROOT / 'evidence/portability/windows-qualified-alias111-link-20261101.json', report)
    print(dict(hostObjects=len(host), aliasesApplied=len(accepted), duplicateDiagnostics=duplicates,
        remainingUndefinedSymbols=len(missing), fullNativeGame=False, sourceCredit=0))


if __name__ == '__main__':
    main()
