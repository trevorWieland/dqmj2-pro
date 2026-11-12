/* ov000 row 0x02213fa4: 100 bytes.
 *
 * What it does: 25 instructions and 0 call(s), then a 18-entry dispatch through an inline branch table at 0x02213fb0 (dispatch word at 0x02213fa8)
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




asm u32 native_ov000_02213fa4 (register u32 a0)
{
    cmp r0, #17
    addls pc, pc, r0, lsl #2
    b L_02214000
    dcd 0xea000010
    dcd 0xea00000f
    dcd 0xea00000e
    dcd 0xea00000d
    dcd 0xea00000c
    dcd 0xea00000d
    dcd 0xea00000c
    dcd 0xea00000b
    dcd 0xea000008
    dcd 0xea000007
    dcd 0xea000006
    dcd 0xea000005
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000002
    dcd 0xea000001
    dcd 0xea000000
    dcd 0xeaffffff
    mov r0, #1
    bx lr
L_02214000:
    mov r0, #0
    bx lr
}
