/* ov006 row 0x0220410c: 68 bytes.
 *
 * What it does: 30 instructions; no calls; no back edge; returns through bx lr; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x3c -> constant 0x027fffa8 (image word 0x027fffa8)
 *   pool +0x40 -> constant 0x0221c18c (image word 0x0221c18c)
 *   branch +0x0c -> +0x12
 *   branch +0x20 -> +0x2e
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220410c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_ov006_0220410c (register u32 a0)
{
    ldr r1, =0x027fffa8
    ldrh r2, [r1, #0]
    mov r1, #0x2
    lsl r1, r1, #0xe
    and r1, r2
    asr r1, r1, #0xf
    beq ov006_0220410c_L12
    mov r0, #0x0
    bx lr
ov006_0220410c_L12:
    ldr r1, =0x0221c18c
    ldr r2, [r1, #0x4]
    add r1, r2, #0x0
    add r1, #0x38
    ldrb r1, [r1, #0]
    lsl r1, r1, #0x1f
    lsr r1, r1, #0x1f
    bne ov006_0220410c_L2e
    ldrh r1, [r2, #0x2c]
    strh r1, [r0, #0]
    ldrh r1, [r2, #0x2e]
    strh r1, [r0, #0x2]
    mov r0, #0x0
    bx lr
ov006_0220410c_L2e:
    ldrh r1, [r2, #0x28]
    strh r1, [r0, #0]
    ldrh r1, [r2, #0x2a]
    strh r1, [r0, #0x2]
    mov r0, #0x1
    bx lr
    mov r8, r8
}
