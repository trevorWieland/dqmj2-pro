/* ov006 row 0x0220406c: 96 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x58 -> constant 0x027fffa8 (image word 0x027fffa8)
 *   pool +0x5c -> constant 0x0221c18c (image word 0x0221c18c)
 *   branch +0x0c -> +0x12
 *   branch +0x20 -> +0x26
 *   branch +0x2c -> +0x32
 *   branch +0x36 -> +0x3c
 *   branch +0x42 -> +0x48
 *   branch +0x4c -> +0x52
 *   test +0x2a cmp r2, r3
 *   test +0x34 cmp r2, r3
 *   test +0x40 cmp r1, r2
 *   test +0x4a cmp r0, r2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220406c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_ov006_0220406c (register u32 a0)
{
    ldr r1, =0x027fffa8
    ldrh r2, [r1, #0]
    mov r1, #0x2
    lsl r1, r1, #0xe
    and r1, r2
    asr r1, r1, #0xf
    beq ov006_0220406c_L12
    mov r0, #0x0
    bx lr
ov006_0220406c_L12:
    ldr r1, =0x0221c18c
    ldr r1, [r1, #0x4]
    add r2, r1, #0x0
    add r2, #0x38
    ldrb r2, [r2, #0]
    lsl r2, r2, #0x1c
    lsr r2, r2, #0x1f
    bne ov006_0220406c_L26
    mov r0, #0x0
    bx lr
ov006_0220406c_L26:
    ldrh r3, [r1, #0x28]
    ldrh r2, [r0, #0]
    cmp r2, r3
    bls ov006_0220406c_L32
    mov r0, #0x0
    bx lr
ov006_0220406c_L32:
    ldrh r2, [r0, #0x4]
    cmp r2, r3
    bhs ov006_0220406c_L3c
    mov r0, #0x0
    bx lr
ov006_0220406c_L3c:
    ldrh r2, [r1, #0x2a]
    ldrh r1, [r0, #0x2]
    cmp r1, r2
    bls ov006_0220406c_L48
    mov r0, #0x0
    bx lr
ov006_0220406c_L48:
    ldrh r0, [r0, #0x6]
    cmp r0, r2
    blo ov006_0220406c_L52
    mov r0, #0x1
    bx lr
ov006_0220406c_L52:
    mov r0, #0x0
    bx lr
    mov r8, r8
}
