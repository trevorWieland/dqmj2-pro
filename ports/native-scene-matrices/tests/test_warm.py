import pathlib
import subprocess
import sys
import tempfile

with tempfile.TemporaryDirectory(prefix="j2p-warm-") as folder:
    subprocess.run([sys.executable, str(pathlib.Path(__file__).parent / "warm/copied_run.py"),
        sys.argv[1], str(pathlib.Path(folder) / "result.json")], check=True)
