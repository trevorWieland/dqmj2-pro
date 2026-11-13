/* ov006 row 0x021E3CD8: 12 bytes.
 *
 * ov006_forward_four_args_021e3cd8: Four-argument forwarder to main function 0x020273C8.
 *
 * Evidence: Body is a single tail call to native_fn_ov006_020273c8(a, b, c, d); no other work.
 * Touches: main function 0x020273C8.
 * Remaining unknowns: The callee's semantics are unknown, so the forwarder can only be named by mechanism.
 *
 * The address stays in the symbol and file name because the measurement pairs a
 * compiled symbol to the private ledger row by its eight-hex address; removing
 * it would silently unmatch the row under the pinned private ledger.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_ov006_020273c8(u32, u32, u32, u32);
u32 ov006_forward_four_args_021e3cd8(u32 a, u32 b, u32 c, u32 d) {
    return native_fn_ov006_020273c8(a, b, c, d);
}
