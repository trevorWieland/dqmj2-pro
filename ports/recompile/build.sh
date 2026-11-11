#!/usr/bin/env bash
# Build the standalone recompilation stub with the pinned Metrowerks toolchain.
#
# This is the POSIX twin of build.ps1; both produce the same objects and link the same ELF.
# Usage:
#   ./ports/recompile/build.sh [toolchain-dir] [out-dir]
# Defaults: tools/mwccarm/mwccarm/2.0/base and build/recompile.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tool="${1:-$root/tools/mwccarm/mwccarm/2.0/base}"
out="${2:-$root/build/recompile}"
mkdir -p "$out"

cc="$tool/mwccarm.exe"
as="$tool/mwasmarm.exe"
ld="$tool/mwldarm.exe"
for exe in "$cc" "$as" "$ld"; do
    [ -x "$exe" ] || [ -f "$exe" ] || { echo "missing pinned tool: $exe" >&2; exit 1; }
done

# Metrowerks looks for its libraries through these variables. MWLibraries is a directory and is
# accepted as-is; MWLibraryFiles is a LIST of archive names, not a directory (pointing it at a
# directory splits on the drive colon), so this flat image links no Metrowerks runtime and leaves
# it unset.
export MWLibraries="$tool"
unset MWLibraryFiles || true
[ -f "$root/tools/mwccarm/mwccarm/license.dat" ] && export LM_LICENSE_FILE="$root/tools/mwccarm/mwccarm/license.dat"

cflags=(-O2 -enum int -char signed -str noreuse -proc arm946e -gccext,on -fp soft -inline off
        -Cpp_exceptions off -RTTI off -interworking -w off -sym on -gccinc -nolink -msgstyle gcc)

"$cc" "${cflags[@]}" -c "$root/src/main/p3g_main_02000c34/native_main_02000c34.c" -o "$out/main.o"
echo "compiled  src/main/p3g_main_02000c34/native_main_02000c34.c -> $out/main.o"
"$cc" "${cflags[@]}" -c "$root/src/main/p3g_main_02000c34/native_main_020c225c.c" -o "$out/boot.o"
echo "compiled  src/main/p3g_main_02000c34/native_main_020c225c.c -> $out/boot.o"
"$cc" "${cflags[@]}" -c "$root/ports/recompile/stubs.c" -o "$out/stubs.o"
echo "compiled  ports/recompile/stubs.c -> $out/stubs.o"

# The assembler spells the same ARM9 core arm5TE; -proc arm946e is a compiler spelling only.
"$as" -proc arm5TE "$root/ports/recompile/startup.s" -o "$out/startup.o"
echo "assembled ports/recompile/startup.s -> $out/startup.o"

"$ld" -o "$out/stub.elf" "$root/ports/recompile/stub.lcf" \
    "$out/startup.o" "$out/main.o" "$out/boot.o" "$out/stubs.o"

size=$(wc -c < "$out/stub.elf")
echo
echo "linked    $out/stub.elf"
echo "entry     0x$(python3 -c "import struct,sys;d=open('$out/stub.elf','rb').read();print('%08x'%struct.unpack_from('<I',d,0x18)[0])")"
echo "size      $size bytes (ELF container)"
echo "note      flat image, no VRAM/input/sound; services are empty stubs (see ports/recompile/README.md)"
