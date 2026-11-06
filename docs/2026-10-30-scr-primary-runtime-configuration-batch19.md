# Complete primary-controlled runtime configuration pair — 2026-10-30

Two complete world SCR routines rebuild from ordinary structured C: entry 261,
`[11912,12536)`, and entry 273, `[18412,19036)`, each 624 bytes. Their C definitions
are under `src/scripts/20261030/batch19/object6/` and `object7/`. They form one
implementation family, with two authored definitions and two qualified instances.
The source compares a primary flag, then calls the same named configuration API
with mode 0 when clear or mode 2 when set. Categories are the source/header enum
constants 6 and 7. No gameplay accessibility, entity, area, quest, or renewability
meaning is established by these raw categories or mode values.

The symbolic C interface explicitly declares module float objects and the VM
argument-bank float objects. Four incoming words are copied to shared slots
23–26. The fifth is copied to slot 31 or 54, then overwritten by the getter result
before the condition. Slots 23–26 and 31 have measured outside reads and writes;
they must not be represented as private C locals. Slot 54 has no other currently
encoded references, but remains conservatively explicit module storage here.
All outside references are recorded by PC, slot, access direction, and own-range
membership. This does not exhaust opaque native or computed references.

The live argument-bank inputs are 0–4. API argument preparation and the original
dispatcher clobber argument words 0–6, including return word 0; these declared
external objects intentionally expose that ABI effect. The C entry has no ordinary
formals and reads those external inputs. A native port must supply them through
the VM/module context bridge. It must not invent independent private copies that
discard the observed module-global writes or API argument-bank effects.

Named primary access uses SYS41 and its original native getter. Named runtime
configuration uses SYS69, original main:ARM02051EA8. That dispatcher converts
category/mode to bytes, selector to signed 16 bits, and all four scalar parameters
through original binary32 scaling/adjustment and signed integer conversion. It
then calls original overlay000:ARM02212C94 with eight words. The measured scale is
4096. Half-tick controls cover both signs, alongside signed zero, fractional values,
and endpoints ±4096. The supported primary index is finite, integral, and 0–1535;
supported coordinate values are finite binary32 with absolute value at most 4096.
This is a qualified fixture domain, not an exhaustive conversion theorem.

The constructor itself remains original and executes: it scans 16 records at
`02243E3C`, stride `10C`, using nonzero active byte `+105`. The accepted corpus
deliberately sets all 16 active bytes to nonzero values, including 1, 255, 128, and
2. This forces its capacity-exhausted return without entering resource handling.
It returns native -1, converted to float -1 in VM argument register 0. All record
bytes remain unchanged. Neither the constructor nor any lower routine is replaced
with a provider or credited as newly reconstructed source.

Free-pool probes reach original resource handling and fault at `021DF9A4`. Those
are unsupported execution contexts. Their partial execution, subsequent memory,
and absent complete SCR returns receive zero proof/source/error-path credit.
They remain in `work/script-source/20261030/batch19-configuration-probe.json` as
diagnostic evidence. This batch proves capacity-return contexts only; it does not
prove successful object creation, valid resource context, or natural scene/caller
reachability. Native category/constructor existence is not an access or renewal
proof.

Each range has one public root and one private return. The current encoded audit
finds no public interior root, external direct interior transfer, or shared return.
Both eight-byte padding ranges following the private returns are excluded from
source credit. The source includes one ordinary extra compound block in the else
arm; the compiler emits the original block entry and join layout. Authored C has
no opcodes, PC constants, byte arrays, or generated disassembly.

The separately named v16 backend parses explicit module/argument objects, scalar
assignments, typed primary reads, scalar conditions, and the seven-float named
configuration call. It receives five copied inputs per build: core parser,
backend, C, header, and symbolic object mapping. Original bytecode is not a
compiler input. Each source-only product matches all 624 bytes; replacing both
ranges produces the original decoded image. No general C compiler claim is made.

Before adoption, an experimental metadata defect was found: the getter-result
write descriptor pointed to the statement's first argument transfer, 32 bytes
before the actual module write. Its C and emitted executable bytes were correct.
The initial compiler, matcher, accessor, report, and source-only products were
preserved under `work/script-source/20261030/batch19/pre-adoption-metadata/`.
Only the new unaccepted v16 metadata was corrected, and the complete original/
recompiled proof was rerun. The final accessor independently resolves every
compiler object read/write PC to the actual current decoded instruction and slot.
Earlier frozen backends, source, and proofs were not changed.

The final proof uses eight scalar/flag profiles, all four VM threads, two entries,
and two serialized calls in each fresh context. Original and reconstructed runs
produce 256 complete own-entry executions and 6,208 actual native returns, with
both outcomes at each decision and every own record executed. Counts include no
callee source or whole-image credit. Every native call retains the original
20,000-instruction and 1,000,000-microsecond bounds; count-only research was not
adopted. The complete SCR step cap is 40.

Comparison covers all general registers/CPSR, ordered CPU-store hashes, full VM
context, persistent state, all 256 VM slots, the exact six ordered module stores,
all eight constructor words, the complete argument bank, and the entire exhausted
pool. An independent binary32 conversion model checks constructor arguments.
Ten malformed source/type/ABI/storage controls fail before output. The grouped
accessor performs one full current source/input/product/native-proof validation
and returns records keyed by code hash and start. The registry adapter suite
passes 22 meaningful rejections and both positive units from root and parent
working directories. Missing products withhold current credit.

Reproduce the full original/reconstructed native proof:

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_runtime_configuration_20261030_batch19.py'
```

Replay source-only acceptance and mutation controls:

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\verify_interpreted_runtime_configuration_sources.py'
```

Frozen final identities:

- Backend `84ff9e84b8085d8776c623ec92c9b3e7ace9e9daa90420297f54b8090fb6f5b7`;
  matcher `0311afc386e8fd86a2a3685fd82b3a2b136f4dbb9f86961e703d5d5167cd90e8`;
  native fixture `3a2300dcf4351d22b6b45ebaa23cbbe175ae70f5fe61b63ae249e307465810ee`.
- Report `evidence/matches/scripts-20261030-runtime-configuration.json`:
  `2f7f79434d325b9d12aa1c106af2faba8d47382728af9e11c0fdaa1f97ee706b`.
- Grouped accessor `87d2bdf6c79dbc0fad5754d6c63426ab834545fe04203899e2ff4082959b70ab`;
  adapter `ce6bf50ddbd277b880f4588a9ee142ef6fcc695064678b17ae474931dc43a4d1`;
  mutation suite `6e237dc6108324d35bce4d8445295bd4028b5db0f6cb4c57d8a7358f71089196`.
- Verification `evidence/verification/interpreted-runtime-configuration-source-negatives-20261030.json`:
  `300787f72e4677228a28d6cf1d2f07c896faef4312e27a74543710d1caba6b52`.
- Entry 261 body `0510e557b0ed88ae31d07fde3502aeaf2b6ca0265494c7017b24674775d2d6fb`;
  entry 273 body `fba288ab296b856ef1680413ef7d788335d64673ec1338839db5d5dbb4edae09`.

The authoritative ROM remains SHA256
`674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`.
All source/include/profile hashes are in the frozen source-closure report. The
integrator owns shared registration; this work does not edit the application,
baseline, original inputs, old source/proofs, or shared ledgers. This is 1,248 bytes
of qualified interpreted source, with zero new native, padding, scaffolding,
complete-image, successful-construction, or whole-ROM source credit.
