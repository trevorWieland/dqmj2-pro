/* 0x02203ebc (ov006, Thumb, 48 B) -- "mask fully set" predicate, recovered by
   decomp-permuter and accepted by ops/verify_permuter.py.

   The only source difference from the previous draft is the operand order of the
   final comparison: `mask == field` rather than `field == mask`. mwcc then emits
   `cmp r0, r1` where the image has it, instead of `cmp r1, r0`.

   Build caveat, measured with the full compiler sweep, not assumed: mwccarm 2.0/base
   folds `mask == (field & mask)` into the BIC idiom (`bics r1, r0`) and CANNOT
   reproduce this row from any of the formulations tried. Every 2.0/sp1-or-later build
   and every dsi build reproduces it exactly; 1.2/* and 2004/b56 emit a 52-byte body.
   So this source is byte-exact under tools/mwccarm/mwccarm/2.0/sp1/mwccarm.exe, and
   promoting the row requires the project to adopt that build for it (the ledger row's
   compilerSha256 is still the global 2.0/base pin, which is why this file is not a
   ledger acceptance on its own). */
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
