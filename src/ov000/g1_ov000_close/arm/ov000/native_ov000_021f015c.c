/* ov000 row 0x021f015c: 328 bytes.
 *
 * What it does: 82 instructions; 3 call(s) to 0x021ef688, 0x021ef688, 0x021ef688; loops (back edge at +0x70); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill.
 *
 *   back edge +0x13c -> +0xb8
 *   test +0x1c cmp r4, #0
 *   test +0x88 cmp r7, #0
 *   test +0x134 cmp r7, r0, asr #24
 *   1 block transfer(s), 17 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f015c; the literal pool and
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

extern void native_fn_021ef688(void);


asm u32 native_ov000_021f015c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    ldr r8, [sp, #0x40]
    mov r6, r0
    sub r0, r3, r8
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    cmp r4, #0
    mov r10, r1
    mov r9, r2
    addle sp, sp, #20
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldrb r7, [sp, #0x38]
    add r1, r3, #2
    str r9, [sp]
    mov r0, r7, lsl #1
    and r1, r1, #255
    add r0, r0, #2
    str r1, [sp, #0x4]
    and r0, r0, #255
    str r0, [sp, #0x8]
    mov r5, #0
    str r5, [sp, #0xc]
    mov r3, r10
    mov r0, #1
    mov r1, #2
    mov r2, #12
    str r5, [sp, #0x10]
    bl native_fn_021ef688
    ldrb r1, [sp, #0x38]
    add r3, r10, #1
    add r2, r9, #1
    ldrb r0, [sp, #0x3c]
    strh r1, [r6, #12]
    cmp r7, #0
    strh r0, [r6, #14]
    str r5, [r6, #0x4]
    and r10, r3, #255
    and r9, r2, #255
    addle sp, sp, #20
    str r5, [r6]
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r0, r10, r8
    and r6, r4, #255
    and r4, r0, #255
    mov r11, #2
ov000_021f015c_Lb8:
    str r9, [sp]
    stmib sp, {r8, r11}
    mov r0, #0
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    add r0, r5, #2
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r11
    mov r2, #5
    mov r3, r10
    bl native_fn_021ef688
    str r9, [sp]
    str r6, [sp, #0x4]
    mov r0, #2
    str r0, [sp, #0x8]
    mov r0, #1
    str r0, [sp, #0xc]
    str r0, [sp, #0x10]
    add r0, r5, #8
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, #2
    mov r2, #6
    mov r3, r4
    bl native_fn_021ef688
    add r0, r9, #2
    and r9, r0, #255
    add r0, r5, #1
    mov r0, r0, lsl #24
    cmp r7, r0, asr #24
    mov r5, r0, asr #24
    bgt ov000_021f015c_Lb8
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
