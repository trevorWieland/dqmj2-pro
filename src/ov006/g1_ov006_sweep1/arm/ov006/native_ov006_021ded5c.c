/* ov006 row 0x021ded5c: 268 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x100 -> native_data4_0220f594 (image word 0x0220f594)
 *   pool +0x104 -> constant 0x0220f72c (image word 0x0220f72c)
 *   pool +0x108 -> constant 0x04001010 (image word 0x04001010)
 *   branch +0x30 -> +0x38
 *   branch +0x48 -> +0x80
 *   branch +0x7c -> +0xb4
 *   test +0x2c cmp r3, #1
 *   test +0x40 cmp r0, #0
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ded5c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data4_0220f594[];
extern void native_fn_021dee68(void);
extern void native_fn_021ddf18(void);
extern void native_fn_02049af0(void);
extern void native_fn_021def04(void);
extern void native_fn_021df4b0(void);
extern void native_fn_020414c8(void);


asm u32 native_ov006_021ded5c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #16
    ldr r3, =native_data4_0220f594
    add lr, sp, #12
    ldr r3, [r3, #0x8]
    mov r12, #0
    mov r6, r0
    mov r5, r1
    mov r4, r2
    strh r12, [lr]
    strh r12, [lr, #2]
    cmp r3, #1
    bne ov006_021ded5c_L38
    bl native_fn_021dee68
ov006_021ded5c_L38:
    ldr r0, =native_data4_0220f594
    ldr r0, [r0, #0x40]
    cmp r0, #0
    mov r0, #0
    bne ov006_021ded5c_L80
    bl native_fn_021ddf18
    mov r3, #1
    mov r12, r0
    str r3, [sp]
    mov r2, r4
    mov r0, r6
    mov r1, r5
    str r3, [sp, #0x4]
    sub r4, r3, #2
    mov r3, r12, asr #5
    str r4, [sp, #0x8]
    bl native_fn_02049af0
    b ov006_021ded5c_Lb4
ov006_021ded5c_L80:
    bl native_fn_021ddf18
    mov r12, r0
    mov r0, #0
    str r0, [sp]
    mov r3, #1
    mov r2, r4
    mov r0, r6
    mov r1, r5
    str r3, [sp, #0x4]
    sub r4, r3, #2
    mov r3, r12, asr #5
    str r4, [sp, #0x8]
    bl native_fn_02049af0
ov006_021ded5c_Lb4:
    ldr r0, =0x0220f72c
    mov r1, #0
    strb r1, [r0, #0x8]
    bl native_fn_021def04
    mov r0, #0
    bl native_fn_021df4b0
    ldr r1, =native_data4_0220f594
    mov r2, #1
    mov r0, #46
    str r2, [r1, #0x40]
    bl native_fn_020414c8
    ldr r1, =0x04001010
    mov r2, #0
    ldr r0, =native_data4_0220f594
    str r2, [r1]
    mov r1, #1
    str r1, [r0, #0x8]
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, pc}
}
