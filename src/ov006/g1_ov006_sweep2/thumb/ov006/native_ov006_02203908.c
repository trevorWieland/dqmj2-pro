/* ov006 row 0x02203908: 76 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x44 -> constant 0x04001000 (image word 0x04001000)
 *   pool +0x48 -> constant 0xffffe0ff (image word 0xffffe0ff)
 *   branch +0x04 -> +0x24
 *   test +0x02 cmp r0, #0x1
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02203908; the literal pool and
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



asm u32 native_ov006_02203908 (register u32 a0)
{
    push {r3, r4}
    cmp r0, #0x1
    bne ov006_02203908_L24
    ldr r0, =0x04001000
    mov r2, #0x1f
    ldr r3, [r0, #0]
    lsl r2, r2, #0x8
    and r2, r3
    lsr r4, r2, #0x8
    orr r1, r4
    ldr r3, [r0, #0]
    ldr r2, =0xffffe0ff
    lsl r1, r1, #0x8
    and r2, r3
    orr r1, r2
    str r1, [r0, #0]
    pop {r3, r4}
    bx lr
ov006_02203908_L24:
    mov r0, #0x1
    lsl r0, r0, #0x1a
    mov r2, #0x1f
    ldr r3, [r0, #0]
    lsl r2, r2, #0x8
    and r2, r3
    lsr r4, r2, #0x8
    orr r1, r4
    ldr r3, [r0, #0]
    ldr r2, =0xffffe0ff
    lsl r1, r1, #0x8
    and r2, r3
    orr r1, r2
    str r1, [r0, #0]
    pop {r3, r4}
    bx lr
}
