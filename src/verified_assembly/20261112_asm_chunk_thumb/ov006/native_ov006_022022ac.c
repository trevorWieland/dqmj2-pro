/* ov006 row 0x022022ac: 56 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x34 -> native_data2_0221c16c (image word 0x0221c16c)
 *   branch +0x18 -> +0x1e
 *   branch +0x1c -> +0x20
 *   test +0x16 cmp r3, r0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022022ac; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 56 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data2_0221c16c[];


asm u32 native_ov006_022022ac (register u32 a0)
{
    push {r3, r4}
    ldr r3, =native_data2_0221c16c
    mov r2, #0xa9
    ldr r4, [r3, #0]
    lsl r2, r2, #0x4
    ldrb r4, [r4, r2]
    strb r4, [r0, #0]
    ldr r4, [r3, #0]
    add r0, r2, #0x1
    ldrb r3, [r4, r2]
    ldrb r0, [r4, r0]
    cmp r3, r0
    beq ov006_022022ac_L1e
    mov r0, #0x1
    b ov006_022022ac_L20
ov006_022022ac_L1e:
    mov r0, #0x0
ov006_022022ac_L20:
    strb r0, [r1, #0]
    ldr r0, =native_data2_0221c16c
    ldr r2, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    ldrb r1, [r2, r0]
    add r0, r0, #0x1
    strb r1, [r2, r0]
    pop {r3, r4}
    bx lr
}
