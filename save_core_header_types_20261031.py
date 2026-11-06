import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT),str(ROOT/'deps/native')]
from link_runtime_unit import measured_module


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def prepare():
    original = ROOT/'nonmatching/save-core/20261030-save-operations'
    base = (original/'native_main_0207979c_pointer_before.c').read_text()
    header = (original/'save_operations_types_20261030.h').read_text()
    variants = {}
    variants['void'] = (base.replace('u32 native_main_','void native_main_').replace('return 6;','return;').replace('return (count + 3) * 2;','return;'),header,None)
    variants['signed_return'] = (base.replace('u32 native_main_','int native_main_'),header,None)
    switch = base.replace('if (valid == 0) {','switch (valid) {\n    case 0:').replace('    count = summary->rawCount;','    default:\n    count = summary->rawCount;').replace('    return (count + 3) * 2;\n}', '    return (count + 3) * 2;\n    }\n}')
    switch = switch.replace('        return 6;\n    }','        return 6;')
    variants['switch'] = (switch,header,None)
    common = '''#include "save_operations_types_20261030.h"
u32 native_main_0207979c(void) {
    SaveHeaderSummary *summary = &native_data_021c65d0;
    u8 valid = native_fn_0207df2c(0,native_data_021c65a8);
    int second;
    native_data_021c6544.headerValid = valid;
    if (valid) {
        int count = summary->rawCount;
        native_data_021c6544.first = (3-count)*2+11;
        second = (count+3)*2;
        native_data_021c6544.second = second;
    } else {
        native_data_021c6544.first = 17;
        second = 6;
        native_data_021c6544.second = second;
    }
    return second;
}
'''
    variants['if_else'] = (common,header,None)
    count = '''#include "save_operations_types_20261030.h"
u32 native_main_0207979c(void) {
    SaveHeaderSummary *summary = &native_data_021c65d0;
    u8 valid = native_fn_0207df2c(0,native_data_021c65a8);
    int count = valid ? summary->rawCount : 0;
    native_data_021c6544.headerValid = valid;
    native_data_021c6544.first = (3-count)*2+11;
    native_data_021c6544.second = (count+3)*2;
    return (count+3)*2;
}
'''
    variants['conditional_count'] = (count,header,None)
    variants['reader_byte_return'] = (base,header.replace('extern int native_fn_0207df2c','extern u8 native_fn_0207df2c'),None)
    full = header.replace('    u8 rawCount;','    u8 rawCount;\n    u8 reserved86[2];\n    u32 payloadChecksum;\n    u32 headerChecksum;')
    variants['full_summary_prefix'] = (base,full,None)
    inline = '''static inline u32 set_header_layout(SaveOperationState *state,int first,int second) {
    state->first = first;
    state->second = second;
    return second;
}
'''
    body = base.replace('    native_data_021c6544.first = (3 - count) * 2 + 11;\n    native_data_021c6544.second = (count + 3) * 2;\n    return (count + 3) * 2;','    return set_header_layout(&native_data_021c6544,(3-count)*2+11,(count+3)*2);').replace('        native_data_021c6544.first = 17;\n        native_data_021c6544.second = 6;\n        return 6;','        return set_header_layout(&native_data_021c6544,17,6);')
    body = body.replace('u32 native_main_',inline+'u32 native_main_')
    variants['inline_layout_return'] = (body,header,'smart')
    inline_void = body.replace('static inline u32 set_header_layout','static inline void set_header_layout').replace('    return second;\n}', '    return;\n}')
    inline_void = inline_void.replace('return set_header_layout(&native_data_021c6544,17,6);','set_header_layout(&native_data_021c6544,17,6);\n        return 6;').replace('return set_header_layout(&native_data_021c6544,(3-count)*2+11,(count+3)*2);','set_header_layout(&native_data_021c6544,(3-count)*2+11,(count+3)*2);\n    return (count+3)*2;')
    variants['inline_layout_void'] = (inline_void,header,'smart')
    variants['buffer_subobject'] = (base.replace('&native_data_021c65d0','(SaveHeaderSummary *)(native_data_021c65a8+0x28)'),full,None)
    arm = measured_module('main')[1]
    native = arm[0x7979C:0x79800]
    jobs = []
    for name,(source,types,inline_mode) in variants.items():
        folder = ROOT/'nonmatching/save-core/20261031-save-header-types'/name
        folder.mkdir(parents=True,exist_ok=True)
        p = folder/'native_main_0207979c.c'
        p.write_text(source)
        (folder/'save_operations_types_20261030.h').write_text(types)
        work = ROOT/'work/save-core-lane/20261031-header-types'/name
        work.mkdir(parents=True,exist_ok=True)
        job = dict(module='main',mode='arm',address='0x0207979C',bytes=100,alias='func_0207979c',
            source=p.relative_to(ROOT).as_posix(),work=work.relative_to(ROOT).as_posix(),inlineMode=inline_mode,
            nativeSpanSha256=sha(native),acceptedSourceCredit=0,priorSourceSha256=sha((original/'native_main_0207979c_pointer_before.c').read_bytes()))
        jobs.append(job)
    return jobs


def run(job):
    path = ROOT/job['work']/'job.json'
    path.write_text(json.dumps(job,indent=2)+'\n')
    process = subprocess.run([sys.executable,str(ROOT/'evidence/application/save_core_header_type_worker_20261031.py'),str(path)],
        capture_output=True,text=True,cwd=ROOT,timeout=180)
    if process.returncode:
        return dict(job,failure=process.stderr,sourceCredit=0)
    return json.loads((path.parent/'result.json').read_text())


def main():
    jobs = prepare()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(run,jobs))
    report = dict(schemaVersion=1,sourceCredit=0,functions=rows,
        counts=dict(naturalSourceHypotheses=len(rows),compilable=sum(r.get('compilable',False) for r in rows),
            exactCandidates=sum(r.get('byteExactCandidate',False) for r in rows)),
        limits=['Ten natural control-flow/return/dependency-type/inline-view hypotheses with at most three isolated compiler processes. Each has independent header/source/profile WORK outputs. Original100-byte wrapper and frozen96-byte hypothesis remain unchanged. Full-summary prefix adds the measured bank88/8C checksum words; opaque bytes and index semantics are unclassified. No volatile,forced registers,assembly,opcode patches,fake arguments or source credit.'])
    path = ROOT/'evidence/attempts/save-core-header-types-20261031.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['counts']))
    for r in rows:
        print(r['source'],[(a.get('compiledBytes'),a.get('sameOffsetBytes'),a.get('byteExact')) for a in r.get('compileAttempts',[])])


if __name__=='__main__':
    main()
