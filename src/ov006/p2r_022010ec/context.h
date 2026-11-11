/* Shared declarations for the ov006 Thumb accessor packet (batch 8).
 *
 * Overlay globals are declared as flat byte arrays and addressed with their
 * measured field offsets. Every symbol name carries its measured address, so the
 * comparison harness resolves relocations without any side table.
 *
 * Enablers this batch exists to exercise (both are tools now, not prose):
 *   - `ops/disasm.py --resolve-pools` follows `ldr rX,[pc,#n]` and prints the
 *     literal, because a 12-32 B Thumb accessor usually keeps its pool *outside*
 *     the row. The pool words below were read that way.
 *   - the two-variable return idiom: when the original ends with
 *     `adds r0, r3, #0` (a move from the loop counter into the return register),
 *     the source returned a *separate* variable, e.g.
 *         s32 count = 0;
 *         while (count < limit && text[count] != 0) count++;
 *         length = count;
 *         return length;
 *     Returning the counter directly drops that move and compiles 2 bytes short.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* This packet is built with -thumb and the Thumb BL encoder, so every source
 * here is a Thumb unit; the harness is driven with P2_MODULE=ov006 P2_THUMB=1. */

/* 0x0221c160: pointer to the shared value word read by 0x022010ec. */
extern u16 *native_data_ov006_0221c160;
/* 0x0221c150: block whose second word (at +4) points at the stream record. */
extern u8 native_data_ov006_0221c150[];

extern u32 native_fn_02204974(s32 first, s32 second);
