/* ov000 row 0x021fb9a8: 116 bytes.
 *
 * What it does: 29 instructions and 0 call(s), then a 9-entry dispatch through an inline branch table at 0x021fb9b8 (dispatch word at 0x021fb9b0)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;




asm u32 native_ov000_021fb9a8 (register u32 a0)
{
    sub r1, r1, #47
    cmp r1, #8
    addls pc, pc, r1, lsl #2
    b L_021fba14
    dcd 0xea000007
    dcd 0xea000008
    dcd 0xea000009
    dcd 0xea00000a
    dcd 0xea00000b
    dcd 0xea000010
    dcd 0xea00000f
    dcd 0xea00000a
    dcd 0xea00000b
    add r0, r0, #20
    bx lr
    add r0, r0, #24
    bx lr
    add r0, r0, #28
    bx lr
    add r0, r0, #32
    bx lr
    add r0, r0, #36
    bx lr
    add r0, r0, #40
    bx lr
    add r0, r0, #44
    bx lr
L_021fba14:
    add r0, r0, #20
    bx lr
}
