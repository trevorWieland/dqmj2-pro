/* ov000 row 0x02213a4c: 284 bytes.
 *
 * What it does: 70 instructions and 0 call(s), then a 18-entry dispatch through an inline branch table at 0x02213a5c (dispatch word at 0x02213a54)
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




asm u32 native_ov000_02213a4c (register u32 a0)
{
    cmp r0, #17
    mov r3, #1
    addls pc, pc, r0, lsl #2
    b L_02213b58
    dcd 0xea000010
    dcd 0xea000014
    dcd 0xea000018
    dcd 0xea00001c
    dcd 0xea000020
    dcd 0xea000024
    dcd 0xea000028
    dcd 0xea00002c
    dcd 0xea000008
    dcd 0xea000007
    dcd 0xea000006
    dcd 0xea000005
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000002
    dcd 0xea000001
    dcd 0xea000000
    dcd 0xea000027
    ldr r12, [pc, #0xb8]
    mov r0, #245760
    str r12, [r2]
    str r0, [r1]
    b L_02213b5c
    mov r0, #4096
    str r0, [r2]
    mov r0, #737280
    str r0, [r1]
    b L_02213b5c
    ldr r12, [pc, #0x90]
    mov r0, #184320
    str r12, [r2]
    str r0, [r1]
    b L_02213b5c
    mov r0, #4096
    str r0, [r2]
    mov r0, #737280
    str r0, [r1]
    b L_02213b5c
    mov r0, #4096
    str r0, [r2]
    mov r0, #737280
    str r0, [r1]
    b L_02213b5c
    mov r0, #2048
    str r0, [r2]
    mov r0, #737280
    str r0, [r1]
    b L_02213b5c
    ldr r12, [pc, #0x40]
    mov r0, #737280
    str r12, [r2]
    str r0, [r1]
    b L_02213b5c
    ldr r12, [pc, #0x2c]
    mov r0, #368640
    str r12, [r2]
    str r0, [r1]
    b L_02213b5c
    mov r0, #4096
    str r0, [r2]
    mov r0, #737280
    str r0, [r1]
    b L_02213b5c
L_02213b58:
    mov r3, #0
L_02213b5c:
    mov r0, r3
    bx lr
    dcd 0x0000170a
}
