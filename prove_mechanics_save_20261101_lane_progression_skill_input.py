import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROFILE = 'evidence/lanes/save-core/progression-skill-input139-profile-20261101.json'
FIXTURE = 'evidence/application/save_core_progression_skill_input139_20261101.py'
REPORT = 'evidence/application/save-core-progression-skill-input139-20261101.json'
PROFILE_SHA = '013e4e83582d8a224e4af0e6fb8afa067f2812c73bc8df48f06f40c8e6943781'
CASE_SHA = 'dea44e5c9e9946ab8ccad3b80b482c017bb22cae9e5965747952a14e8de1b1c8'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    assert sha((ROOT / PROFILE).read_bytes()) == PROFILE_SHA
    process = subprocess.run([sys.executable, str(ROOT / FIXTURE)], capture_output=True, text=True,
                             timeout=180, creationflags=subprocess.CREATE_NO_WINDOW)
    assert process.returncode == 0, process.stdout + process.stderr
    result = json.loads((ROOT / REPORT).read_text())
    assert result['sourceCredit'] == 0 and result['parent']['bytes'] == 3744
    counts = result['counts']
    assert counts == dict(contexts=1536, prefixExecutions=4608, originalSkillBoundaries=768,
                          correctedSkillBoundaries=768, historicalScalarRejections=512,
                          historicalScalarCoincidences=256, originalGetterReturns=6912,
                          suppliedCalls=4608, actualParentReturns=0, actualSkillCalleeReturns=0)
    sidecar = result['vectorSidecar']
    compressed = (ROOT / sidecar['path']).read_bytes()
    assert sha(compressed) == sidecar['sha256'] and len(compressed) == sidecar['compressedBytes']
    raw = gzip.decompress(compressed)
    assert sha(raw) == sidecar['uncompressedSha256'] == CASE_SHA
    assert len(raw) == sidecar['uncompressedBytes']
    assert len(json.loads(raw)) == sidecar['contexts'] == counts['contexts']
    for row in result['hypotheses']:
        assert row['exactByteEqual'] is False and row['sourceCredit'] == 0
        assert sha((ROOT / row['source']).read_bytes()) == row['sourceSha256']
        assert sha((ROOT / row['object']).read_bytes()) == row['objectSha256']
        assert sha((ROOT / row['linkedBinary']).read_bytes()) == row['linkedBinarySha256']
    print(json.dumps(counts))
    print(sha((ROOT / REPORT).read_bytes()))


if __name__ == '__main__':
    main()
