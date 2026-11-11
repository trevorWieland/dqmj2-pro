<#
.SYNOPSIS
    Build the standalone recompilation stub: matched boot source + platform stubs + minimal startup,
    linked by the pinned Metrowerks toolchain into a flat ARM9 ELF.

.DESCRIPTION
    This is the public link path for the RECOMPILATION lens. It compiles the two matched boot
    functions from src/, a stubbed platform layer and a minimal startup, then links them with
    stub.lcf using the pinned mwldarm.

    The result is NOT the game. It is a linked image whose entry point runs the reconstructed
    main() against empty services; it exists so the toolchain path is exercised publicly and so a
    porter has a linkable starting point.

.PARAMETER Toolchain
    Directory holding mwccarm.exe, mwasmarm.exe and mwldarm.exe. Defaults to the pinned location
    under tools/ (a private junction in a full checkout).

.PARAMETER OutDir
    Output directory. Defaults to build/recompile.

.EXAMPLE
    ./ports/recompile/build.ps1
#>
param(
    [string]$Toolchain = "tools/mwccarm/mwccarm/2.0/base",
    [string]$OutDir = "build/recompile"
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$tool = (Resolve-Path $Toolchain).Path
$out = Join-Path $root $OutDir
New-Item -ItemType Directory -Force -Path $out | Out-Null

$cc = Join-Path $tool "mwccarm.exe"
$as = Join-Path $tool "mwasmarm.exe"
$ld = Join-Path $tool "mwldarm.exe"
foreach ($exe in @($cc, $as, $ld)) {
    if (-not (Test-Path $exe)) { throw "missing pinned tool: $exe" }
}

# Metrowerks looks for its libraries through these variables. MWLibraries is a directory and is
# accepted as-is. MWLibraryFiles is a LIST of archive file names, not a directory: pointing it at a
# directory splits on the drive colon ("Specified file 'C' not found"), so this flat image leaves it
# unset and links no Metrowerks runtime at all.
$env:MWLibraries = $tool
if ($env:MWLibraryFiles) { Remove-Item Env:MWLibraryFiles }
$license = Join-Path $root "tools/mwccarm/mwccarm/license.dat"
if (Test-Path $license) { $env:LM_LICENSE_FILE = $license }

$cflags = @("-O2", "-enum", "int", "-char", "signed", "-str", "noreuse", "-proc", "arm946e",
            "-gccext,on", "-fp", "soft", "-inline", "off", "-Cpp_exceptions", "off", "-RTTI", "off",
            "-interworking", "-w", "off", "-sym", "on", "-gccinc", "-nolink", "-msgstyle", "gcc")

$sources = @(
    @{ Name = "main";    Path = "src/main/p3g_main_02000c34/native_main_02000c34.c" },
    @{ Name = "boot";    Path = "src/main/p3g_main_02000c34/native_main_020c225c.c" },
    @{ Name = "stubs";   Path = "ports/recompile/stubs.c" }
)

foreach ($source in $sources) {
    $full = Join-Path $root $source.Path
    $obj = Join-Path $out ("{0}.o" -f $source.Name)
    & $cc @cflags "-c" $full "-o" $obj
    if ($LASTEXITCODE -ne 0) { throw ("compile failed: {0}" -f $source.Path) }
    Write-Host ("compiled  {0} -> {1}" -f $source.Path, $obj)
}

$startupObj = Join-Path $out "startup.o"
# The assembler spells the same ARM9 core arm5TE; -proc arm946e is a compiler spelling only.
& $as "-proc" "arm5TE" (Join-Path $root "ports/recompile/startup.s") "-o" $startupObj
if ($LASTEXITCODE -ne 0) { throw "assemble failed: ports/recompile/startup.s" }
Write-Host ("assembled ports/recompile/startup.s -> {0}" -f $startupObj)

$elf = Join-Path $out "stub.elf"
$lcf = Join-Path $root "ports/recompile/stub.lcf"
& $ld "-o" $elf $lcf (Join-Path $out "startup.o") (Join-Path $out "main.o") (Join-Path $out "boot.o") (Join-Path $out "stubs.o")
if ($LASTEXITCODE -ne 0) { throw "link failed" }

# Entry point from the ELF header (little-endian e_entry at offset 0x18) and the image size.
$bytes = [System.IO.File]::ReadAllBytes($elf)
$entry = [BitConverter]::ToUInt32($bytes, 0x18)
$size = $bytes.Length
Write-Host ""
Write-Host ("linked    {0}" -f $elf)
Write-Host ("entry     0x{0:x8}" -f $entry)
Write-Host ("size      {0} bytes (ELF container)" -f $size)
Write-Host "note      flat image, no VRAM/input/sound; services are empty stubs (see ports/recompile/README.md)"
