# Complete registered-key primary-flag routine — 2026-10-30

One complete world SCR entry is reconstructed as ordinary named, structured C:
`src/scripts/20261030/batch17/apply_registered_primary.c`. Its sole definition
`float apply_registered_primary(float candidate)` rebuilds entry259, code-relative
range `[7228,8356)`, exactly1128 bytes, including its private return at8352.
There is no native executable-byte credit or complete-image credit.

The authoritative ROM remains175959612 bytes, SHA256
`674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`.
The archive `world.e` hashes to
`516ee5fa9061712ec2593d8d385ff61e1c3d54c31d3b291246366bfd891e3923`;
its member0 decoded script is
`9c6c4a136b306126a83a8a749df18276aa2a9d328a4add073fc47f50ea0619f8`,
code hash `a87d97153fbe293b7f78dd028b2a6abddce4dbc4b49ecb78779bbd9d8ea06dbc`.
The reconstructed range hashes to
`900c520d1c47be0167c33b8ac2bbaa5ea2839b65e130ea672f7721927222180b`.
Original bytes outside this complete range remain explicitly zero-credit scaffolding.

The C source compares its float input, in order, against ten explicitly declared
module-global float keys. A first match selects the corresponding module-global
float flag index. No match changes the candidate to-1. For a non-sentinel candidate,
it calls the named primary getter and sets that bit only when previously false.
When already true it changes its private index local to-1, while still returning
the original candidate. Duplicate keys therefore choose the first key, even if
that key's flag was already set. This does not establish any once-ever property:
other native/script logic can clear the same primary flags.

The returned value occupies VM argument register0 as raw binary32. A negative-zero
input matching a positive-zero key returns its original `80000000` bits. Matching
infinities are supported in measured profiles. Quiet and signaling NaN candidates
match no key and return-1. The proof does not claim exhaustive NaN payloads or all
possible module-global float tables. Float bit-copying is distinct from integer
numeric conversion when preparing a native Android implementation.

Slots3–12 hold the ten module-global keys and13–22 the corresponding flag-index
values. They are not private locals. The current encoded reference audit finds
one read and two writes for each of these slots. Original entry256 initializes
them to-1; the registration flow writes key and flag pairs. The initializer and
registration flow remain original dependencies, not recovered by this batch.
Their natural caller/scene reachability and complete producer-domain proof remain
unresolved. No direct encoded SCR call to259 was found. Synthetic native launch
contexts exercise the complete entry without claiming an enclosing scene path.

Formal candidate slot42 is written before every source read; slot43 is initialized
to-1. Boolean slot44 is assigned by the getter before its conditional read, and is
left unchanged on paths where the getter is skipped. The current encoded audit
finds no outside references to slots42–44, no public interior entry, external
direct interior branch, or shared return. Opaque native/computed references are
not exhaustively ruled out. The proof covers serialized calls, including all four
VM threads and repeated entry, rather than concurrent independent use of these
three slots.

Only a selected index that will actually be passed to a flag API must be finite,
integral, and within0..1535. The five explicit unsupported selected-index contexts
use-1,1536,31.5,NaN,+infinity. The fixture rejects them before executing this own
entry; this is a qualification guard, not a native error path. They receive zero
complete-return, post-stop state, or error-path credit. An unselected invalid
table element does not by itself violate the measured entry domain.

The original native VM interpreter/dispatcher and primary-flag accessors execute
without providers. SYS41 and42 bind the named getter/setter; primary storage is
`021C0E20`, with actual aligned-word read/modify/write stores. Existing native
getter/setter identities are main:ARM02063B40 and02063B60. All native dependencies
have zero new source credit here. No primary index is assigned an area, quest,
accessibility, spawn, reset, or renewability meaning by this proof.

The separately named restricted backend `scr_c_compiler_20261030_v14.py` extends
the frozen core parser with float formals/returns, explicit extern float globals,
scalar assignments, definite-assigned locals, structured conditions, and a dynamic
index for the existing typed primary APIs. Two explicit C compound blocks lower
to the corresponding generated block/join records. Authored source contains no
opcode transcript, source PC constants, byte arrays, or per-opcode macros. It is
a restricted C99 backend, not a general C compiler. Earlier backends remain frozen.

Source-only compilation uses five copied inputs: core parser, backendv14, C,
header, and symbolic binding profile. The compiler receives no original bytecode.
Every input, emitted1128-byte body, build report, and reconstructed image is hashed.
The current full source range and whole patched image equal their original bytes.
The validator repeats the compiler in a fresh temporary directory and independently
recomputes direct/private/global references, scalar branch semantics, all relevant
state transitions, and complete-entry accounting from the current decoded image.

There are31 profiles ×4 threads ×2 serialized calls ×2 implementations:
496 complete entry executions. Native start/fork/interpreter/helper calls total
14748 actual returns; that larger number is not a script-entry count. The profiles
cover each of ten keys with initially clear/set flags, unmatched input, both NaN
classes, negative zero, both infinities, duplicate keys, shared flag indices,
unregistered sentinels, and a matched sentinel key. All twelve conditional branch
sites take both outcomes, and all own records execute within the supported domain.
Every call uses a fresh bounded native machine context with a20000-instruction
cap,1000000-microsecond timeout, and actual return checks; the script cap is100 steps.

The comparison includes all general registers/CPSR and native ordered CPU stores,
all persistent bytes, full VM state, raw scalar result, ordered primary word stores,
and all256 VM slots. Randomized slots outside42–44, including all20 module globals,
must be preserved. Ten malformed source/profile cases fail before output. The
standalone adapter mutation suite rejects23 separate identity, closure, availability,
domain, raw-return, global/private, native-state, accounting, and excess-credit
claims, then accepts the positive unit. Both root and parent-directory invocations
passed, with identical verification output.

Reproduce the complete native differential proof with pinned Python3.13.5:

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_registered_flags_20261030_batch17.py'
```

Replay current source-only/acceptance/mutation gates:

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\verify_interpreted_registered_flags_sources.py'
```

Frozen identities:

- Source `084887ba1ffe0e821f3e3dccace1262fc5881a32113cbeff9b2be924af9f3f30`;
  header `a84a47733ba2148fd1719589f1265ee535a6fca62ec836eb616497320c1615f6`;
  binding profile `9061b4599bf0afb7c650a09b2c158aa87f18f2d58d432d5722991385149b0961`.
- Backend `b0ee0e0fbc2b89d9e86be1a4928eab76c3da8838276c0a1b98f58e28ab310472`;
  matcher `4e598094ada3d74c3a3ada59494b001a1a2d116b0d43f8eae93b046da412d023`.
- Differential report `evidence/matches/scripts-20261030-registered-flags.json`:
  `8bfede07c7fad8ef86f277d9369b3834ecc6107d0eddf361c381a782cc5fd40f`.
- Validator `2dff9d1fe00b72514a295fb7e9a38b16d28d258ed28f2f2e61dd65d96dae7c21`;
  adapter `b5ff0a561a6d9a473777bda0982bd8a6a728b76c4cbb2529f8cc3eea92da75c8`;
  suite `b6369cf5a06b20e953f2b425d93bda491ce968af072503faa44cd1dafe662f8d`.
- Mutation report `evidence/verification/interpreted-registered-flags-source-negatives-20261030.json`:
  `646e0a3b03a6980aed05e5a2961cfd6c8fddcdfd2ecd748fb3f7b568393e4554`.

These are source/proof candidates for integrator acceptance. No shared registry,
ledger, application, baseline, original ROM/save, old source or frozen proof was
edited. Full-image interpreted logic, whole-ROM source reconstruction, opaque
global program closure, natural initialization, and gameplay meaning remain open.
