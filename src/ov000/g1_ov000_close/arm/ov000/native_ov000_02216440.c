/* ov000 row 0x02216440: 548 bytes.
 *
 * What it does: 135 instructions; 9 call(s) to 0x02008be0, 0x02216414, 0x02046af4, +6 more; loops (back edge at +0x54); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x21c -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x220 -> constant 0x0224536c (image word 0x0224536c)
 *   branch +0x44 -> +0xe8
 *   back edge +0x210 -> +0x17c
 *   test +0x24 cmp r11, #0
 *   test +0x40 cmp r0, #0
 *   test +0x14c cmp r6, #0
 *   test +0x208 cmp r6, r0, asr #24
 *   1 block transfer(s), 25 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02216440; the literal pool and
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

extern void native_fn_02008be0(void);
extern void native_fn_02216414(void);
extern void native_fn_02046af4(void);
extern void native_fn_020470fc(void);
extern void native_fn_02087d0c(void);
extern void native_fn_02216260(void);


asm u32 native_ov000_02216440 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #88
    ldr r7, [sp, #0x8c]
    ldr r6, =0x021c9698
    str r3, [sp, #0x14]
    sub r3, r3, r7
    mov r3, r3, lsl #24
    mov r11, r3, asr #24
    ldr r8, [sp, #0x88]
    cmp r11, #0
    mov r5, r0
    mov r10, r1
    mov r9, r2
    addle sp, sp, #88
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [sp, #0x90]
    cmp r0, #0
    beq ov000_02216440_Le8
    add r1, sp, #24
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    bl native_fn_02216414
    mov r1, r0
    add r0, sp, #24
    mov r3, #0
    stmia sp, {r0, r3}
    mov r0, r6
    mov r2, #32
    bl native_fn_02046af4
    mov r4, r0
    bl native_fn_020470fc
    mov r2, r0
    mov r1, r4
    mov r0, r6
    bl native_fn_02087d0c
    add r0, r0, #7
    mov r0, r0, asr #3
    add r0, r0, #4
    and r3, r0, #255
    str r9, [sp]
    str r3, [sp, #0x4]
    mov r2, #2
    str r2, [sp, #0x8]
    mov r0, #1
    str r0, [sp, #0xc]
    str r0, [sp, #0x10]
    ldr r1, [sp, #0x14]
    ldr r4, =0x0224536c
    add r6, r10, r1
    ldrsb r1, [r4, #16]
    add r4, r6, #2
    sub r3, r4, r3
    mov r0, #23
    and r3, r3, #255
    bl native_fn_02216260
    add r0, r9, #1
    and r9, r0, #255
ov000_02216440_Le8:
    ldrb r6, [sp, #0x80]
    ldr r0, [sp, #0x14]
    mov r3, r10
    add r1, r0, #2
    mov r0, r6, lsl #1
    add r0, r0, #2
    str r9, [sp]
    and r1, r1, #255
    str r1, [sp, #0x4]
    and r0, r0, #255
    str r0, [sp, #0x8]
    mov r0, #1
    str r0, [sp, #0xc]
    mov r1, #0
    ldr r0, =0x0224536c
    str r1, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, #4
    mov r2, #12
    bl native_fn_02216260
    ldrb r1, [sp, #0x80]
    add r3, r10, #1
    add r2, r9, #1
    ldrb r0, [sp, #0x84]
    strh r1, [r5, #12]
    cmp r6, #0
    mov r4, #0
    strh r0, [r5, #14]
    str r4, [r5, #0x4]
    and r10, r3, #255
    and r9, r2, #255
    addle sp, sp, #88
    str r4, [r5]
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r0, r10, r7
    and r5, r11, #255
    and r11, r0, #255
ov000_02216440_L17c:
    str r9, [sp]
    str r7, [sp, #0x4]
    mov r0, #2
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    ldr r1, =0x0224536c
    add r0, r4, #5
    mov r0, r0, lsl #24
    ldrsb r1, [r1, #16]
    mov r0, r0, asr #24
    mov r2, #5
    mov r3, r10
    bl native_fn_02216260
    str r9, [sp]
    str r5, [sp, #0x4]
    mov r0, #2
    str r0, [sp, #0x8]
    str r8, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    ldr r1, =0x0224536c
    add r0, r4, #12
    mov r0, r0, lsl #24
    ldrsb r1, [r1, #16]
    mov r0, r0, asr #24
    mov r2, #6
    mov r3, r11
    bl native_fn_02216260
    add r0, r9, #2
    and r9, r0, #255
    add r0, r4, #1
    mov r0, r0, lsl #24
    cmp r6, r0, asr #24
    mov r4, r0, asr #24
    bgt ov000_02216440_L17c
    add sp, sp, #88
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
