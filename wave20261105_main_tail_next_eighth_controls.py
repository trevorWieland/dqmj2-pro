import copy
import os
import shutil
import subprocess
from project import ROOT, sha256
import match_runtime as C
from wave20261105_main_tail_next_eighth_bindings import verify_original, negative_controls
from wave20261105_main_tail_next_compiler import COMPILER


def execute(rows):
    checks = negative_controls(rows)['negativeCases']
    for row in rows:
        names = [symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function']
        if not names:
            continue
        for symbol in names:
            for label, key, value in [('wrong-mode', 'mode', 'thumb'), ('function-as-data', 'kind', 'data'),
                                      ('same-address-wrong-overlay', 'module', 'ov000'), ('wrong-address', 'address', '0x203b8e0'),
                                      ('wrong-CPU', 'processor', 'arm7'), ('wrong-program', 'program', 'child')]:
                bindings = copy.deepcopy(row['nativeSymbolEntries'])
                bindings[symbol][key] = value
                try:
                    verify_original(row, bindings)
                except ValueError as error:
                    checks.append(dict(caller=row['address'], case=label, rejected=True, reason=str(error)))
                else:
                    raise ValueError('Invalid measured resource callee identity accepted')
    for row in rows:
        verify_original(row, row['nativeSymbolEntries'])
    directory = ROOT / 'work/w5tn/eighth-controls/layout'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / 'src/runtime/parallel_wave20261105/main-tail-next/eighth/context.h'
    shutil.copyfile(header, directory / 'context.h')
    source = directory / 'layout.c'
    source.write_text('#include "context.h"\n')
    output = directory / 'layout.o'
    command = [str(COMPILER), *C.FLAGS, '-opt', 'speed', '-c', str(source), '-o', str(output)]
    environment = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
    if process.returncode:
        raise ValueError(('Native pointer-field layout assertions failed', process.stdout, process.stderr))
    positive = dict(compilerSha256=sha256(COMPILER),headerSha256=sha256(header),sourceSha256=sha256(source),objectSha256=sha256(output),exitCode=0,facts=['word32','pointer32','RecordStride6','SignedId16At0','UnsignedVariantAt2','UnsignedCategoryAt4','BorrowedByteStride6'])
    failures = []
    for label, old, new in [('wrong-record-stride','u8 opaque5;','u8 opaque5[2];'),('wrong-category-offset','u8 opaque3;','u8 opaque3[2];'),('wrong-byte-stride','u8 opaque1[5]','u8 opaque1[4]')]:
        if header.read_text().count(old) != 1:
            raise ValueError('Pointer-field layout mutation ambiguous')
        (directory / 'context.h').write_text(header.read_text().replace(old, new))
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=60)
        if not process.returncode or 'illegal constant expression' not in process.stdout:
            raise ValueError(('Wrong native signed field/offset accepted', process.stdout, process.stderr))
        failures.append(dict(case=label, rejected=True, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
    return dict(status='passed', sourceCredit=0, bindingControls=checks, nativeCompilerLayout=positive, wrongNativeLayouts=failures, signedCursorAbi=signed_abi(header, directory))


def signed_abi(header,directory):
    import match_runtime as C
    import unicorn
    from unicorn import arm_const as R
    from elftools.elf.elffile import ELFFile
    source=directory/'signed.c'
    source.write_text('#include "context.h"\ns32 abi_id(ChoiceRecord *p) { return p->id0; }\n')
    output=directory/'signed.o'
    command=[str(COMPILER),*C.FLAGS,'-opt','speed','-c',str(source),'-o',str(output)]
    environment=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))

    def probe(text):
        (directory/'context.h').write_text(text)
        process=subprocess.run(command,cwd=ROOT,env=environment,capture_output=True,text=True,timeout=60)
        if process.returncode:raise ValueError(('Signed16 ABI probe compile failed',process.stdout,process.stderr))
        with output.open('rb') as stream:
            elf=ELFFile(stream)
            symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name=='abi_id')
            body=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM)
        vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
        vm.mem_map(0x02300000,0x2000)
        vm.mem_write(0x02300000,body)
        records=[]
        for value in [0,1,127,128,255,32767,32768,65534,65535]:
            vm.mem_write(0x02301000,value.to_bytes(2,'little')+bytes(4))
            vm.reg_write(R.UC_ARM_REG_R0,0x02301000)
            vm.reg_write(R.UC_ARM_REG_LR,0x02300800)
            vm.reg_write(R.UC_ARM_REG_SP,0x02301f00)
            vm.emu_start(0x02300000,0x02300800,count=100)
            result=vm.reg_read(R.UC_ARM_REG_R0)
            expected=(value if value<32768 else value-65536)&0xffffffff
            if result!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02300800:raise ValueError(('Signed16 ABI differs',value,result,expected))
            records.append(dict(halfword=value,returned=result))
        return dict(actualNativeAbiProbeReturns=len(records),cases=records,sourceSha256=sha256(source),objectSha256=sha256(output),originalGameOrCalleeBodiesExecuted=0)

    text=header.read_text()
    positive=probe(text)
    try:probe(text.replace('s16 id0;','u16 id0;'))
    except ValueError as error:negative=dict(case='wrong-unsigned-id',rejected=True,reason=str(error))
    else:raise ValueError('Wrong unsigned16 ABI accepted')
    return dict(status='passed',positive=positive,negative=negative,sourceCredit=0)
