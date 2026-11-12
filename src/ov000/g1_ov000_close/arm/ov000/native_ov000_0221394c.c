/* ov000 row 0x0221394c: 256 bytes.
 *
 * What it does: 62 instructions; 1 call(s) to 0x02213970; loops (back edge at +0xe8); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xf8 -> constant 0x02243e3c (image word 0x02243e3c)
 *   pool +0xfc -> constant 0x00000a3c (image word 0x00000a3c)
 *   branch +0x34 -> +0xdc
 *   branch +0x88 -> +0xdc
 *   branch +0x94 -> +0xd4
 *   branch +0xd8 -> +0xec
 *   back edge +0xe8 -> +0x24
 *   test +0x28 cmp r0, #0
 *   test +0x30 cmpne r0, #5
 *   test +0x8c cmp r6, #0
 *   test +0xd4 cmp r4, #0
 *   test +0xe0 cmp lr, #16
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221394c; the literal pool and
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



asm u32 native_ov000_0221394c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r4, #0
    ldr r5, =0x02243e3c
    mov r7, r0
    mov r6, r1
    mov lr, r4
    add r12, sp, #0
    mov r11, r4
ov000_0221394c_L24:
    ldrb r0, [r5, #0x105]
    cmp r0, #0
    ldrneb r0, [r5, #0x106]
    cmpne r0, #5
    beq ov000_0221394c_Ldc
    add r0, r5, #112
    ldmia r0, {r0, r1, r2}
    stmia r12, {r0, r1, r2}
    ldr r10, [sp, #0x4]
    ldr r0, [r7, #0x4]
    ldr r2, [r7]
    sub r3, r0, r10
    smull r0, r1, r3, r3
    ldr r9, [sp]
    ldr r3, [sp, #0x8]
    sub r2, r2, r9
    smlal r0, r1, r2, r2
    ldr r2, [r7, #0x8]
    sub r2, r2, r3
    smlal r0, r1, r2, r2
    mov r2, r0, lsr #12
    ldr r0, =0x00000a3c
    orr r2, r2, r1, lsl #20
    subs r0, r2, r0
    rscs r0, r11, r1, asr #12
    bge ov000_0221394c_Ldc
    cmp r6, #0
    moveq r4, #1
    beq ov000_0221394c_Ld4
    ldr r0, [r6, #0x4]
    ldr r8, [r6]
    sub r0, r0, r10
    sub r10, r8, r9
    smull r9, r8, r0, r0
    smlal r9, r8, r10, r10
    ldr r0, [r6, #0x8]
    sub r0, r0, r3
    smlal r9, r8, r0, r0
    mov r0, r9, lsr #12
    orr r0, r0, r8, lsl #20
    mov r3, r8, asr #12
    subs r0, r2, r0
    rscs r0, r3, r1, asr #12
    movlt r4, #1
ov000_0221394c_Ld4:
    cmp r4, #0
    bne ov000_0221394c_Lec
ov000_0221394c_Ldc:
    add lr, lr, #1
    cmp lr, #16
    add r5, r5, #268
    blt ov000_0221394c_L24
ov000_0221394c_Lec:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
