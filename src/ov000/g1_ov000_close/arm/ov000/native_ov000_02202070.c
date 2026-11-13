/* ov000 row 0x02202070: 324 bytes.
 *
 * What it does: 77 instructions; 9 call(s) to 0x02215698, 0x02217440, 0x02216350, +6 more; loops (back edge at +0x80); returns through pop {r4, r5, r6, r7, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x134 -> constant 0x02237d9c (image word 0x02237d9c)
 *   pool +0x138 -> constant 0x02237d94 (image word 0x02237d94)
 *   pool +0x13c -> constant 0x02237f7c (image word 0x02237f7c)
 *   pool +0x140 -> constant 0x02237e8c (image word 0x02237e8c)
 *   branch +0x18 -> +0x2c
 *   branch +0x20 -> +0x5c
 *   branch +0x28 -> +0x124
 *   branch +0x58 -> +0x124
 *   branch +0x7c -> +0x94
 *   branch +0x90 -> +0x9c
 *   test +0x14 cmp r7, #1
 *   test +0x1c cmp r7, #3
 *   test +0x24 cmp r7, #5
 *   test +0x78 cmp r0, #12
 *   test +0x88 cmp r0, #6
 *   1 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02202070; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_02217440(void);
extern void native_fn_02216350(void);
extern void native_fn_022015c8(void);
extern void native_fn_02216260(void);
extern void native_fn_02215094(void);
extern void native_fn_022021b4(void);


asm u32 native_ov000_02202070 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #20
    mov r7, r0
    bl ov000_display_context_02215698
    bl native_fn_02217440
    cmp r7, #1
    beq ov000_02202070_L2c
    cmp r7, #3
    beq ov000_02202070_L5c
    cmp r7, #5
    b ov000_02202070_L124
ov000_02202070_L2c:
    mov r0, #8
    str r0, [sp]
    mov r2, #4
    str r2, [sp, #0x4]
    ldr r0, =0x02237d9c
    str r2, [sp, #0x8]
    mov r4, #0
    mov r1, #1
    mov r3, #23
    str r4, [sp, #0xc]
    bl native_fn_02216350
    b ov000_02202070_L124
ov000_02202070_L5c:
    bl native_fn_02217440
    ldr r1, =0x02237d94
    ldr r2, =0x02237f7c
    ldr r1, [r1, #0x8]
    mov r5, r0
    ldrb r0, [r2, r1]
    ldr r4, =0x02237e8c
    cmp r0, #12
    bne ov000_02202070_L94
    bl native_fn_022015c8
    mov r2, r0
    cmp r0, #6
    movhi r2, #6
    b ov000_02202070_L9c
ov000_02202070_L94:
    mov r0, #2
    mov r2, r0
ov000_02202070_L9c:
    mov r6, r2, lsl #1
    and r1, r6, #255
    stmia sp, {r1, r2}
    str r0, [sp, #0x8]
    mov r12, #0
    mov r0, r4
    mov r1, #1
    mov r2, #5
    mov r3, #12
    str r12, [sp, #0xc]
    bl native_fn_02216350
    mov r1, #3
    str r1, [sp]
    mov r1, #30
    str r1, [sp, #0x4]
    mov r2, #2
    mov r0, #1
    str r2, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    str r0, [sp, #0x10]
    ldrsb r1, [r5, #16]
    mov r3, r0
    bl native_fn_02216260
    sub r0, r6, #1
    mov r0, r0, lsl #3
    add r0, r0, #48
    mov r1, #112
    and r0, r0, #255
    str r0, [sp]
    mov r3, r1
    add r0, r4, #168
    mov r2, #48
    bl native_fn_02215094
ov000_02202070_L124:
    mov r0, r7
    bl native_fn_022021b4
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, pc}
}
