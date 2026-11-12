/* ov006 row 0x02201a20: 140 bytes.
 *
 * What it does: 64 instructions; 3 call(s) to 0x02201a2c, 0x02201a9c, 0x02201a72; loops (back edge at +0x28); returns through bx lr; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x80 -> constant 0x0221c164 (image word 0x0221c164)
 *   pool +0x84 -> constant 0x00010dcd (image word 0x00010dcd)
 *   pool +0x88 -> constant 0x00003039 (image word 0x00003039)
 *   branch +0x12 -> +0x20
 *   back edge +0x28 -> +0x0c
 *   branch +0x2c -> +0x7c
 *   branch +0x56 -> +0x6c
 *   branch +0x5a -> +0x66
 *   back edge +0x78 -> +0x52
 *   test +0x10 tst r5, r4
 *   test +0x26 cmp r2, #0x10
 *   test +0x2a cmp r3, #0x1
 *   test +0x54 tst r0, r1
 *   test +0x58 cmp r2, #0x0
 *   test +0x76 cmp r3, #0x10
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02201a20; the literal pool and
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



asm u32 native_ov006_02201a20 (register u32 a0)
{
    push {r3, r4, r5, r6}
    add r4, r0, #0x0
    mov r0, #0x0
    add r3, r0, #0x0
    add r2, r0, #0x0
    mov r1, #0x1
ov006_02201a20_Lc:
    add r5, r1, #0x0
    lsl r5, r2
    tst r5, r4
    beq ov006_02201a20_L20
    add r0, r2, #0x1
    add r3, r3, #0x1
    lsl r0, r0, #0x10
    lsl r3, r3, #0x10
    asr r0, r0, #0x10
    lsr r3, r3, #0x10
ov006_02201a20_L20:
    add r2, r2, #0x1
    lsl r2, r2, #0x10
    asr r2, r2, #0x10
    cmp r2, #0x10
    blt ov006_02201a20_Lc
    cmp r3, #0x1
    bls ov006_02201a20_L7c
    ldr r2, =0x0221c164
    ldr r1, =0x00010dcd
    ldr r0, [r2, #0x4]
    ldr r5, [r0, #0x58]
    add r6, r5, #0x0
    mul r6, r1
    ldr r1, =0x00003039
    add r1, r6, r1
    str r1, [r0, #0x58]
    ldr r0, [r2, #0x4]
    mov r1, #0x1
    ldr r0, [r0, #0x58]
    lsl r0, r0, #0x18
    lsr r0, r0, #0x18
    mul r0, r3
    lsl r0, r0, #0x8
    lsr r2, r0, #0x10
    mov r3, #0x0
ov006_02201a20_L52:
    add r0, r4, #0x0
    tst r0, r1
    beq ov006_02201a20_L6c
    cmp r2, #0x0
    bne ov006_02201a20_L66
    add r0, r3, #0x1
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    pop {r3, r4, r5, r6}
    bx lr
ov006_02201a20_L66:
    sub r0, r2, #0x1
    lsl r0, r0, #0x10
    lsr r2, r0, #0x10
ov006_02201a20_L6c:
    lsl r0, r4, #0xf
    lsr r4, r0, #0x10
    add r0, r3, #0x1
    lsl r0, r0, #0x10
    asr r3, r0, #0x10
    cmp r3, #0x10
    blt ov006_02201a20_L52
    mov r0, #0x0
ov006_02201a20_L7c:
    pop {r3, r4, r5, r6}
    bx lr
}
