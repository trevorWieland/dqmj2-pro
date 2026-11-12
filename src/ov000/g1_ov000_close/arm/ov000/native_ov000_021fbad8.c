/* ov000 row 0x021fbad8: 452 bytes.
 *
 * What it does: 113 instructions; 18 call(s) to 0x02062aa0, 0x02062ad0, 0x02062a50, +15 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill.
 *
 *   branch +0x28 -> +0x3c
 *   branch +0x38 -> +0x60
 *   branch +0x40 -> +0x54
 *   branch +0x50 -> +0x60
 *   branch +0x5c -> +0x1ac
 *   branch +0xc8 -> +0x1ac
 *   back edge +0x1b8 -> +0x24
 *   test +0x24 cmp r5, r6
 *   test +0x3c cmp r5, r11
 *   test +0x74 cmp r0, #0
 *   test +0xc4 cmp r0, #0
 *   test +0x1b4 cmp r5, #6
 *   7 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fbad8; the literal pool and
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

extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_02215d94(void);
extern void native_fn_0207c2b8(void);
extern void native_fn_0207c18c(void);
extern void native_fn_0207c3d8(void);
extern void native_fn_0207c1b8(void);
extern void native_fn_0207c73c(void);
extern void native_fn_021fba1c(void);


asm u32 native_ov000_021fbad8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r10, r0
    str r1, [sp, #0xc]
    bl native_fn_02062aa0
    mov r6, r0
    bl native_fn_02062ad0
    add r11, r6, r0
    mov r5, #0
ov000_021fbad8_L24:
    cmp r5, r6
    bge ov000_021fbad8_L3c
    mov r0, r5
    bl native_fn_02062a50
    mov r4, r0
    b ov000_021fbad8_L60
ov000_021fbad8_L3c:
    cmp r5, r11
    bge ov000_021fbad8_L54
    sub r0, r5, r6
    bl native_fn_02062a88
    mov r4, r0
    b ov000_021fbad8_L60
ov000_021fbad8_L54:
    mov r0, #0
    strb r0, [r10]
    b ov000_021fbad8_L1ac
ov000_021fbad8_L60:
    and r0, r5, #255
    bl native_fn_02215d94
    mov r9, r0
    ldrb r0, [r4, #0x33]
    mov r1, r9
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
    strb r0, [r10]
    add r0, r4, #32
    bl native_fn_0207c2b8
    str r0, [r10, #0x8]
    add r0, r4, #32
    mov r1, r9
    bl native_fn_0207c18c
    str r0, [r10, #0x4]
    add r0, r4, #32
    mov r1, r9
    bl native_fn_0207c3d8
    str r0, [r10, #0x10]
    add r0, r4, #32
    mov r1, r9
    bl native_fn_0207c1b8
    str r0, [r10, #0xc]
    ldr r0, [sp, #0xc]
    cmp r0, #0
    bne ov000_021fbad8_L1ac
    add r0, r4, #32
    mov r1, r9
    bl native_fn_0207c73c
    ldrsh r7, [r4, #24]
    mov r4, r0
    ldr r8, [r10, #0xc]
    add r0, r10, #20
    stmia sp, {r4, r9}
    str r8, [sp, #0x8]
    mov r1, r5
    mov r2, #47
    mov r3, r7
    bl native_fn_021fba1c
    stmia sp, {r4, r9}
    str r8, [sp, #0x8]
    add r0, r10, #24
    mov r1, r5
    mov r2, #48
    mov r3, r7
    bl native_fn_021fba1c
    stmia sp, {r4, r9}
    str r8, [sp, #0x8]
    add r0, r10, #28
    mov r1, r5
    mov r2, #49
    mov r3, r7
    bl native_fn_021fba1c
    stmia sp, {r4, r9}
    str r8, [sp, #0x8]
    add r0, r10, #32
    mov r1, r5
    mov r2, #50
    mov r3, r7
    bl native_fn_021fba1c
    stmia sp, {r4, r9}
    str r8, [sp, #0x8]
    add r0, r10, #36
    mov r1, r5
    mov r2, #51
    mov r3, r7
    bl native_fn_021fba1c
    stmia sp, {r4, r9}
    str r8, [sp, #0x8]
    add r0, r10, #40
    mov r1, r5
    mov r2, #54
    mov r3, r7
    bl native_fn_021fba1c
    stmia sp, {r4, r9}
    mov r3, r7
    add r0, r10, #44
    mov r1, r5
    mov r2, #55
    str r8, [sp, #0x8]
    bl native_fn_021fba1c
    str r9, [r10, #0x30]
ov000_021fbad8_L1ac:
    add r10, r10, #52
    add r5, r5, #1
    cmp r5, #6
    blt ov000_021fbad8_L24
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
