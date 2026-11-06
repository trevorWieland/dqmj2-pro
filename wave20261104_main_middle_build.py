import wave20261104_main_tail_proof as base
import wave20261104_main_middle_compiler as compiler
from wave20261104_main_middle_bindings import verify_original


def build(source, directory, negative=False):
    original = base.compiler
    original_verify = base.verify_original
    try:
        base.compiler = compiler
        base.verify_original = verify_original
        return base.build(source, directory, negative)
    finally:
        base.compiler = original
        base.verify_original = original_verify
