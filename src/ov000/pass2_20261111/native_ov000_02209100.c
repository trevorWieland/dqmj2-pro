/* Mode-to-mask table.
 *
 * Five modes map to one bit each. The chain is written as five plain ifs with
 * no trailing return, which is why the image's last test has no early `bxeq`:
 * an unmatched mode falls off the end and returns the untouched argument.
 * Unknowns: which caller's mode this is and what the high bit enables.
 */
typedef int s32;

s32 native_ov000_02209100(s32 mode)
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
        return 0x80;
}
