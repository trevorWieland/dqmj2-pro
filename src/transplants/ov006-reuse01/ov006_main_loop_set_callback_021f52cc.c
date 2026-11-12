/* ov006 row 0x021F52CC: 12 bytes.
 *
 * ov006_main_loop_set_callback_021f52cc: Installs the per-frame callback in the ov006 main-loop context.
 *
 * Evidence: src/overlays/ov006_20261031_loop212/loop.c calls *(u32 **)(native_data_ov006_0221c06c + 12) once per frame and sets it to 021f5870 through this function before the loop.
 * Touches: ov006 global context 0x0221c06c, word +0xC.
 * Remaining unknowns: The callback's contract beyond 'called once per frame' is not established.
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
extern u8 native_data_ov006_0221c06c[];
void ov006_main_loop_set_callback_021f52cc(u32 callback) {
    *(volatile u32 *)(native_data_ov006_0221c06c + 12) = callback;
}
