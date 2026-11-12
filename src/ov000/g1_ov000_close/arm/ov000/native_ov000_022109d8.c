/* ov000 row 0x022109d8: 140 bytes.
 *
 * What it does: 33 instructions and 0 call(s), then a 9-entry dispatch through an inline branch table at 0x022109ec (dispatch word at 0x022109e4)
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




asm u32 native_ov000_022109d8 (register u32 a0)
{
    mov r2, #0
    mov r1, r2
    cmp r0, #8
    addls pc, pc, r0, lsl #2
    b L_02210a54
    dcd 0xea000007
    dcd 0xea000008
    dcd 0xea000009
    dcd 0xea00000a
    dcd 0xea00000b
    dcd 0xea00000c
    dcd 0xea00000d
    dcd 0xea00000e
    dcd 0xea00000f
    ldr r2, [pc, #0x44]
    b L_02210a54
    ldr r2, [pc, #0x40]
    b L_02210a54
    mov r2, #18432
    b L_02210a54
    mov r2, #24576
    b L_02210a54
    mov r2, #40960
    b L_02210a54
    mov r2, #57344
    b L_02210a54
    mov r2, #131072
    b L_02210a54
    mov r2, #131072
    b L_02210a54
    mov r2, #524288
L_02210a54:
    mov r0, r2
    bx lr
    dcd 0x00000b85
    dcd 0x0000147a
}
