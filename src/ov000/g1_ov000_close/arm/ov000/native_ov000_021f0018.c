/* ov000 row 0x021f0018: 324 bytes.
 *
 * What it does: 80 instructions; 6 call(s) to 0x021ef688, 0x021f0110, 0x021ef688, +3 more; loops (back edge at +0x58); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x140 -> constant 0x02236c1c (image word 0x02236c1c)
 *   branch +0x70 -> +0xf8
 *   branch +0xbc -> +0xe8
 *   back edge +0xf4 -> +0x78
 *   test +0x64 cmp r10, #0
 *   test +0xb8 cmp r9, #0
 *   test +0xf0 cmp r4, r10
 *   test +0xf8 cmp r10, #6
 *   1 block transfer(s), 16 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f0018; the literal pool and
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
extern void native_fn_021ef77c(void);
extern void native_fn_021ef748(void);


asm u32 native_ov000_021f0018 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #24
    ldr r6, [sp, #0x44]
    mov r10, r1
    ldr r7, [sp, #0x40]
    mov r1, r10, lsl #1
    add r4, r6, #2
    str r0, [sp, #0x14]
    and r0, r4, #255
    str r7, [sp]
    mov r9, r2
    add r1, r1, #2
    str r0, [sp, #0x4]
    and r0, r1, #255
    str r0, [sp, #0x8]
    mov r0, #1
    mov r8, r3
    str r0, [sp, #0xc]
    mov r4, #0
    mov r1, #2
    mov r2, #12
    str r4, [sp, #0x10]
    bl native_fn_021ef688
    add r1, r8, #1
    add r0, r7, #1
    cmp r10, #0
    and r8, r1, #255
    and r7, r0, #255
    bls ov000_021f0018_Lf8
    mov r11, r4
ov000_021f0018_L78:
    add r0, r4, #2
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    add r0, r7, r4, lsl #1
    and r0, r0, #255
    stmia sp, {r0, r6}
    mov r0, #2
    str r0, [sp, #0x8]
    str r11, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    mov r0, r5
    mov r1, #2
    mov r2, #1
    mov r3, r8
    bl native_fn_021ef688
    cmp r9, #0
    beq ov000_021f0018_Le8
    mov r1, #16
    str r1, [sp]
    mov r1, #0
    str r1, [sp, #0x4]
    mov r3, r4, lsl #1
    ldrh r3, [r9, r3]
    mov r0, r5
    mov r1, #9
    mov r2, #2
    bl native_fn_021ef77c
ov000_021f0018_Le8:
    add r0, r4, #1
    and r4, r0, #255
    cmp r4, r10
    blo ov000_021f0018_L78
ov000_021f0018_Lf8:
    cmp r10, #6
    movlo r3, r10
    mov r2, #0
    movhs r3, #6
    str r2, [sp]
    mov r4, #1
    and r2, r3, #255
    ldr r0, [sp, #0x14]
    mov r1, r10
    mov r3, #2
    str r4, [sp, #0x4]
    bl native_fn_021ef748
    ldr r0, =0x02236c1c
    strb r8, [r0, #0x3]
    strb r7, [r0, #0x1]
    strb r6, [r0, #0x2]
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
