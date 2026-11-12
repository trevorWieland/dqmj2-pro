/* ov000 row 0x02226af8: 276 bytes.
 *
 * What it does: 67 instructions and 1 call(s), then a 16-entry dispatch through an inline branch table at 0x02226b24 (dispatch word at 0x02226b1c)
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

extern void native_fn_02226778(void);


asm u32 native_ov000_02226af8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r4, [pc, #0x100]
    bl native_fn_02226778
    ldr r0, [pc, #0xfc]
    ldrsb r1, [r0, #24]
    cmp r1, #22
    bgt L_02226b64
    bge L_02226bb8
    cmp r1, #15
    addls pc, pc, r1, lsl #2
    b L_02226bf8
    dcd 0xea000015
    dcd 0xea000014
    dcd 0xea000013
    dcd 0xea000012
    dcd 0xea00002f
    dcd 0xea00002e
    dcd 0xea00002d
    dcd 0xea00002c
    dcd 0xea00002b
    dcd 0xea00000c
    dcd 0xea000029
    dcd 0xea000011
    dcd 0xea000010
    dcd 0xea000026
    dcd 0xea000025
    dcd 0xea00000d
L_02226b64:
    cmp r1, #23
    bgt L_02226b74
    beq L_02226bb8
    b L_02226bf8
L_02226b74:
    cmp r1, #27
    beq L_02226be4
    b L_02226bf8
    ldrb r1, [r4, #0x18c]
    cmp r1, #127
    beq L_02226bf8
    cmp r1, #2
    moveq r1, #1
    streqb r1, [r0, #0x1c]
    b L_02226bf8
    ldrb r1, [r4, #0x18c]
    cmp r1, #127
    beq L_02226bf8
    cmp r1, #2
    moveq r1, #1
    streqb r1, [r0, #0x1c]
    b L_02226bf8
L_02226bb8:
    ldrb r0, [r4, #0x18c]
    cmp r0, #127
    beq L_02226bf8
    cmp r0, #1
    movne r0, #127
    strneb r0, [r4, #0x18c]
    bne L_02226bf8
    ldr r0, [pc, #0x2c]
    mov r1, #1
    strb r1, [r0, #0x1c]
    b L_02226bf8
L_02226be4:
    ldrb r0, [r4, #0x193]
    cmp r0, #0
    ldrne r0, [pc, #0x14]
    movne r1, #1
    strneb r1, [r0, #0x1c]
L_02226bf8:
    ldr r0, [pc, #0x8]
    ldrsb r0, [r0, #28]
    ldmia sp!, {r4, pc}
    dcd 0x02246aa8
    dcd 0x022468b8
}
