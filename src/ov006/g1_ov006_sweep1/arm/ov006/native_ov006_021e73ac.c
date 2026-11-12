/* ov006 row 0x021e73ac: 240 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xec -> native_data_02207e1c (image word 0x02207e1c)
 *   branch +0x20 -> +0xe0
 *   branch +0x40 -> +0xe0
 *   branch +0xac -> +0xe0
 *   branch +0xc0 -> +0xe0
 *   test +0x1c cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0xa8 cmp r0, #0
 *   test +0xbc cmp r0, #0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e73ac; the literal pool and
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

extern void native_fn_021e7608(void);
extern u8 native_data_02207e1c[];
extern void native_fn_02049ad0(void);
extern void native_fn_02049be4(void);
extern void native_fn_021e7a88(void);


asm u32 native_ov006_021e73ac (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #28
    mov r8, r0
    mov r7, r1
    mov r6, r2
    mov r5, r3
    bl native_fn_021e7608
    cmp r0, #0
    beq ov006_021e73ac_Le0
    mov r0, r8, lsl #24
    ldr r2, =native_data_02207e1c
    add r1, r7, r7, lsl #1
    mov r0, r0, asr #24
    add r4, r2, r1
    bl native_fn_02049ad0
    cmp r0, #0
    beq ov006_021e73ac_Le0
    and lr, r6, #255
    ldr r12, [sp, #0x38]
    ldr r3, [sp, #0x44]
    ldr r6, [sp, #0x3c]
    mov r1, r3, asr #4
    ldr r2, [sp, #0x40]
    add r1, r3, r1, lsr #27
    mov r2, r2, lsl #24
    str lr, [sp]
    and r3, r5, #255
    str r3, [sp, #0x4]
    and r3, r12, #255
    str r3, [sp, #0x8]
    and r3, r6, #255
    str r3, [sp, #0xc]
    mov r1, r1, asr #5
    str r1, [sp, #0x10]
    mov r1, r2, asr #24
    str r1, [sp, #0x14]
    mov r1, #1
    str r1, [sp, #0x18]
    ldrb r1, [r4, #0x1]
    ldrsb r3, [r4]
    mov r2, #0
    bl native_fn_02049be4
    cmp r0, #0
    beq ov006_021e73ac_Le0
    mov r0, r8
    mov r1, r7
    bl native_fn_021e7a88
    cmp r0, #0
    beq ov006_021e73ac_Le0
    ldr r1, [sp, #0x38]
    ldr r0, [sp, #0x3c]
    ldr r2, [sp, #0x44]
    mul r0, r1, r0
    add sp, sp, #28
    add r0, r2, r0, lsl #5
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
ov006_021e73ac_Le0:
    mov r0, #0
    add sp, sp, #28
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
