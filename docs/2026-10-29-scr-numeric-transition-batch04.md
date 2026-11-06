# Complete nested numeric-state transition, 2026-10-29

One substantive 352-byte SCR routine now rebuilds exactly from ordinary C: `s07e01.e` entry 102, executable range `0xFC64..0xFDC4`. It reads raw context value 0 and numeric byte-plane indices 0 and 9, then writes numeric 9 to 3 only when those three values equal 60, 7 and 2. These are measured indices and values; no world, event, quest, progression or encounter meaning is assigned.

The separate empty-family batch adds no substantive logic and is documented independently. V1/v2/v3 and finished batches remain frozen. This unit uses a separately named v4 compiler and new source/header/allocation inputs under `src/scripts/20261029/batch04/`.

```c
#include "scr_numeric.h"
void advance_numeric_nine_when_values_match(void)
{
    float context_value = get_context_value(0);
    float state_zero = get_numeric_state(0);
    float state_nine = get_numeric_state(9);
    if (context_value == 60) {
        if (state_zero == 7) {
            if (state_nine == 2) {
                set_numeric_state(9, 3);
            }
        }
    }
}
```

## Reproduction and scope

```text
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_numeric_transition_20261029_batch04.py
```

The final fresh replay passed from the parent DQM directory. Its source-only subprocess receives the v4 compiler, frozen v1 parser dependency, C source, explicit ABI header and named allocation JSON. It does not receive original bytecode. The matcher compares the generated 352 bytes with the ROM-backed decoded range and preserves every other byte as original scaffolding.

V4 adds float getter declarations, raw VM context reads, numeric byte getter/setter APIs, exact-integer scalar comparisons and nested structured `if`/`else`. Boolean support remains separately typed. General C/C++, runtime arithmetic/reassignment, arbitrary APIs and full preprocessing remain unsupported. All generated branch targets come from source structure; source code contains no program-counter constants, opcode macros or executable arrays.

The named allocation profile maps `context_value` to slot 133, `state_zero` to 126 and `state_nine` to 127. This is an explicit compiler allocation input, not source-level instruction text. Slot 133 has one known direct write/read pair inside this routine. Slots 126 and 127 each have one internal write/read pair and two known outside writes, with no known outside reads in understood operand forms. Those shared physical scratch locations are reconciled: this routine unconditionally initializes all three slots before any branch or read. Poisoned initial storage is independently overwritten. Arbitrary opaque native slot accesses and interleaved/reentrant invocation semantics remain uncertified.

## ABI and native behavior

`get_context_value(0)` reads the raw binary32 word at VM context `+0x450`. Its natural producer and the game's ability to supply value 60 are **not established**; fixtures provide this input explicitly. Numeric indices 0 and 9 are raw byte-plane locations. Getters return exact 0..255 values as binary32, and this setter accepts a compiler-supported byte-domain value. Integer literals 60, 7, 2 and 3 are exactly representable in the target binary32 ABI. Native SYS39/SYS40 wrappers and the context operand reader remain original callees with zero new source credit.

The fresh original-versus-rebuilt suite passes **3,906 actual returning native calls per implementation, 7,812 total**, with 129 separately initialized machines per implementation. There are 128 scenarios covering all four nested outcomes, all four selected VM threads, independent seeds, byte extremes and context values immediately around 60, signed zeros, infinities and NaN payloads. Each scenario runs the complete routine twice.

The first invocation follows 11, 14, 17 or 21 script records according to the nested branch outcome. Exactly the matching case writes one numeric byte, changing 9 from 2 to 3. Reentry then reads 3, skips the setter and performs no repeated write. Nonmatching cases preserve all persistent bytes. Slots retain the exact captured context/numeric input values, including the old value 2 after a successful first write; the second invocation refreshes that scratch value to 3.

Every counted native call reaches the return sentinel within 20,000 instructions and one second and preserves SP/R4-R11. All general registers/CPSR, ordered CPU stores, persistent state and VM contexts agree. Native initialization, entry/fork, getter, setter, comparison and termination execute unchanged without stubs. A negative native entry is rejected without executing the reconstructed routine. Full direct boundaries have no decoded external interior entry or shared return tail; the private return is at `0xFDC0`. Adjacent unexecuted original bytes remain hashed zero-credit scaffolding.

Eighteen negative source/profile controls reject invalid context/numeric indices, non-byte setter values, type/identifier/condition errors and missing, duplicate, invalid or unused named allocations. A wrong but valid allocation changes output bytes and fails the original comparison. A failed CLI build preserves existing output/report sentinels. Separate generated numeric `if`/`else` fixtures validate both runtime outcomes for values 0, 2, 3 and 255 and receive zero original-source credit.

## Frozen identities

| Artifact | SHA-256 |
| --- | --- |
| V4 compiler | `171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7` |
| Matcher | `95d85c5e1223872be29b98263d75965e5310b987b0338541b37af790a4292b4f` |
| C source | `5d92cace3f73a28d0f93be17709c410c41154789525d67698f28902bb3bcbddb` |
| ABI header | `dd9083a3b944895fa04c96a6dc41900e7d9d1923842f1f420ea253ff854a3bcf` |
| Named allocation input | `41373da4b45c7ac0fdbd056165460b705fccc4fe8fcbefceda466c1924fc657a` |
| Native fixture | `d6e22c9055991030d0cd2f9a1667ed3d31236ffa07522cac0bf0a7ebf8b23fcd` |
| Emitted/original routine | `05fb2c6b3e087b6c6e32ead277dc644ad3b3127764853eba394237a7d60161cd` |
| Report `evidence/matches/scripts-20261029-numeric-transition.json` | `814c640a5d45f2aa88e86726f4f5fa94b2f4fbba1403dca27d2ac81c8bca91a0` |

The decoded image hash is `f9aa89801c68b6f8c765a4162caa1540bace68c5928738621fd7890e41a050db`; archive hash is `0eea1755d720f4544d974fa8bcaa66ba0d094ca92c72a1c1da5fc7218aef83ae`. Archive bytes are verified against the pinned ROM allocation interval, and all member aliases are checked without multiplying source credit. The decoded image remains 143,140 bytes; 142,788 bytes retain zero source credit. No whole image, native executable bytes, archive compression, scene, travel path, access condition, battle eligibility or encounter renewability is established.
