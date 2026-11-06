import gzip
import hashlib
import json
import os
import random
import struct
import subprocess
from project import ROOT,read_json,write_json,sha256
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA, LINKER_SHA, DLLTOOL_SHA

WORK = ROOT/'work/fifo-closed876-windows32-20261101'


def scenario(entry,index):
    rng = random.Random(entry*100000+index)
    pages = [bytearray(rng.randbytes(4096))for unused in range(2)]
    if entry == 0x0200A440:
        values = [0,1,31,32,0x03FFFFFF,0x04000000,0x80000000,0xFFFFFFFF,rng.getrandbits(32)]
        channel,payload,flag = values[index%9],values[index//9%9],values[index//81%9]
        status = [0,2,0x4000,0x4002,0x8000,0x8002,0xC000,0xFFFF][index//3%8]
        struct.pack_into('<H',pages[1],0x184,status)
        registers = [rng.getrandbits(32)for unused in range(13)]
        registers[:3] = [channel,payload,flag]
    elif entry in [0x0200DDF4,0x0200DFD8]:
        registers = [rng.getrandbits(32)for unused in range(13)]
        callback = 0 if index%3 == 0 else 0x0200A440
        before_flags = [0,1,4,0xFFFF,0x8000,rng.getrandbits(16)][index//3%6]
        before_ack = [0,1,4,0xFFFF,0x8000,rng.getrandbits(16)][index//5%6]
        status = [0,2,0x4000,0x4002,0x8000,0x8002,0xC000,0xFFFF][index//2%8]
        struct.pack_into('<I',pages[0],0x3D4,callback)
        struct.pack_into('<HH',pages[0],0x408,before_flags,before_ack)
        struct.pack_into('<H',pages[1],0x184,status)
    else:
        values = [0,1,0xFFFFFFFF,0x80000000,0x7FFFFFFF,rng.getrandbits(32)]
        registers = [rng.getrandbits(32)for unused in range(13)]
        registers[:4] = [values[(index//4+slot)%len(values)]for slot in range(4)]
        busy = [0,1,0xFFFFFFFF,0][index%4]
        status = [0,2,0x4000,0x4002,0x8000,0x8002,0xC000,0xFFFF][index//4%8]
        struct.pack_into('<I',pages[0],0x444,busy)
        struct.pack_into('<H',pages[1],0x184,status)
    cpsr = (index%16<<28)|0x1F|(index//2%2<<7)|(index//7%2<<6)
    return pages,registers,cpsr


def main():
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    clang, linker, dlltool = [tools / name for name in ['clang.exe', 'ld.lld.exe', 'llvm-dlltool.exe']]
    assert [sha256(path) for path in [clang, linker, dlltool]] == [CLANG_SHA, LINKER_SHA, DLLTOOL_SHA]
    WORK.mkdir(parents=True, exist_ok=True)
    environment = {key: value for key, value in os.environ.items()
                   if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    steps = []

    def run(command, data=None, timeout=120):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT, env=environment, input=data, capture_output=True,
                                timeout=timeout, creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=result.returncode,
            stdoutSha256=hashlib.sha256(result.stdout).hexdigest(), stderr=result.stderr.decode(errors='replace')))
        assert result.returncode == 0, steps[-1]
        return result

    definition = WORK / 'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\n', encoding='ascii')
    library = WORK / 'kernel32.lib'
    run([dlltool, '-m', 'i386', '-k', '-d', definition, '-l', library])
    sources = [ROOT/'ports/windows-native/fifo_closed876_runner_20261101.c']
    sources += [ROOT/f'src/runtime/20261101_fifo_requests352/native_main_{entry:08x}.c'for entry in [0x0200F370,0x0200F418,0x0200F4C4]]
    sources += [ROOT/'src/runtime/20261101_fifo_send136/native_main_0200a440.c']
    sources += [ROOT/f'src/runtime/20261101_fifo_ack300/native_main_{entry:08x}.c'for entry in [0x0200DDF4,0x0200DFD8]]
    sources += [ROOT/f'src/runtime/runtime08/native_main_{entry:08x}.c'for entry in [0x0200FB60,0x0200FB70,0x0200FB80,0x0200FBA0]]
    objects = []
    for number,source in enumerate(sources):
        obj = WORK/f'source-{number:02}.obj'
        run([clang,'--target=i686-pc-windows-msvc','-std=c11','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector',
            '-fno-strict-aliasing','-Wno-incompatible-pointer-types','-Wno-int-conversion','-c',source,'-o',obj])
        objects.append(obj)
    aliases = [0x0200A440,0x0200FB60,0x0200FB70,0x0200FB80,0x0200FBA0]
    executable = WORK/'fifo-closed.exe'
    run([linker,'-flavor','link','/machine:x86','/subsystem:console','/nodefaultlib','/entry:j2p_entry',
        '/safeseh:no','/fixed','/dynamicbase:no','/timestamp:0','/manifest:embed',
        "/manifestuac:level='asInvoker' uiAccess='false'",'/out:'+str(executable),
        *[f'/alternatename:_native_fn_{entry:08x}=_native_main_{entry:08x}'for entry in aliases],*objects,library])
    binary = executable.read_bytes();pe = struct.unpack_from('<I',binary,0x3C)[0]
    assert binary[pe:pe+4] == b'PE\0\0' and struct.unpack_from('<H',binary,pe+4)[0] == 0x14C
    assert struct.unpack_from('<H',binary,pe+24)[0] == 0x10B and b'asInvoker'in binary
    oracles,originals = [],{}
    for family in ['requests352-v2','send136','ack300']:
        path = ROOT/f'evidence/matches/main-fifo-{family}-20261101.json'
        data = path.read_bytes();archive = ROOT/'evidence/portability/oracles'/('fifo-'+hashlib.sha256(data).hexdigest()+'.json')
        archive.parent.mkdir(parents=True,exist_ok=True)
        if archive.exists():assert archive.read_bytes() == data
        else:archive.write_bytes(data)
        report = read_json(archive);trace = report['oracle']['traceArchive']
        assert sha256(ROOT/report['fixture']) == report['fixtureSha256']
        assert sha256(ROOT/trace['path']) == trace['sha256']
        records = json.loads(gzip.decompress((ROOT/trace['path']).read_bytes()))
        if family == 'send136':
            for row in records['direct']:originals[0x0200A440,row['index']] = row['original']
        else:
            for row in records:originals[int(row['entry'],0),row['original']['index']] = row['original']
        oracles.append(dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive)))
    assert len(originals) == 2688
    payload = bytearray(struct.pack('<3I',0x4A324649,1,len(originals)));expected = []
    for (entry,index),record in sorted(originals.items()):
        pages,registers,cpsr = scenario(entry,index)
        payload.extend(struct.pack('<7I',entry,index,*registers[:4],cpsr));payload.extend(b''.join(pages))
        events = [(address,args[0]if args else 0)for address,args in record['calls']if address in [0x02007FF4,0x02008008]]
        event_words = [value for pair in events for value in pair];event_words += [0]*(16-len(event_words))
        expected.append((entry,index,record['result'],record['cpsr']&0xFF,len(events),event_words,record['pagesSha256']))
    output = run([executable],bytes(payload),timeout=180).stdout
    repeat = run([executable],bytes(payload),timeout=180).stdout
    assert output == repeat
    stride = 20+64+8192
    assert output[:12] == payload[:12] and len(output) == 12+len(expected)*stride
    failures = []
    for position,row in enumerate(expected):
        offset = 12+position*stride
        actual = struct.unpack_from('<5I',output,offset)
        events = list(struct.unpack_from('<16I',output,offset+20))
        digest = hashlib.sha256(output[offset+84:offset+84+8192]).hexdigest()
        if actual != row[:5] or events != row[5] or digest != row[6]:
            failures.append(dict(entry=hex(row[0]),index=row[1],actualHeader=list(actual),expectedHeader=list(row[:5]),pageHashMatches=digest==row[6],irqEventsMatch=events==row[5]))
    report = dict(generator=__file__.split(chr(92))[-1],generatorSha256=sha256(__file__),
        actualWindowsNativeUniqueCalls=2688,repeatedFreshProcessRuns=2,sourceRoutineBodies=10,sourceRoutineNativeInitializedBytes=876,
        newFifoSourceBytesWithinThatClosure=788,previouslyMatchedHelperBytes=88,sourceCredit=0,
        armEmulationInNativeProcess=False,originalArmCodeOrRomSaveInputsInNativeProcess=False,
        memoryComparisonBytesPerCall=8192,fullPageOrIrqFailures=failures,oracles=oracles,
        sources=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in sources],
        tools=dict(clangSha256=CLANG_SHA,linkerSha256=LINKER_SHA,dlltoolSha256=DLLTOOL_SHA),
        executable=dict(path=executable.relative_to(ROOT).as_posix(),sha256=sha256(executable)),steps=steps,
        platformAdapters=['Single-thread IRQ control-mask C state machine','Private fixed-address register byte pages','Explicit original callback ID to host function mapping and logical pointer-return mapping'],
        suppliedHelperOutcomes=0,fullWindowsGameBuilt=False,androidDeviceExecutions=0,
        limitations=['Actual PE32 execution on Windows with32-bit pointers and exact low-address private pages',
            'IRQ control state and call sequence are compared to ARM evidence; physical ARM interrupts are not implemented',
            'Synthetic register snapshots prove written bytes, not physical FIFO/W1C behavior or asynchronous ARM7 delivery',
            'All final page bytes are hashed; Windows instruction/store ordering and raw ARM registers are not equated',
            'No concurrency, scene availability, Android device or full-game proof'])
    write_json(ROOT/'evidence/portability/fifo-closed876-windows32-20261101.json',report)
    assert not failures,failures[:8]
    print(dict(windowsNativeCalls=2688,sourceRoutines=10,sourceBytes=876,fullPageOrIrqFailures=0,sourceCredit=0))


if __name__ == '__main__':main()
