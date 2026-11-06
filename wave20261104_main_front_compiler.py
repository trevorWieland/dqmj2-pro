from pathlib import Path
import wave20261102_main_sdk_second_compiler as M
from project import ROOT, sha256

BASE_SHA = 'ab817d78e73c7214529f801993e6ee8be1d0a45fb57b290a258aebf73fb67c5b'
WORK = ROOT / 'work/w4af/c'
SOURCE = ROOT / 'src/runtime/parallel_wave20261104/main-arm-front'
FLAGS = M.FLAGS[:]
COMPILER = M.COMPILER
REGISTERS = M.REGISTERS


def compare(source, module, optimization, inline, speed=False, thumb=False, compiler=None, processor=None):
    source = Path(source).resolve()
    assert sha256(ROOT / 'wave20261102_main_sdk_second_compiler.py') == BASE_SHA
    assert module == 'main' and (source.is_relative_to(SOURCE) or source.is_relative_to(ROOT / 'work/w4af'))
    previous = M.WORK, M.FLAGS
    try:
        M.WORK, M.FLAGS = WORK, FLAGS
        return M.compare(source, module, optimization, inline, speed, thumb, compiler, processor)
    finally:
        M.WORK, M.FLAGS = previous
