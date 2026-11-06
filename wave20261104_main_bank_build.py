import wave20261104_main_tail_proof as base
import wave20261104_main_bank_compiler as compiler


def build(source, directory, negative=False):
    original = base.compiler
    try:
        base.compiler = compiler
        return base.build(source, directory, negative)
    finally:
        base.compiler = original
