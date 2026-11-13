/* ov006 row 0x021E3CD4: 4 bytes.
 *
 * ov006_noop_021e3cd4: Empty function: four-byte return-only body.
 *
 * Evidence: Compiled body is exactly 4 bytes (bx lr); source body is empty; 93 callers use it as a callback/no-op default.
 * Touches: nothing.
 * Remaining unknowns: Why callers require a no-op callback here is not established.
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
void ov006_noop_021e3cd4(void) {
}
