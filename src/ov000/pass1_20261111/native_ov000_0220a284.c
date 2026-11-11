/* Mode-to-pointer selector.
 *
 * Modes 1 and 2 share the constant pointer 0x0220a120 (a code address inside
 * ov000); every other mode yields null. The image compares the mode twice with
 * `cmp`/`cmpne` and branches, which is a two-case switch, not an OR of
 * equalities (an OR range-collapses to `sub`/`cmp`).
 * Unknowns: what the pointer at 0x0220a120 is (function or table).
 */
typedef unsigned int u32;

u32 native_ov000_0220a284(u32 mode)
{
    switch (mode) {
    case 1:
    case 2:
        return 0x0220a120;
    }
    return 0;
}
