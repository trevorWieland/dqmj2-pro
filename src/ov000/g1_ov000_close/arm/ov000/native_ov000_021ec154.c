/* ov000 row 0x021ec154: 316 bytes.
 *
 * What it does: 78 instructions; 6 call(s) to 0x021ebdf0, 0x021ec23c, 0x021ebdf0, +3 more; loops (back edge at +0x54); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x138 -> constant 0x02236a98 (image word 0x02236a98)
 *   branch +0x70 -> +0xe8
 *   back edge +0xe4 -> +0x78
 *   test +0x60 cmp r10, #0
 *   test +0xe0 cmp r4, r10
 *   test +0xec cmp r10, #6
 *   1 block transfer(s), 16 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ec154; the literal pool and
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

extern void native_fn_021ebdf0(void);
extern void native_fn_021ebeec(void);
extern void native_fn_021ebe8c(void);


asm u32 native_ov000_021ec154 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #24
    ldr r6, [sp, #0x44]
    mov r10, r1
    ldr r7, [sp, #0x40]
    mov r1, r10, lsl #1
    add r4, r6, #2
    str r0, [sp, #0x14]
    mov r9, r2
    add r1, r1, #2
    str r7, [sp]
    and r0, r4, #255
    str r0, [sp, #0x4]
    and r0, r1, #255
    str r0, [sp, #0x8]
    mov r0, #1
    mov r8, r3
    str r0, [sp, #0xc]
    mov r1, #0
    mov r2, #12
    str r1, [sp, #0x10]
    bl native_fn_021ebdf0
    add r1, r8, #1
    add r0, r7, #1
    cmp r10, #0
    and r8, r1, #255
    and r7, r0, #255
    mov r4, #0
    bls ov000_021ec154_Le8
    mov r11, #2
ov000_021ec154_L78:
    add r0, r7, r4, lsl #1
    and r0, r0, #255
    str r0, [sp]
    add r0, r4, #3
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    stmib sp, {r6, r11}
    mov r0, #0
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    mov r0, r5
    mov r1, #0
    mov r2, #1
    mov r3, r8
    bl native_fn_021ebdf0
    mov r1, #16
    str r1, [sp]
    mov r3, r4, lsl #1
    ldrh r3, [r9, r3]
    mov r0, r5
    mov r1, #9
    mov r2, #4
    bl native_fn_021ebeec
    add r0, r4, #1
    and r4, r0, #255
    cmp r4, r10
    blo ov000_021ec154_L78
ov000_021ec154_Le8:
    mov r0, #0
    cmp r10, #6
    movlo r2, r10
    str r0, [sp]
    mov r0, #1
    movhs r2, #6
    str r0, [sp, #0x4]
    ldr r4, [sp, #0x48]
    ldr r0, [sp, #0x14]
    mov r1, r10
    and r2, r2, #255
    mov r3, #3
    str r4, [sp, #0x8]
    bl native_fn_021ebe8c
    ldr r0, =0x02236a98
    strb r8, [r0, #0x4]
    strb r7, [r0, #0x5]
    strb r6, [r0]
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
