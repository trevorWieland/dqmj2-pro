/* ov000 row 0x022215ec: 388 bytes.
 *
 * What it does: 95 instructions; 1 call(s) to 0x02008ca4; loops (back edge at +0x140); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x17c -> constant 0x02246428 (image word 0x02246428)
 *   pool +0x180 -> constant 0x06840000 (image word 0x06840000)
 *   branch +0x28 -> +0x170
 *   back edge +0x140 -> +0x34
 *   test +0x1c cmp r7, #0
 *   test +0x20 cmpne r8, #0
 *   test +0x24 cmpne r9, #0
 *   test +0x130 cmp r11, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022215ec; the literal pool and
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


asm u32 native_ov000_022215ec (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    ldr r1, =0x02246428
    ldr r2, [r1]
    ldr r7, [r1, #0x8]
    ldr r9, [r1, #0x4]
    add r8, r2, #8
    cmp r7, #0
    cmpne r8, #0
    cmpne r9, #0
    beq ov000_022215ec_L170
    ldr r3, [sp]
    mov r11, #24576
ov000_022215ec_L34:
    ldr r5, [r8]
    ldr r6, [r7]
    mov r1, r5, lsl #27
    mov r4, r6, lsl #27
    mov r1, r1, lsr #27
    sub r1, r1, r4, lsr #27
    mov lr, r5, lsl #22
    mul r10, r0, r1
    mov r12, r5, lsl #17
    mov r2, r5, lsl #11
    mov r1, r5, lsl #6
    mov r10, r10, lsr #5
    add r4, r10, r4, lsr #27
    mov r10, r5, lsl #1
    and r4, r4, #31
    mov lr, lr, lsr #27
    mov r12, r12, lsr #27
    mov r2, r2, lsr #27
    mov r1, r1, lsr #27
    mov r10, r10, lsr #27
    bic r3, r3, #31
    orr r3, r3, r4
    bic r3, r3, #992
    mov r4, r6, lsl #22
    sub lr, lr, r4, lsr #27
    mul r14, r0, r14
    mov lr, lr, lsr #5
    add r4, lr, r4, lsr #27
    mov r4, r4, lsl #27
    orr r4, r3, r4, lsr #22
    mov r3, r6, lsl #17
    bic r4, r4, #31744
    sub r12, r12, r3, lsr #27
    mul r12, r0, r12
    mov r12, r12, lsr #5
    add r12, r12, r3, lsr #27
    mov r3, r6, lsl #11
    mov r12, r12, lsl #27
    orr r4, r4, r12, lsr #17
    sub r2, r2, r3, lsr #27
    mul r12, r0, r2
    mov r2, r6, lsl #6
    bic r4, r4, #2031616
    mov r12, r12, lsr #5
    add r3, r12, r3, lsr #27
    sub r1, r1, r2, lsr #27
    mul r12, r0, r1
    mov r1, r6, lsl #1
    mov r3, r3, lsl #27
    orr r3, r4, r3, lsr #11
    sub r4, r10, r1, lsr #27
    mul r4, r0, r4
    mov r10, r12, lsr #5
    add r10, r10, r2, lsr #27
    mov r2, r4, lsr #5
    add r1, r2, r1, lsr #27
    bic r3, r3, #65011712
    mov r2, r10, lsl #27
    orr r2, r3, r2, lsr #6
    bic r2, r2, #2080374784
    mov r1, r1, lsl #27
    orr r3, r2, r1, lsr #1
    sub r11, r11, #1
    cmp r11, #0
    str r3, [r9], #4
    add r7, r7, #4
    add r8, r8, #4
    bgt ov000_022215ec_L34
    ldr r0, =0x02246428
    ldr r1, =0x06840000
    ldr r0, [r0, #0x4]
    mov r2, #98304
    str r3, [sp]
    str r5, [sp, #0x4]
    str r6, [sp, #0x8]
    bl native_fn_02008ca4
    add sp, sp, #12
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_022215ec_L170:
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
