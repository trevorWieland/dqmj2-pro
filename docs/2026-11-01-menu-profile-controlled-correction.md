# 2026-11-01: Controlled compiler-profile correction for the 396-byte consumer

The earlier explanation that changing the input helper return declaration from u32 to signed char caused the 396-byte consumer to shrink to 392 bytes is retracted. That experiment did not rebuild the unchanged baseline with the same compiler profile. The initial default space profile already produces 392 bytes for the unchanged source.

The new controlled experiment reproduces the pinned compiler at `tools/mwccarm/mwccarm/2.0/base/mwccarm.exe`, SHA-256 `7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880`. It genuinely compiles and links each of these separate source variants under both profiles:

| Source variant | Default space | Accepted speed |
| --- | ---: | ---: |
| Unchanged 0206EAA0 baseline | 392 bytes, nonmatching | 396 bytes, complete match |
| Input helper 0206238C declared s8 return | 392 bytes, nonmatching | 396 bytes, complete match |
| Byte setter 02062358 declared u32 return | 392 bytes, nonmatching | 396 bytes, complete match |

The common flags are `-O2 -enum int -char signed -str noreuse -proc arm946e -gccext,on -fp soft -inline off -Cpp_exceptions off -RTTI off -interworking -w off -sym on -gccinc -nolink -msgstyle gcc`. The accepted profile additionally uses `-opt speed`. Each replay checks source identity, compiler identity, current real-link output and the measured 396-byte native span. Both normal and parent-directory `-I -S` runs reproduce all six outcomes.

Run `python check_save_core_menu_profiles308_20261101.py`. The full six-row evidence is `evidence/attempts/menu-profile308-controlled-baseline-20261101.json`. The earlier 291/297 sources, reports and writeup remain unchanged as history. This addendum supersedes only the earlier causal interpretation of their shrinkage observation.

The 252-byte input routine's compiler/link equality, 38,092 returning native/source entry executions with its typed 92-byte consumer, independent models and negative controls are unaffected. Its preferred u32 API preserves the existing consumer view and measured full return words FFFFFFFF/0/1; these tests recover no original signed-char versus full-word declaration. Neither declaration variant is forced by the consumer's byte score.

The new 396-byte latch-return declaration alternative is not preferred or registered. Its only source change is `extern void native_fn_02062358(u32 value)` to `extern u32 native_fn_02062358(u32 value)`. Any migration still requires the native setter's qualified input/return contract and an overlay-owned alternative for the separately discovered birth395 header declaration. This experiment establishes no broader interface correctness for unchanged historical helper declarations.
