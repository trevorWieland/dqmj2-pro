/* Mode to mask value.
 *
 * Modes 0..3 map to the single-bit masks 1, 2, 4 and 8, mode 4 maps to 128, and
 * every other mode is returned unchanged (the last test only overwrites the
 * result on equality, so the input survives as r0).
 * Unknowns: which hardware word the masks are applied to.
 */
typedef unsigned int u32;

u32 native_ov000_02209100(u32 mode)
{
    if (mode == 0)
        return 1;
    if (mode == 1)
        return 2;
    if (mode == 2)
        return 4;
    if (mode == 3)
        return 8;
    if (mode == 4)
        return 128;
    return mode;
}
