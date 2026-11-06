import wave20261104_main_tail_proof as base
import wave20261105_main_tail_next_compiler as compiler
from wave20261105_main_tail_next_fifth_bindings import verify_original


def build(source, directory, negative=False):
    original, original_verify = base.compiler, base.verify_original
    try:
        base.compiler, base.verify_original = compiler, verify_original
        return base.build(source, directory, negative)
    finally:
        base.compiler, base.verify_original = original, original_verify
