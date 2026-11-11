"""Drive DeSmuME 0.9.13 non-interactively and capture ARM9 main RAM.

Why this exists
---------------
`docs/data/unbacked-data.md` proves the species roster (24-byte records at
`0x021c4bf8`) and the script-VM text block (`0x020fb264`) live in main BSS. BSS is
zero at load, so the only way to get those bytes is a dump taken from a running
instance in the right game state. `ops/ram_capture.py` validates and slices such a
dump but does not produce one; this wrapper produces it.

How the capture is made non-interactive
---------------------------------------
DeSmuME 0.9.13's Windows frontend has **no** command-line option to run a Lua
script (`--help` lists none; `--frameskip`, `--load-slot`, `--play-movie` are the
closest). It does, however, have a `[Scripting] AutoLoad` setting: on ROM load it
looks for `<lua path>\\<rom base name>.lua` and, when found, opens the Lua window
and sets the script path. Setting that edit control's text fires `EN_CHANGE`, whose
handler runs the script (`main.cpp` OpenCore -> CreateDialog + WM_SETTEXT;
`luaconsole.cpp` UpdateFileEntered -> PostMessage(IDC_BUTTON_LUARUN)). The default
Lua path is `<exe dir>\\Lua`, so a one-line shim there is enough.

The chain this wrapper performs:
  1. verify the emulator install and the Lua DLLs (see `--emulator`);
  2. copy the ROM and save into `work/emulator/scratch/` (inputs/ is never touched)
     and place the save where DeSmuME looks for it: `<exe dir>/Battery/<rom>.dsv`,
     re-wrapped in DeSmuME's `.dsv` footer (a bare raw image is read as empty);
  3. write `[Scripting] AutoLoad=1` into `desmume.ini`;
  4. write `<exe dir>/Lua/<rom>.lua`, a shim that dofiles `work/emulator/capture.lua`;
  5. launch DeSmuME on the scratch ROM with `--disable-sound`;
  6. wait for `capture.lua` to write the 1,929,792-byte window, then close the GUI;
  7. build a capture spec and hand the dump to `ops/ram_capture.py --check`, or
     `--slice` it into `extract/ram/` with a manifest fragment;
  8. print the roster sanity summary from the dump (heuristics, not proof).

Nothing here writes to `inputs/`, `manifest.json`, or `ledger/`. The ROM and save
are private; the dump stays under the gitignored `work/`.

Usage
-----
    # boot baseline (BSS still zero) - the pipeline test
    python ops/emulate_capture.py --name boot --frames 120

    # a scripted attempt at the monster roster, sliced and validated
    python ops/emulate_capture.py --name roster --frames 900 \
        --timeline "30:UP;10:A;240:" --slice

Exit codes: 0 success, 1 capture or validation failed, 2 install problem.
"""
import argparse
import ctypes
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import time
from ctypes import wintypes
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EMULATOR = ROOT / 'tools' / 'desmume' / '0.9.13-win64' / 'DeSmuME_0.9.13_x64.exe'
CAPTURE_LUA = ROOT / 'work' / 'emulator' / 'capture.lua'
SCRATCH = ROOT / 'work' / 'emulator' / 'scratch'
DUMPS = ROOT / 'work' / 'emulator' / 'dumps'
SPECS = ROOT / 'work' / 'emulator' / 'specs'

BASE = 0x02000000
LENGTH = 1929792  # 0x021D7240 - 0x02000000, the whole `main` module window
ROSTER_ADDRESS = 0x021C4BF8
ROSTER_BYTES = 360
ROSTER_STRIDE = 24
ROSTER_RECORDS = 15
SPECIES_OFFSET = 10
COUNT_OFFSET = 1
FIRST_OFFSET = 2
VM_ADDRESS = 0x020FB264
VM_BYTES = 4096
PROVEN_SPECIES = {139, 176, 188, 254, 350, 425, 426}

TOOL_NAME = ('DeSmuME 0.9.13 x64 SSE2 (official win64 release; lua51.dll + lua5.1.dll '
             'from the official 0.9.13 source tarball), Lua 5.1 capture.lua '
             '(memory.readbyterange)')

# DeSmuME .dsv = raw backup bytes + this footer (mc.cpp kDesmumeSaveCookie /
# DESMUME_BACKUP_FOOTER_TXT / BackupDevice::readFooter). A bare raw save is NOT
# recognised by the emulator: readFooter() fails, _info is zeroed and the file is
# treated as empty, so the game shows no save data. The footer carries
# (bytes written, padded size, save type, address width, memory size, version).
DSV_COOKIE = b'|-DESMUME SAVE-|'
DSV_FOOTER_TEXT = (b'|<--Snip above here to create a raw sav by excluding this '
                   b'DeSmuME savedata footer:')
# index into save_types[] (mc.cpp): 1=EEPROM 4kbit, 2=EEPROM 64kbit,
# 3=EEPROM 512kbit (64 KiB), 4=FRAM 256kbit, 5..=FLASH.
DSV_TYPE_BY_SIZE = {
    512: (1, 1),          # EEPROM 4kbit, 1-byte addresses
    8 * 1024: (2, 2),     # EEPROM 64kbit
    64 * 1024: (3, 2),    # EEPROM 512kbit
    32 * 1024: (4, 2),    # FRAM 256kbit
    256 * 1024: (5, 3),   # FLASH 2Mbit
    512 * 1024: (8, 3),   # FLASH 16Mbit
}


def dsv_bytes(raw):
    """Wrap a raw backup image in DeSmuME's .dsv footer."""
    if raw.endswith(DSV_COOKIE):
        return raw
    size = len(raw)
    if size not in DSV_TYPE_BY_SIZE:
        raise SystemExit(f'unsupported save size {size}; add its save type to DSV_TYPE_BY_SIZE')
    save_type, addr_size = DSV_TYPE_BY_SIZE[size]
    footer = DSV_FOOTER_TEXT + struct.pack('<6I', size, size, save_type, addr_size, size, 0) + DSV_COOKIE
    return raw + footer


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def manifest_rom_hash():
    try:
        manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8-sig'))
        return (manifest.get('rom') or {}).get('sha256')
    except (OSError, ValueError):
        return None


def print_step(message):
    print(f'[emulate] {message}')


def ensure_install(exe):
    problems = []
    if not exe.is_file():
        problems.append(f'emulator not found: {exe}\n'
                        f'  install the official desmume-0.9.13-win64.zip from\n'
                        f'  https://github.com/TASEmulators/desmume/releases/tag/release_0_9_13\n'
                        f'  and extract it so this path exists')
    for dll in ('lua51.dll', 'lua5.1.dll'):
        if exe.is_file() and not (exe.parent / dll).is_file():
            problems.append(f'missing {dll} next to the emulator: {exe.parent / dll}\n'
                            f'  0.9.13\'s zip omits both; extract desmume/src/frontend/windows/lua/lua.7z\n'
                            f'  (x64 folder) from the official desmume-0.9.13.tar.xz release')
    if not CAPTURE_LUA.is_file():
        problems.append(f'capture script not found: {CAPTURE_LUA}')
    if problems:
        for problem in problems:
            print(f'install problem: {problem}', file=sys.stderr)
        raise SystemExit(2)
    return exe


def ensure_ini_autoload(exe):
    """Set [Scripting] AutoLoad=1 without disturbing the rest of the settings file."""
    ini = exe.parent / 'desmume.ini'
    text = ini.read_text(encoding='utf-8', errors='replace') if ini.is_file() else ''
    if not re.search(r'^\[Scripting\]', text, re.M):
        text += '\n[Scripting]\nAutoLoad=1\n'
    elif re.search(r'^AutoLoad=', text, re.M):
        text = re.sub(r'^AutoLoad=\d+', 'AutoLoad=1', text, flags=re.M)
    else:
        text = re.sub(r'^(\[Scripting\][^\n]*\n)', r'\1AutoLoad=1\n', text, count=1, flags=re.M)
    ini.write_text(text, encoding='utf-8')
    if '[Scripting]' not in text or 'AutoLoad=1' not in text:
        raise SystemExit(f'failed to enable [Scripting] AutoLoad in {ini}')
    return ini


def prepare_scratch(exe, rom, save):
    SCRATCH.mkdir(parents=True, exist_ok=True)
    DUMPS.mkdir(parents=True, exist_ok=True)
    SPECS.mkdir(parents=True, exist_ok=True)

    rom_copy = SCRATCH / rom.name
    if not rom_copy.is_file() or rom_copy.stat().st_size != rom.stat().st_size:
        print_step(f'copying ROM to {rom_copy.relative_to(ROOT)} ({rom.stat().st_size} bytes)')
        rom_copy.write_bytes(rom.read_bytes())
    if sha256(rom_copy) != sha256(rom):
        raise SystemExit(f'ROM copy does not match {rom}; refusing to run')

    battery = exe.parent / 'Battery'
    battery.mkdir(exist_ok=True)
    save_copy = battery / (rom.stem + '.dsv')
    payload = dsv_bytes(save.read_bytes())
    if not save_copy.is_file() or save_copy.read_bytes() != payload:
        print_step(f'importing save to {save_copy} ({save.stat().st_size} raw bytes + '
                   f'{len(payload) - save.stat().st_size}-byte DeSmuME footer)')
        save_copy.write_bytes(payload)
    return rom_copy, save_copy


def write_shim(exe, rom):
    lua_dir = exe.parent / 'Lua'
    lua_dir.mkdir(exist_ok=True)
    shim = lua_dir / (rom.stem + '.lua')
    target = str(CAPTURE_LUA).replace('\\', '/')
    content = (f'-- generated by ops/emulate_capture.py; AutoLoad finds this next to the exe\n'
               f'dofile([[{target}]])\n')
    shim.write_text(content, encoding='ascii')
    return shim


# --- Win32 helpers (window lookup / graceful close / screenshot) -----------------

user32 = ctypes.WinDLL('user32', use_last_error=True)
EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
WM_CLOSE = 0x0010


def window_for_pid(pid):
    """Largest visible top-level window of `pid` (DeSmuME retitles to "Paused")."""
    found = []

    def callback(hwnd, _lparam):
        owner = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
        if owner.value == pid and user32.IsWindowVisible(hwnd):
            klass = ctypes.create_unicode_buffer(64)
            user32.GetClassNameW(hwnd, klass, 64)
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            area = (rect.right - rect.left) * (rect.bottom - rect.top)
            if klass.value == 'DeSmuME' and area > 0:
                found.append((area, hwnd))
        return True

    user32.EnumWindows(EnumWindowsProc(callback), 0)
    if not found:
        return None
    return max(found)[1]


def close_process(process, hwnd):
    if process.poll() is not None:
        return
    if hwnd:
        user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
        for _ in range(20):
            time.sleep(0.25)
            if process.poll() is not None:
                return
    process.kill()
    process.wait(timeout=10)


def screenshot_window(hwnd, path):
    """Save a PNG of the emulator window using PowerShell/System.Drawing."""
    rect = wintypes.RECT()
    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        print('[emulate] GetWindowRect failed for the emulator window', file=sys.stderr)
        return False
    width, height = rect.right - rect.left, rect.bottom - rect.top
    if width <= 0 or height <= 0:
        print(f'[emulate] emulator window has empty rect {width}x{height}', file=sys.stderr)
        return False
    script = f'''
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class Shot {{
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
}}
"@
[void][Shot]::SetForegroundWindow([IntPtr]{int(hwnd)})
Start-Sleep -Milliseconds 700
$bmp = New-Object System.Drawing.Bitmap {width}, {height}
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen({rect.left}, {rect.top}, 0, 0, $bmp.Size)
$bmp.Save('{path}', [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
'''
    command = ['powershell', '-NoProfile', '-NonInteractive', '-Command', script]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0 or not path.is_file():
        print(f'[emulate] screenshot failed: {result.stderr.strip()}', file=sys.stderr)
        return False
    return True


# --- capture ---------------------------------------------------------------------

def run_capture(args, exe, rom_copy):
    out = DUMPS / f'{args.name}.bin'
    log = DUMPS / f'{args.name}.log'
    out.unlink(missing_ok=True)
    log.unlink(missing_ok=True)

    env = dict(os.environ)
    env.update({
        'DQM_CAPTURE_OUT': str(out),
        'DQM_CAPTURE_LOG': str(log),
        'DQM_CAPTURE_FRAMES': str(args.frames),
        'DQM_CAPTURE_TIMELINE': args.timeline or '',
        'DQM_CAPTURE_EXIT': '0' if (args.pause or args.screenshot) else '1',
        'DQM_CAPTURE_LENGTH': str(args.dump_length),
    })
    if args.save_state is not None:
        env['DQM_CAPTURE_SAVESTATE'] = str(args.save_state)
    if args.load_state is not None:
        env['DQM_CAPTURE_LOADSTATE'] = str(args.load_state)
    if args.debug:
        env['DQM_CAPTURE_DEBUG'] = '1'
    if args.pause or args.screenshot:
        env['DQM_CAPTURE_PAUSE'] = '1'

    command = [str(exe), str(rom_copy), '--disable-sound']
    print_step(f'launching {exe.name} ({args.frames} frames, timeline={args.timeline!r})')
    started = time.time()
    process = subprocess.Popen(command, cwd=str(SCRATCH), env=env)

    timeout = args.timeout
    while time.time() - started < timeout:
        if out.is_file() and out.stat().st_size >= args.dump_length:
            time.sleep(0.8)  # let the script log its last line / settle
            break
        if process.poll() is not None:
            break
        time.sleep(0.25)

    elapsed = time.time() - started
    hwnd = window_for_pid(process.pid)
    if args.screenshot and hwnd:
        if screenshot_window(hwnd, Path(args.screenshot)):
            print_step(f'screenshot written to {args.screenshot}')
        else:
            print('[emulate] continuing without a screenshot', file=sys.stderr)
    close_process(process, hwnd)

    if log.is_file():
        for line in log.read_text(encoding='utf-8', errors='replace').splitlines():
            if line.strip():
                print(f'  {line}')
    if not out.is_file():
        print(f'capture failed: no dump after {elapsed:.1f}s (emulator exited?)', file=sys.stderr)
        return None
    size = out.stat().st_size
    print_step(f'dump {out.relative_to(ROOT)} {size} bytes in {elapsed:.1f}s sha256 {sha256(out)[:16]}…')
    if size != args.dump_length:
        print(f'capture failed: dump is {size} bytes, expected {args.dump_length}', file=sys.stderr)
        return None
    return out


def roster_summary(dump):
    data = dump.read_bytes()
    offset = ROSTER_ADDRESS - BASE
    block = data[offset:offset + ROSTER_BYTES]
    records = []
    for index in range(ROSTER_RECORDS):
        record = block[index * ROSTER_STRIDE:(index + 1) * ROSTER_STRIDE]
        species = int.from_bytes(record[SPECIES_OFFSET:SPECIES_OFFSET + 2], 'little', signed=True)
        records.append({
            'index': index,
            'species': species,
            'plausible': species in PROVEN_SPECIES,
            'count': record[COUNT_OFFSET],
            'first': int.from_bytes(record[FIRST_OFFSET:FIRST_OFFSET + 1], 'little', signed=True),
            'zero': all(byte == 0 for byte in record),
            'ff': all(byte == 0xFF for byte in record),
        })
    vm = data[VM_ADDRESS - BASE:VM_ADDRESS - BASE + VM_BYTES]
    populated = sum(1 for r in records if not r['zero'] and not r['ff'])
    plausible = sum(1 for r in records if r['plausible'])
    print_step(f'roster 0x{ROSTER_ADDRESS:08x}: {populated}/15 non-empty records, '
               f'{plausible}/15 species in the proven set {sorted(PROVEN_SPECIES)}')
    for record in records:
        print(f'    [{record["index"]:2d}] species={record["species"]:5d} '
              f'{ "plausible" if record["plausible"] else "         " } '
              f'count={record["count"]:3d} first={record["first"]:3d}'
              f'{ "  ALL-ZERO" if record["zero"] else ""}{ "  ALL-FF" if record["ff"] else ""}')
    print_step(f'scriptvm 0x{VM_ADDRESS:08x}: {sum(1 for b in vm if b)}/4096 non-zero bytes, '
               f'cursor@+0x80={vm[0x80]}')
    return {'records': records, 'populated': populated, 'plausible': plausible,
            'vmNonZero': sum(1 for b in vm if b), 'cursor': vm[0x80]}


def write_spec(args, dump, rom_hash):
    capture_point = args.capture_point or (
        f'DeSmuME 0.9.13 Lua capture: {args.frames} frames'
        + (f' then timeline {args.timeline!r}' if args.timeline else '')
        + (f', loaded state slot {args.load_state}' if args.load_state is not None else '')
    )
    spec = {
        'dump': str(dump.relative_to(ROOT)).replace('\\', '/'),
        'dumpBase': hex(BASE),
        'module': 'main',
        'provenance': {
            'buildSha256': rom_hash,
            'tool': TOOL_NAME,
            'capturePoint': capture_point,
            'timestampUtc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        },
        'captures': [
            {'name': 'ram-roster', 'address': hex(ROSTER_ADDRESS), 'bytes': ROSTER_BYTES},
            {'name': 'ram-scriptvm', 'address': hex(VM_ADDRESS), 'bytes': VM_BYTES},
        ],
    }
    path = SPECS / f'{args.name}.json'
    path.write_text(json.dumps(spec, indent=2) + '\n', encoding='utf-8')
    print_step(f'spec written to {path.relative_to(ROOT)}')
    return path


def validate(spec, slice_):
    command = [sys.executable, str(ROOT / 'ops' / 'ram_capture.py'), '--spec', str(spec)]
    if not slice_:
        command.append('--check')
    result = subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True)
    for line in (result.stdout + result.stderr).splitlines():
        if line.strip():
            print(f'  ram_capture: {line.rstrip()}')
    if result.returncode != 0:
        print(f'ram_capture rejected the dump (exit {result.returncode})', file=sys.stderr)
        return False
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--name', required=True, help='capture name (dump/spec file stem)')
    parser.add_argument('--frames', type=int, default=300,
                        help='frames to advance before the timeline (default 300)')
    parser.add_argument('--timeline', default='',
                        help='button timeline "FRAMES:BUTTONS;..." e.g. "30:UP;10:A;240:"')
    parser.add_argument('--rom', default='inputs/game.nds', help='private ROM (never modified)')
    parser.add_argument('--save', default='inputs/save.sav', help='private save (never modified)')
    parser.add_argument('--emulator', default=str(DEFAULT_EMULATOR))
    parser.add_argument('--capture-point', default=None,
                        help='provenance sentence describing the in-game state')
    parser.add_argument('--dump-length', type=int, default=LENGTH,
                        help='bytes to dump from 0x02000000 (default 1929792; use 4194304 for all main RAM)')
    parser.add_argument('--timeout', type=float, default=300.0, help='seconds before giving up')
    parser.add_argument('--save-state', type=int, default=None, help='write DeSmuME state slot N')
    parser.add_argument('--load-state', type=int, default=None, help='load DeSmuME state slot N')
    parser.add_argument('--debug', action='store_true',
                        help='log joypad readback from the Lua script')
    parser.add_argument('--pause', action='store_true',
                        help='pause the emulator after dumping instead of exiting')
    parser.add_argument('--screenshot', default=None, help='PNG path for the captured frame')
    parser.add_argument('--slice', action='store_true',
                        help='slice into extract/ram and emit the manifest fragment')
    parser.add_argument('--no-validate', action='store_true', help='skip ops/ram_capture.py')
    args = parser.parse_args(argv)

    rom = (ROOT / args.rom).resolve()
    save = (ROOT / args.save).resolve()
    if not rom.is_file() or not save.is_file():
        print(f'inputs not found: {rom} / {save}', file=sys.stderr)
        return 1

    exe = ensure_install(Path(args.emulator).resolve())
    ensure_ini_autoload(exe)
    rom_copy, _save_copy = prepare_scratch(exe, rom, save)
    write_shim(exe, rom_copy)

    rom_hash = manifest_rom_hash() or sha256(rom)
    dump = run_capture(args, exe, rom_copy)
    if dump is None:
        return 1

    summary = roster_summary(dump)
    spec = write_spec(args, dump, rom_hash)
    if not args.no_validate and not validate(spec, args.slice):
        return 1

    if summary['populated'] == ROSTER_RECORDS and summary['plausible'] >= 7:
        print_step('roster looks POPULATED (15 non-empty records, several proven species)')
    else:
        print_step('roster is NOT proven populated; dump is still a valid pipeline capture')
    return 0


if __name__ == '__main__':
    sys.exit(main())
