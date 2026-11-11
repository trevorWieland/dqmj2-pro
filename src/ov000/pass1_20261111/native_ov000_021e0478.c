/* Mode-gated value fetch.
 *
 * Only mode 2 queries the engine through native_fn_0220a4e4; every other mode
 * returns zero. The image seeds the result in r1 before the test, calls with the
 * untouched first argument still in r0, and moves the callee's value into r1.
 * Unknowns: what the callee reads and why only mode 2 needs it.
 */
typedef unsigned int u32;

extern u32 native_fn_0220a4e4(u32);

u32 native_ov000_021e0478(u32 unused, u32 mode)
{
    u32 result = 0;

    if (mode == 2)
        result = native_fn_0220a4e4(unused);
    return result;
}
