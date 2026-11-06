import ctypes
import subprocess
import sys
import time
from ctypes import wintypes
from concurrent.futures import ThreadPoolExecutor
from project import ROOT, read_json, write_json, sha256, now


def main():
    hold = read_json(ROOT / 'evidence/verification/cohort159-parent-incident-hold-20261105.json')
    audit_name = 'evidence/lanes/parallel-wave20261105/gamespy-qr2-next/eighth/routing-incident/restored-seven-packet-audit.json'
    audit = read_json(ROOT / audit_name)
    assert audit['allSevenReadyInputPinsExact'] and audit['uniqueImmutablePinsVerified'] == 1499
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    native = ctypes.WinDLL('ntdll')
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.WaitForSingleObject.restype = wintypes.DWORD
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    native.NtResumeProcess.argtypes = [wintypes.HANDLE]
    native.NtResumeProcess.restype = wintypes.LONG
    parent = kernel.OpenProcess(0x0800, False, hold['processId'])
    child = kernel.OpenProcess(0x100000, False, hold['childValidationProcessId'])
    assert parent and child, ctypes.get_last_error()
    output = ROOT / 'evidence/verification/cohort159-post-incident-revalidation-20261105.json'
    result = dict(startedUtc=now(), sourceCredit=0, state='waiting-for-existing-child',
        parentProcessId=hold['processId'], childProcessId=hold['childValidationProcessId'],
        restoredPinAuditSha256=sha256(ROOT / audit_name), generatorSha256=sha256(__file__))
    write_json(output, result)

    def verify_pins():
        pins = {}
        for packet in audit['packets']:
            for kind in ['ready', 'inputs']:
                row = packet[kind]
                assert sha256(ROOT / row['path']) == row['sha256']
            ready = read_json(ROOT / packet['ready']['path'])
            reports = {item['report'] for item in ready['packets']}
            rows = read_json(ROOT / packet['inputs']['path'])['files'] + ready['files']
            for row in rows:
                if row['path'] in reports:
                    continue
                assert row['path'] not in pins or pins[row['path']] == row['sha256']
                pins[row['path']] = row['sha256']
        assert len(pins) == audit['uniqueImmutablePinsVerified']
        def check(item):
            name, digest = item
            assert sha256(ROOT / name) == digest, name
        with ThreadPoolExecutor(max_workers=8) as executor:
            list(executor.map(check, pins.items()))
        return len(pins)

    try:
        while kernel.WaitForSingleObject(child, 0) == 258:
            driver = read_json(ROOT / 'evidence/verification/cohort159-validation-driver.json')
            assert driver['state'] != 'failed', driver
            time.sleep(5)
        driver = read_json(ROOT / 'evidence/verification/cohort159-validation-driver.json')
        assert driver['state'] == 'build-and-regression-checks-passed' and len(driver['steps']) == 16
        result.update(state='rerunning-restored-input-freshness', preRerunPins=verify_pins(),
            originalDriverSha256=sha256(ROOT / 'evidence/verification/cohort159-validation-driver.json'),
            originalFreshnessSha256=sha256(ROOT / 'evidence/verification/evidence-freshness.json'))
        write_json(output, result)
        registry = sha256(ROOT / 'recovery.json')
        log = ROOT / 'logs/integration/cohort159-post-incident-freshness-20261105.txt'
        with log.open('w', encoding='utf-8') as stream:
            subprocess.run([sys.executable, str(ROOT / 'validate_evidence_ash_cache_20261031.py')],
                cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True)
        fresh = read_json(ROOT / 'evidence/verification/evidence-freshness.json')
        assert fresh['passed'] and fresh['restoredSourceFunctions'] == 10763
        assert sha256(ROOT / 'recovery.json') == registry
        result.update(state='verified-ready-to-resume-parent', passed=True, postRerunPins=verify_pins(),
            revalidatedSourceFunctions=fresh['restoredSourceFunctions'], sourceRegistrySha256=registry,
            allOriginalNegativeAcceptanceCases=fresh['negativeAcceptanceCases'],
            rerunLogSha256=sha256(log), restoredFreshnessSha256=sha256(ROOT / 'evidence/verification/evidence-freshness.json'))
        write_json(output, result)
        status = native.NtResumeProcess(parent)
        assert status == 0, status
        result.update(state='verified-parent-resumed', parentResumeStatus=status, finishedUtc=now())
        write_json(output, result)
        print(dict(passed=True, revalidatedSourceFunctions=10763, restoredUniquePins=result['postRerunPins'], parentResumed=hold['processId']))
    finally:
        kernel.CloseHandle(child)
        kernel.CloseHandle(parent)


if __name__ == '__main__':
    main()
