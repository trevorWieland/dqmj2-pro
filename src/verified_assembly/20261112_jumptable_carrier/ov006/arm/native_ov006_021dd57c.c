/* ov006 row 0x021dd57c: 80 bytes.
 *
 * What it does: switch dispatch through an inline table
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles and the meaning of the table entries are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;




asm u32 native_ov006_021dd57c (register u32 a0)
{
    cmp r1, #4
    addls pc, pc, r1, lsl #2
    b L_021dd5c4
    dcd 0xea000003
    dcd 0xea000004
    dcd 0xea000005
    dcd 0xea000006
    dcd 0xea000007
    ldrb r0, [r0, #0x7]
    bx lr
    ldrb r0, [r0, #0x8]
    bx lr
    ldrb r0, [r0, #0x9]
    bx lr
    ldrb r0, [r0, #0xa]
    bx lr
    ldrb r0, [r0, #0xb]
    bx lr
L_021dd5c4:
    mov r0, #0
    bx lr
}
