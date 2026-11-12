typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Bit probe in a 0x64-byte-per-index bitmap block (pass-2 near-win).
 * The image loads the word into r0 and keeps the mask in r2. That rotation needs the
 * mask copied into a named value *before* the word load and the shifted mask kept
 * in its own named temp: writing the obvious `value = word[..]` first allocates the
 * word to r2 and the mask to r1 (7 differing bytes). The permuter found this
 * form; the redundant-looking named temp is the allocation knob, not semantics.
 * Unknowns: which record family uses the block and what the bits mean. */

extern u8 native_data_ov000_0224575c[];

s32 native_ov000_02215cb4(s32 index, s32 bit)
{
    u32 *word = (u32 *)(native_data_ov000_0224575c + index * 0x64);
    u32 value;
    s32 result = 0;
    u32 mask = 1;
    u32 shifted;

    value = mask;
    shifted = value << (bit & 0x1f);
    if (word[bit >> 5] & shifted)
        result = value;
    return result;
}
