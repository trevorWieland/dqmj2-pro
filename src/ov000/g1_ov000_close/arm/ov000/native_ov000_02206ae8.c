/* ov000 row 0x02206ae8: 308 bytes.
 *
 * What it does: 77 instructions; 6 call(s) to 0x02206868, 0x02206be8, 0x02206868, +3 more; loops (back edge at +0x5c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill.
 *
 *   branch +0x68 -> +0x100
 *   branch +0xcc -> +0xf0
 *   back edge +0xfc -> +0x80
 *   test +0x60 cmp r10, #0
 *   test +0xc8 cmp r9, #0
 *   test +0xf8 cmp r4, r10
 *   test +0x100 cmp r10, #6
 *   1 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02206ae8; the literal pool and
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

extern void native_fn_02206868(void);
extern void native_fn_022069d8(void);
extern void native_fn_022069a4(void);


asm u32 native_ov000_02206ae8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    ldr r8, [sp, #0x44]
    ldrb r5, [sp, #0x40]
    mov r10, r1
    mov r1, r10, lsl #1
    add r1, r1, #2
    str r5, [sp]
    str r0, [sp, #0x18]
    add r4, r8, #2
    mov r9, r2
    and r2, r4, #255
    str r2, [sp, #0x4]
    and r1, r1, #255
    mov r0, #0
    str r1, [sp, #0x8]
    str r0, [sp, #0xc]
    ldr r7, [sp, #0x48]
    str r0, [sp, #0x10]
    mov r1, r0
    mov r2, #12
    mov r5, r3
    str r7, [sp, #0x14]
    bl native_fn_02206868
    cmp r10, #0
    mov r4, #0
    bls ov000_02206ae8_L100
    ldrb r0, [sp, #0x40]
    add r0, r0, #1
    and r6, r0, #255
    add r0, r5, #1
    and r11, r0, #255
ov000_02206ae8_L80:
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    add r0, r6, r4, lsl #1
    and r0, r0, #255
    stmia sp, {r0, r8}
    mov r0, #2
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    mov r0, r5
    mov r1, #0
    mov r2, #1
    mov r3, r11
    str r7, [sp, #0x14]
    bl native_fn_02206868
    cmp r9, #0
    beq ov000_02206ae8_Lf0
    mov r1, #16
    str r1, [sp]
    mov r3, r4, lsl #1
    ldrh r3, [r9, r3]
    mov r0, r5
    mov r1, #5
    mov r2, #2
    bl native_fn_022069d8
ov000_02206ae8_Lf0:
    add r0, r4, #1
    and r4, r0, #255
    cmp r4, r10
    blo ov000_02206ae8_L80
ov000_02206ae8_L100:
    cmp r10, #6
    movlo r4, r10
    mov r2, #0
    movhs r4, #6
    str r2, [sp]
    mov r3, #1
    ldr r0, [sp, #0x18]
    mov r1, r10
    and r2, r4, #255
    str r3, [sp, #0x4]
    bl native_fn_022069a4
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
