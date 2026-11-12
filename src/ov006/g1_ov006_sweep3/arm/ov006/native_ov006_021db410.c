/* ov006 row 0x021db410: 376 bytes.
 *
 * What it does: 92 instructions; 16 call(s) to 0x02067bc4, 0x021d7e34, 0x021db50c, +13 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x170 -> constant 0x0220f33c (image word 0x0220f33c)
 *   pool +0x174 -> constant 0x021c9698 (image word 0x021c9698)
 *   branch +0x48 -> +0xfc
 *   branch +0xf8 -> +0x154
 *   back edge +0x164 -> +0x44
 *   test +0x44 cmp r9, #0
 *   test +0x160 cmp r7, #10
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021db410; the literal pool and
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

extern void native_fn_02067bc4(void);
extern void native_fn_021d7e34(void);
extern void native_fn_02048094(void);
extern void native_fn_021d79e4(void);
extern void native_fn_020643fc(void);
extern void native_fn_021d7ebc(void);
extern void native_fn_02046af4(void);
extern void native_fn_021d7ad0(void);
extern void native_fn_021d8414(void);


asm u32 native_ov006_021db410 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #72
    ldr r0, =0x0220f33c
    ldr r0, [r0, #0xc]
    bl native_fn_02067bc4
    mov r8, r0
    ldr r1, =0x0220f33c
    ldr r2, [r8]
    ldr r0, [r1]
    sub r9, r2, r0
    bl native_fn_021d7e34
    ldr r4, =0x0220f33c
    mov r7, #0
    mov r10, #3
    add r5, r8, #12
    add r6, sp, #8
    mov r11, #255
ov006_021db410_L44:
    cmp r9, #0
    ble ov006_021db410_Lfc
    mov r0, r9
    mov r1, #0
    bl native_fn_02048094
    add r0, r7, #2
    and r0, r0, #255
    mov r1, #15
    mov r2, #2
    mov r3, #121
    bl native_fn_021d79e4
    ldr r0, [r4]
    add r0, r7, r0
    add r0, r8, r0, lsl #5
    ldr r0, [r0, #0x4]
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    bl native_fn_020643fc
    mov r1, #11
    mov r2, r10
    bl native_fn_021d7ebc
    stmia sp, {r6, r11}
    ldr r1, [r4]
    ldr r0, =0x021c9698
    add r1, r7, r1
    mov r2, #31
    add r1, r5, r1, lsl #5
    mov r3, #0
    bl native_fn_02046af4
    add r0, r7, #12
    and r0, r0, #255
    mov r1, r6
    bl native_fn_021d7ad0
    ldr r0, [r4]
    mov r1, r6
    add r0, r7, r0
    add r0, r8, r0, lsl #5
    ldr r0, [r0, #0x8]
    mov r2, #16
    mov r3, #4
    bl native_fn_021d8414
    add r0, r7, #22
    and r0, r0, #255
    mov r1, r6
    bl native_fn_021d7ad0
    b ov006_021db410_L154
ov006_021db410_Lfc:
    mov r0, #0
    mov r1, #11
    mov r2, r10
    bl native_fn_021d7ebc
    add r0, r7, #2
    and r0, r0, #255
    mov r1, #15
    mov r2, #0
    mov r3, #1
    bl native_fn_021d79e4
    add r0, r7, #12
    and r0, r0, #255
    mov r1, #15
    mov r2, #0
    mov r3, #1
    bl native_fn_021d79e4
    add r0, r7, #22
    and r0, r0, #255
    mov r1, #15
    mov r2, #0
    mov r3, #1
    bl native_fn_021d79e4
ov006_021db410_L154:
    sub r9, r9, #1
    add r10, r10, #2
    add r7, r7, #1
    cmp r7, #10
    blt ov006_021db410_L44
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
