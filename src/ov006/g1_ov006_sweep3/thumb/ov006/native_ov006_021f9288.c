/* ov006 row 0x021f9288: 76 bytes.
 *
 * What it does: 30 instructions; 1 call(s) to 0x021f92a4; no back edge; returns through bx lr; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x3c -> constant 0x0221c0e0 (image word 0x0221c0e0)
 *   pool +0x40 -> native_data_0220b678 (image word 0x0220b678)
 *   pool +0x44 -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0x48 -> native_data_0220b674 (image word 0x0220b674)
 *   branch +0x16 -> +0x1c
 *   test +0x14 cmp r1, #0x20
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f9288; the literal pool and
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

extern u8 native_data_0220b678[];
extern u8 native_data_0220b674[];


asm u32 native_ov006_021f9288 (register u32 a0)
{
    push {r3, r4}
    ldr r0, =0x0221c0e0
    ldr r4, [r0, #0]
    add r0, r4, #0x0
    add r0, #0x29
    ldrb r1, [r0, #0]
    mov r0, #0xf
    add r3, r1, #0x0
    and r3, r0
    asr r2, r1, #0x4
    cmp r1, #0x20
    blo ov006_021f9288_L1c
    add r3, r0, #0x0
    mov r2, #0x1
ov006_021f9288_L1c:
    ldr r1, [r4, #0x4]
    ldr r0, =native_data_0220b678
    ldr r4, [r1, #0]
    ldrb r0, [r0, r3]
    ldr r3, =0xfe00ff00
    and r4, r3
    ldr r3, =native_data_0220b674
    lsl r0, r0, #0x17
    ldrb r2, [r3, r2]
    lsr r0, r0, #0x7
    orr r2, r4
    orr r0, r2
    str r0, [r1, #0]
    pop {r3, r4}
    bx lr
    mov r8, r8
}
