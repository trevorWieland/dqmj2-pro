/* Gate byte probe and engine query.
 *
 * Returns zero when the signed byte at 0x0224536c + 16 is non-zero, otherwise the
 * value from native_fn_021fa498. The image materialises the zero result before
 * the test and returns it through `popne`, so the call is guarded by a result
 * variable rather than an early return (an early `return callee()` would become a
 * tail branch instead of `bl` + `pop`).
 * Unknowns: what the gate byte disables and what the query reads.
 */
typedef signed char s8;
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_0224536c[];
extern u32 native_fn_021fa498(void);

u32 native_ov000_02216ea4(void)
{
    u32 result = 0;

    if (*(s8 *)(native_data_ov000_0224536c + 16) == 0)
        result = native_fn_021fa498();
    return result;
}
