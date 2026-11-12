/* ov000 row 0x021fba1c: 188 bytes.
 *
 * What it does: 46 instructions; 6 call(s) to 0x02008d78, 0x02215cb4, 0x0207afec, +3 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb8 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x34 -> +0xac
 *   branch +0x6c -> +0x7c
 *   branch +0x78 -> +0x88
 *   test +0x30 cmp r0, #0
 *   test +0x68 cmp r5, #0
 *   test +0x70 cmp r0, r5
 *   test +0x80 cmp r0, r1
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fba1c; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_02215cb4(void);
extern void native_fn_0207afec(void);
extern void native_fn_0207baa0(void);
extern void native_fn_0207b244(void);


asm u32 native_ov000_021fba1c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #8
    mov r5, r1
    mov r7, r2
    mov r1, #0
    mov r2, #4
    mov r4, r0
    mov r6, r3
    bl native_fn_02008d78
    mov r1, r7
    and r0, r5, #255
    bl native_fn_02215cb4
    cmp r0, #0
    beq ov000_021fba1c_Lac
    mov r0, r7
    bl native_fn_0207afec
    ldrsh r5, [r0, #28]
    mov r12, #0
    ldr r2, [sp, #0x20]
    ldr r3, [sp, #0x24]
    mov r0, r7
    mov r1, r6
    str r12, [sp]
    mov r12, #1
    str r12, [sp, #0x4]
    bl native_fn_0207baa0
    cmp r5, #0
    ble ov000_021fba1c_L7c
    cmp r0, r5
    movge r0, r5
    b ov000_021fba1c_L88
ov000_021fba1c_L7c:
    ldr r1, =0x0000270f
    cmp r0, r1
    movge r0, r1
ov000_021fba1c_L88:
    ldr r1, [sp, #0x28]
    strh r0, [r4]
    ldr r2, [sp, #0x24]
    mov r0, r7
    bl native_fn_0207b244
    strh r0, [r4, #2]
    add sp, sp, #8
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov000_021fba1c_Lac:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
