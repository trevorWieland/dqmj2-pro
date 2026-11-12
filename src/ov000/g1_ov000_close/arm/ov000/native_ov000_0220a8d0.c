/* ov000 row 0x0220a8d0: 144 bytes.
 *
 * What it does: 36 instructions and 0 call(s), then a 11-entry dispatch through an inline branch table at 0x0220a8dc (dispatch word at 0x0220a8d4)
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




asm u32 native_ov000_0220a8d0 (register u32 a0)
{
    cmp r0, #10
    addls pc, pc, r0, lsl #2
    b L_0220a958
    dcd 0xea000009
    dcd 0xea00000a
    dcd 0xea00000b
    dcd 0xea00000c
    dcd 0xea00000d
    dcd 0xea00000e
    dcd 0xea00000f
    dcd 0xea000016
    dcd 0xea00000f
    dcd 0xea000010
    dcd 0xea000011
    mov r0, #245760
    bx lr
    mov r0, #245760
    bx lr
    mov r0, #737280
    bx lr
    mov r0, #1474560
    bx lr
    mov r0, #1474560
    bx lr
    mov r0, #1474560
    bx lr
    mov r0, #245760
    bx lr
    mov r0, #245760
    bx lr
    mov r0, #1474560
    bx lr
    mov r0, #245760
    bx lr
L_0220a958:
    mov r0, #0
    bx lr
}
