/* ov000 row 0x02221770: 300 bytes.
 *
 * What it does: 73 instructions; 1 call(s) to 0x02008ca4; loops (back edge at +0xec); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x124 -> constant 0x02246428 (image word 0x02246428)
 *   pool +0x128 -> constant 0x06840000 (image word 0x06840000)
 *   branch +0x28 -> +0x118
 *   back edge +0xec -> +0x34
 *   test +0x1c cmp r2, #0
 *   test +0x20 cmpne r4, #0
 *   test +0x24 cmpne r5, #0
 *   test +0xe4 cmp lr, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02221770; the literal pool and
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

extern void native_fn_02008ca4(void);


asm u32 native_ov000_02221770 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #8
    ldr r1, =0x02246428
    ldr r3, [r1]
    ldr r2, [r1, #0x8]
    ldr r5, [r1, #0x4]
    add r4, r3, #8
    cmp r2, #0
    cmpne r4, #0
    cmpne r5, #0
    beq ov000_02221770_L118
    ldr r8, [sp]
    mov lr, #24576
ov000_02221770_L34:
    ldr r12, [r4], #4
    sub lr, lr, #1
    mov r1, r12, lsl #27
    mov r1, r1, lsr #27
    mul r3, r1, r0
    mov r1, r12, lsl #22
    mov r1, r1, lsr #27
    mul r2, r1, r0
    mov r1, r12, lsl #17
    mov r6, r1, lsr #27
    mul r1, r6, r0
    mov r6, r12, lsl #11
    mov r6, r6, lsr #27
    mov r3, r3, lsr #5
    mul r10, r6, r0
    mov r6, r12, lsl #6
    mov r6, r6, lsr #27
    mov r2, r2, lsr #5
    mul r9, r6, r0
    mov r6, r12, lsl #1
    mov r6, r6, lsr #27
    mov r1, r1, lsr #5
    mul r7, r6, r0
    mov r6, r10, lsr #5
    mov r9, r9, lsr #5
    mov r7, r7, lsr #5
    bic r8, r8, #31
    and r3, r3, #31
    orr r3, r8, r3
    bic r3, r3, #992
    mov r2, r2, lsl #27
    orr r2, r3, r2, lsr #22
    bic r2, r2, #31744
    mov r1, r1, lsl #27
    orr r1, r2, r1, lsr #17
    bic r2, r1, #2031616
    mov r1, r6, lsl #27
    orr r1, r2, r1, lsr #11
    bic r2, r1, #65011712
    mov r1, r9, lsl #27
    orr r1, r2, r1, lsr #6
    bic r2, r1, #2080374784
    mov r1, r7, lsl #27
    orr r8, r2, r1, lsr #1
    cmp lr, #0
    str r8, [r5], #4
    bgt ov000_02221770_L34
    ldr r0, =0x02246428
    ldr r1, =0x06840000
    ldr r0, [r0, #0x4]
    mov r2, #98304
    str r8, [sp]
    str r12, [sp, #0x4]
    bl native_fn_02008ca4
    add sp, sp, #8
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov000_02221770_L118:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
