import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import utility_child_snd_alias_v1_20261106 as p
WORK = p.WORK / ('wrong-control-' + str(time.time_ns()))
WORK.mkdir(parents=True, exist_ok=True)
p.pins()
row = copy.deepcopy(p.EXPECTED)
directory = WORK / 'wrong-success-result'
directory.mkdir(exist_ok=True)
source = directory / Path(row['source']).name
text = (p.ROOT / row['source']).read_text()
if text.count('return 1 ;') != 1:
    raise ValueError('Wrong-C return control is not unique')
source.write_text(text.replace('return 1 ;', 'return 0 ;'))
shutil.copyfile(p.ROOT / row['sourceDependencies'][0]['path'], directory / 'context.h')
obj = directory / 'wrong.o'
command = [str(p.executable(row['compiler'])), *row['compilerFlags'], '-c', str(source), '-o', str(obj)]
process = subprocess.run(command, cwd=p.ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(p.ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
if process.returncode:
    raise ValueError('Wrong ordinary-C control did not compile')
row.update(source=source.relative_to(p.ROOT).as_posix(), sourceSha256=p.sha256(source), object=obj.relative_to(p.ROOT).as_posix(), objectSha256=p.sha256(obj))
try:
    p.validate_entry(row)
except ValueError:
    pinnedSourceRejected = True
else:
    raise ValueError('Frozen source admission accepted incorrect C')
spec = importlib.util.spec_from_file_location('wrong_child_alias_link', p.ROOT / 'wave20261102_child_link.py')
linker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(linker)
if linker.LINKER.absolute() != p.executable(p.CONTRACT['linker']):
    raise ValueError('Wrong-C link helper escaped the pinned original linker')
previous = linker.canonical
try:
    linker.canonical = lambda: p.original_namespace(p.EXPECTED)
    try:
        linker.validate(row, directory / 'native-link')
    except ValueError as error:
        failure = error.args[0]
        if not isinstance(failure, dict) or failure.get('equal') is not False:
            raise
    else:
        raise ValueError('Genuine MW link accepted incorrect C')
finally:
    linker.canonical = previous
attempt = json.loads((directory / 'native-link/link-attempt.json').read_bytes())
if attempt['exitCode'] != 0:
    raise ValueError('Wrong-C control failed before actual linker byte comparison')
p.pins()
result = dict(proposalOnly=True, sourceCredit=0, actualCompilerPassed=True, actualGenuineLinkerPassed=True, originalCallerBytesRejected=True, pinnedSourceRejected=pinnedSourceRejected, source=row['source'], sourceSha256=row['sourceSha256'], object=row['object'], objectSha256=row['objectSha256'], mismatch=failure, linkAttempt=attempt, instructionOrObjectPatching=False, globalGateExecuted=False)
(directory / 'control.json').write_text(json.dumps(result, indent=2) + '\n')
print({key: result[key] for key in ['actualCompilerPassed', 'actualGenuineLinkerPassed', 'originalCallerBytesRejected', 'pinnedSourceRejected', 'globalGateExecuted']})
