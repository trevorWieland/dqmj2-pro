from project import ROOT,read_json,sha256
from wave20261104_main_tail_bindings import verify_original as original_branches
import native_alternate_entries as P

TABLE_SHA='682fff32f31d58251ae9a734ab15e0ffc8a6ffa92c26ecefad4e861860352377'
REPORT_SHA='b7c519e8bc67cba5d1b2833577413693c827d00a7ef49a3575cdb021be56b843'

def verify_original(row,bindings):
    if sha256(P.TABLE)!=TABLE_SHA or sha256(ROOT/'evidence/entrypoints/main-unsigned64-entry-20261030.json')!=REPORT_SHA:raise ValueError('Existing activated unsigned64 certificate/table changed')
    if [(r['offset'],r['type'],r['symbol'],r['target'],r['addend']) for r in row['relocations']]!=[(360,1,'native_fn_020260e8','0x20260e8',-8),(384,1,'native_fn_020260dc','0x20260dc',-8)]:raise ValueError('Explicit measured unsigned64 native call contract differs')
    result=original_branches(row,bindings);proof=P.verify('native_fn_020260e8',bindings['native_fn_020260e8'])
    return dict(result,existingAlternateEntry=proof,sourceMethod='Explicit typed C remainder/quotient calls through existing activated measured ABI; no object symbol patch or new entry policy',calleeSourceExtentCredit=0)
