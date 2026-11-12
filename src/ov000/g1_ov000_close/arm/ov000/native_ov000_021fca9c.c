/* ov000 row 0x021fca9c: 584 bytes.
 *
 * What it does: 145 instructions; 18 call(s) to 0x02215698, 0x02217440, 0x02216260, +15 more; loops (back edge at +0x9c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x244 -> constant 0x022372a8 (image word 0x022372a8)
 *   branch +0x2c -> +0x44
 *   branch +0x34 -> +0xa4
 *   branch +0x3c -> +0x158
 *   branch +0x40 -> +0x234
 *   branch +0xa0 -> +0x234
 *   branch +0x138 -> +0x234
 *   branch +0x154 -> +0x234
 *   test +0x28 cmp r4, #0
 *   test +0x30 cmp r4, #2
 *   test +0x38 cmp r4, #4
 *   test +0xd0 cmp r6, #6
 *   test +0x12c cmp r8, r6
 *   test +0x194 cmp r7, #6
 *   1 block transfer(s), 37 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fca9c; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_02217440(void);
extern void native_fn_02216260(void);
extern void native_fn_0204a574(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_022163fc(void);
extern void native_fn_02216440(void);
extern void native_fn_021fdf28(void);
extern void native_fn_02026144(void);
extern void native_fn_022166dc(void);
extern void native_fn_022179fc(void);
extern void native_fn_02217b08(void);
extern void native_fn_021fcd4c(void);


asm u32 native_ov000_021fca9c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #32
    mov r4, r0
    bl native_fn_02215698
    bl native_fn_02217440
    mov r6, r0
    add r1, sp, #28
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    cmp r4, #0
    beq ov000_021fca9c_L44
    cmp r4, #2
    beq ov000_021fca9c_La4
    cmp r4, #4
    beq ov000_021fca9c_L158
    b ov000_021fca9c_L234
ov000_021fca9c_L44:
    mov r1, #16
    strh r1, [sp, #28]
    mov r2, #1
    str r2, [sp]
    str r1, [sp, #0x4]
    mov r1, #2
    str r1, [sp, #0x8]
    str r0, [sp, #0xc]
    str r2, [sp, #0x10]
    ldrsb r1, [r6, #16]
    mov r3, r0
    mov r2, #127
    bl native_fn_02216260
    mov r1, #3
    mov r0, #0
    str r1, [sp]
    mov r5, #1
    str r5, [sp, #0x4]
    add r1, sp, #28
    mov r3, r0
    mov r2, #5
    str r5, [sp, #0x8]
    bl native_fn_0204a574
    b ov000_021fca9c_L234
ov000_021fca9c_La4:
    ldr r0, =0x022372a8
    mov r1, #16
    ldr r5, [r0, #0xc]
    strh r1, [sp, #28]
    ldr r8, [r5, #0xc]
    ldr r9, [r5, #0x10]
    bl native_fn_02062aa0
    mov r6, r0
    bl native_fn_02062ad0
    add r0, r6, r0
    and r6, r0, #255
    cmp r6, #6
    movlo r0, r6
    movhs r0, #6
    and r0, r0, #255
    add r0, r0, #1
    and r7, r0, #255
    mov r0, #5
    mov r1, #1
    mov r2, #4
    bl native_fn_022163fc
    str r7, [sp]
    str r7, [sp, #0x4]
    mov r1, #1
    str r1, [sp, #0x8]
    mov r0, #15
    str r0, [sp, #0xc]
    add r0, r5, #12
    mov r2, #3
    mov r3, #28
    str r1, [sp, #0x10]
    bl native_fn_02216440
    mov r0, #224
    bl native_fn_021fdf28
    cmp r8, r6
    strlt r9, [r5, #0x10]
    strlt r8, [r5, #0xc]
    blt ov000_021fca9c_L234
    sub r0, r6, #1
    mov r1, r7
    str r0, [r5, #0xc]
    bl native_fn_02026144
    mul r0, r7, r0
    str r0, [r5, #0x10]
    b ov000_021fca9c_L234
ov000_021fca9c_L158:
    ldr r0, =0x022372a8
    mov r1, #16
    ldr r5, [r0, #0xc]
    strh r1, [sp, #28]
    ldr r0, [r5, #0x5f0]
    mov r1, #27
    add r0, r0, #2
    and r7, r0, #255
    mov r0, #16
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    str r1, [sp, #0xc]
    cmp r7, #6
    movlo r8, r7
    str r0, [sp, #0x10]
    mov r3, #2
    str r3, [sp, #0x14]
    movhs r8, #6
    mov r1, #5
    mov r2, #30
    str r3, [sp, #0x18]
    bl native_fn_022166dc
    and r0, r8, #255
    stmia sp, {r0, r7}
    mov r7, #0
    str r7, [sp, #0x8]
    mov r0, #16
    str r0, [sp, #0xc]
    add r0, r5, #252
    mov r1, #1
    mov r2, #7
    mov r3, #28
    str r7, [sp, #0x10]
    bl native_fn_02216440
    mov r0, #224
    bl native_fn_021fdf28
    bl native_fn_022179fc
    bl native_fn_02217b08
    mov r0, #21
    str r0, [sp]
    mov r0, #28
    str r0, [sp, #0x4]
    mov r2, #2
    str r2, [sp, #0x8]
    mov r0, r7
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    ldrsb r1, [r6, #16]
    mov r0, #24
    mov r3, r2
    bl native_fn_02216260
ov000_021fca9c_L234:
    mov r0, r4
    bl native_fn_021fcd4c
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
