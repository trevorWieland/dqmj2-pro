import hashlib
from pathlib import Path
import subprocess
from project import ROOT


BASE_COMMIT = 'a85a77f7f3c284cdfcf4e3cb7e81a65e06f993b9'
BASE_SHA256 = 'e698ec92eb31e9fa26d911057bb2f461e31d5a4e8e52d13f038deea26dd4eba8'
BOUNDARY_SHA256 = 'ccc0c5bcab60fa9a7ea31401a32fcb91e431e76a524bd5d669b5c4b041e96bf2'
FINAL_SHA256 = '68212a6ac17f33b49f3f3a09c0f4ecf003dedb7a4d7bb9ea53479a5b22e93ac5'


def build(work, observed_scope_guard=False):
    payload = subprocess.run(['git', 'show', BASE_COMMIT + ':run_checks.py'], cwd=ROOT,
        check=True, capture_output=True).stdout
    if hashlib.sha256(payload).hexdigest() != BASE_SHA256:
        raise ValueError('Frozen original runner differs')
    text = payload.decode('utf-8-sig').replace('\r\n', '\n')
    needle = '        if row["exitCode"]:\n'
    insertion = '''        changed_scope = [name for name, expected in [('recovery.json', registry_hash),
            ('source-preferences.json', preference_hash), ('interpreted-recovery.json', interpreted_hash)]
            if (sha256(ROOT / name) if (ROOT / name).is_file() else None) != expected]
        if changed_scope:
            report['scopeChangedDuringReplay'] = changed_scope
            failed = True
            break
'''
    old = 'report["recoveryRegistryUnchanged"] = sha256(ROOT / "recovery.json") == registry_hash'
    new = 'report["recoveryRegistryUnchanged"] = (ROOT / "recovery.json").is_file() and sha256(ROOT / "recovery.json") == registry_hash'
    if text.count(needle) != 1 or text.count(old) != 1:
        raise ValueError('Frozen runner boundary differs')
    text = text.replace(needle, insertion + needle).replace(old, new)
    if observed_scope_guard:
        needle = "scope_current = (report['recoveryRegistryUnchanged']"
        replacement = "scope_current = (not report.get('scopeChangedDuringReplay') and report['recoveryRegistryUnchanged']"
        if text.count(needle) != 1:
            raise ValueError('Frozen final scope flag differs')
        text = text.replace(needle, replacement)
    path = Path(work) / ('run_checks_scope_final.py' if observed_scope_guard else 'run_checks_scope_boundary.py')
    path.write_text(text, encoding='utf-8')
    expected = FINAL_SHA256 if observed_scope_guard else BOUNDARY_SHA256
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError('Deterministically regenerated scope fixture differs')
    return path
