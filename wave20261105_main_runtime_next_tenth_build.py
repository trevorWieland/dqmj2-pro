import wave20261104_main_tail_proof as base
import wave20261105_main_runtime_next_tenth_compiler as compiler
from wave20261105_main_runtime_next_tenth_bindings import verify_original


def build(source, directory, negative=False):
    old_compiler, old_verify = base.compiler, base.verify_original
    try:
        base.compiler, base.verify_original = compiler, verify_original
        return base.build(source, directory, negative)
    finally:
        base.compiler, base.verify_original = old_compiler, old_verify
