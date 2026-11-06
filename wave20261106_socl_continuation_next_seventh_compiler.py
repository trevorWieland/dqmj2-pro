from project import ROOT,sha256
import wave20261106_socl_continuation_next_compiler as original
C=original.C

COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/sp1p6/mwccarm.exe'
COMPILER_SHA='2819dea7ae847ff83699d18bbc567238abe2804b6783b3bcc5893c5e546b0334'


def compare(source,directory):
    if sha256(COMPILER)!=COMPILER_SHA:raise ValueError('Measured sp1p6 compiler changed')
    if sum(source.read_text().count('native_main_'+n+'(')for n in ['020909c8','02090a3c','02090ae8'])!=1:raise ValueError('Exactly one admitted seventh-packet caller required')
    previous=original.COMPILER
    try:
        original.COMPILER=COMPILER
        return original.compare(source,directory)
    finally:original.COMPILER=previous
