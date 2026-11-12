/* ov001 row 0x021eeab8: 168 bytes.
 *
 * What it does: 40 instructions; 4 call(s) to 0x021eead0, 0x0205c79c, 0x021eeafc, +1 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (40 instructions, 4 calls, 5 branches, 3 back edges, 2 literal slots).
 *
 *   pool +0xa0 -> constant 0x02238e58 (image word 0x02238e58)
 *   pool +0xa4 -> constant 0x02238e5c (image word 0x02238e5c)
 *   branch +0x24 -> +0x34
 *   back edge +0x30 -> +0x18
 *   branch +0x38 -> +0x80
 *   branch +0x4c -> +0x74
 *   branch +0x5c -> +0x80
 *   branch +0x70 -> +0x80
 *   back edge +0x7c -> +0x44
 *   branch +0x84 -> +0x98
 *   test +0x1c cmp r6, r0
 *   test +0x2c cmp r2, #32
 *   test +0x34 cmp r4, #0
 *   test +0x48 cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x78 cmp r7, #32
 *   test +0x80 cmp r4, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021eeab8; the literal pool and
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

extern void native_fn_0205c79c(void);


asm u32 native_ov001_021eeab8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r5, #0
    ldr r1, =0x02238e58
    mov r6, r0
    mov r2, r5
    sub r4, r5, #1
ov001_021eeab8_L18:
    ldr r0, [r1, r2, lsl #3]
    cmp r6, r0
    moveq r4, r2
    beq ov001_021eeab8_L34
    add r2, r2, #1
    cmp r2, #32
    blt ov001_021eeab8_L18
ov001_021eeab8_L34:
    cmp r4, #0
    bge ov001_021eeab8_L80
    ldr r1, =0x02238e58
    mov r7, #0
ov001_021eeab8_L44:
    ldr r0, [r1, r7, lsl #3]
    cmp r0, #0
    bne ov001_021eeab8_L74
    mov r0, r6
    bl native_fn_0205c79c
    cmp r0, #0
    beq ov001_021eeab8_L80
    ldr r0, =0x02238e58
    mov r4, r7
    str r6, [r0, r7, lsl #3]
    mov r5, #1
    b ov001_021eeab8_L80
ov001_021eeab8_L74:
    add r7, r7, #1
    cmp r7, #32
    blt ov001_021eeab8_L44
ov001_021eeab8_L80:
    cmp r4, #0
    blt ov001_021eeab8_L98
    ldr r1, =0x02238e5c
    ldrb r0, [r1, r4, lsl #3]
    add r0, r0, #1
    strb r0, [r1, r4, lsl #3]
ov001_021eeab8_L98:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
