/* ov006 row 0x021de980: 284 bytes.
 *
 * What it does: Writes 2 blocks of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x118 -> constant 0x0220f594 (image word 0x0220f594)
 *   branch +0xa0 -> +0x104
 *   back edge +0x100 -> +0xb8
 *   test +0x9c cmp r8, #0
 *   test +0xf4 cmp r8, r0, asr #24
 *   2 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021de980; the literal pool and
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

extern void native_fn_02049794(void);
extern void native_fn_02026144(void);


asm u32 native_ov006_021de980 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #24
    ldrb r4, [sp, #0x40]
    mov r5, r1
    mov r9, r3
    mov r10, r2
    add r1, r4, #2
    add r2, r9, #2
    mov r6, r0
    and r0, r2, #255
    stmia sp, {r5, r10}
    str r0, [sp, #0x8]
    and r0, r1, #255
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    mov r4, #0
    mov r1, #4
    mov r2, #127
    mov r3, #12
    str r4, [sp, #0x14]
    bl native_fn_02049794
    ldrb r4, [sp, #0x44]
    add r2, r10, #1
    ldrb r1, [sp, #0x48]
    strh r4, [r6, #12]
    ldr r0, [sp, #0x50]
    strh r1, [r6, #14]
    mov r1, r4
    and r10, r2, #255
    bl native_fn_02026144
    mul r0, r4, r0
    str r0, [r6, #0x4]
    ldr r0, [sp, #0x50]
    mov r1, r4
    bl native_fn_02026144
    ldrb r8, [sp, #0x44]
    str r1, [r6]
    mov r7, #0
    cmp r8, #0
    ble ov006_021de980_L104
    add r0, r5, #1
    and r6, r0, #255
    mov r5, #2
    mov r4, #1
    mov r11, #127
ov006_021de980_Lb8:
    stmia sp, {r6, r10}
    str r9, [sp, #0x8]
    add r0, r7, #5
    mov r1, r0, lsl #24
    str r5, [sp, #0xc]
    str r4, [sp, #0x10]
    mov r0, r4
    mov r2, r11
    mov r3, #0
    mov r1, r1, asr #24
    str r4, [sp, #0x14]
    bl native_fn_02049794
    add r0, r7, #1
    mov r0, r0, lsl #24
    add r1, r10, #2
    cmp r8, r0, asr #24
    and r10, r1, #255
    mov r7, r0, asr #24
    bgt ov006_021de980_Lb8
ov006_021de980_L104:
    ldr r0, =0x0220f594
    mov r1, #0
    str r1, [r0, #0x2c]
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
