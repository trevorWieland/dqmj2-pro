/* ov006 row 0x021f5dcc: 40 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x20 -> native_data_0220b534 (image word 0x0220b534)
 *   pool +0x24 -> constant 0x0221c09c (image word 0x0221c09c)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5dcc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 40 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b534[];
extern void native_fn_021fe580(void);


asm u32 native_ov006_021f5dcc (register u32 a0)
{
    push {r3, lr}
    ldr r1, =native_data_0220b534
    add r0, sp, #0x0
    ldrb r2, [r1, #0]
    ldrb r1, [r1, #0x1]
    add r3, sp, #0x0
    strb r2, [r0, #0]
    strb r1, [r0, #0x1]
    ldr r0, =0x0221c09c
    ldrb r1, [r0, #0]
    ldr r0, [r0, #0x4]
    ldrb r1, [r3, r1]
    add r2, r1, #0x0
    bl native_fn_021fe580
    pop {r3, pc}
}
