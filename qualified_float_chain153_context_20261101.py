import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent
REPORT='evidence/abi/main-signed-double-chain601-20261101.json'
REPORT_SHA='31791acb42e7d9af9f22c7de1f3d4d515dc989939b0edb0b7aaf5c31df657e3a'


def catalogue():
    raw=(ROOT/REPORT).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==REPORT_SHA
    report=json.loads(raw)
    assert report['module']=='main' and report['processor']=='arm9' and report['providedCalls']==0
    assert report['actualProperTopReturns']==1350 and report['definedCastChains']==360
    assert report['nativeOnlyOverflowChains']==83
    return [dict(alias=alias,returnType=kind,contextPrototype=prototype,report=REPORT,reportSha256=REPORT_SHA,
        qualification='Measured native binary64 word-pair ABI;semantic evidence only for frozen signed32-derived times1.5 and listed finite conversions')
        for alias,kind,prototype in [
            ('func_020244c4','f64','extern f64 func_020244c4(s32);'),
            ('func_02024540','f64','extern f64 func_02024540(f64, f64);'),
            ('func_02024394','s32','extern s32 func_02024394(f64);')]]


def apply(context,module='main',processor='arm9'):
    assert module=='main' and processor=='arm9'
    changes=[]
    for item in catalogue():
        pattern=r'^extern[^;\n]*\b'+item['alias']+r'\([^;\n]*\);'
        old=re.findall(pattern,context,re.M)
        if old:
            assert len(old)==1
            context=re.sub(pattern,item['contextPrototype'],context,flags=re.M)
            changes.append(dict(item,oldDeclaration=old[0]))
    return context,changes
