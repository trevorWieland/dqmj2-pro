/* ov006 row 0x021f9ac4: 56 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x2c -> constant 0x0221c0e4 (image word 0x0221c0e4)
 *   pool +0x30 -> native_data_0220b6c8 (image word 0x0220b6c8)
 *   pool +0x34 -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   branch +0x08 -> +0x0c
 *   test +0x06 cmp r2, #0x3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f9ac4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 12 of 56 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b6c8[];


asm u32 native_ov006_021f9ac4 (register u32 a0)
{
    ldr r0, =0x0221c0e4
    ldr r0, [r0, #0]
    ldrb r2, [r0, #0x14]
    cmp r2, #0x3
    ble ov006_021f9ac4_Lc
    mov r2, #0x3
ov006_021f9ac4_Lc:
    lsl r1, r2, #0x1
    add r1, r2, r1
    add r2, r1, #0x2
    ldr r1, =native_data_0220b6c8
    ldr r0, [r0, #0x4]
    ldrb r1, [r1, r2]
    ldr r2, [r0, #0]
    lsl r1, r1, #0x17
    lsr r3, r1, #0x7
    ldr r1, =0xfe00ff00
    and r2, r1
    mov r1, #0x28
    orr r1, r2
    orr r1, r3
    str r1, [r0, #0]
    bx lr
}
