/* 0x02203ebc (ov006, Thumb, 48 B) -- "mask fully set" predicate, recovered by
   decomp-permuter and accepted by ops/verify_permuter.py under the row's own rule.

   The only source difference from the previous draft is the operand order of the final
   comparison: `mask == field` rather than `field == mask`, so mwcc emits `cmp r0, r1`
   where the image has it instead of `cmp r1, r0`.

   Compiler selection is proven by sweep, not guessed: exact under mwccarm
   2.0/sp1 .. 2.0/sp2p4 and every dsi build; 2.0/base folds `mask == (field & mask)` into
   the BIC idiom and cannot reach the image from any tried source form; 1.2/* and
   2004/b56 emit a 52-byte body. The row is therefore pinned to 2.0/sp1 -- the lowest
   exact build -- by a row-level rule in config/source_units.json and by the ledger row's
   compilerSha256/compilerFlags (p004); the global compiler stays 2.0/base. Verified
   through public_tools/repo_build.py, not the permuter score.
   Evidence: docs/authoring/permuter-02203ebc-receipt.json and the row's ledger entry;
   the rule itself is in docs/authoring/permuter.md, "The rule this establishes". */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

extern u16 native_data_027fffa8;
extern u8 native_data_ov006_0221c18c[];

/* Report whether the caller's mask is fully set, unless the status gate is up. */
s32 native_ov006_02203ebc(u32 mask)
{
    u32 field;

    if ((native_data_027fffa8 & 0x8000) >> 15)
        return 0;
    field = *(u16 *)(*(u8 **)(native_data_ov006_0221c18c + 4) + 0x32);
    field &= mask;
    return mask == field;
}
