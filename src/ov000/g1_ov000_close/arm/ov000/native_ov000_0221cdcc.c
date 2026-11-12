/* ov000 row 0x0221cdcc: 328 bytes.
 *
 * What it does: 81 instructions; 8 call(s) to 0x0221c658, 0x0221c758, 0x0221cec8, +5 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x144 -> constant 0x022461c4 (image word 0x022461c4)
 *   branch +0x80 -> +0xfc
 *   back edge +0xf8 -> +0x88
 *   test +0x74 cmp r10, #0
 *   test +0xf4 cmp r4, r10
 *   test +0xfc cmp r10, #6
 *   1 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221cdcc; the literal pool and
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

extern void native_fn_0221c658(void);
extern void native_fn_0221c758(void);
extern void native_fn_0221c938(void);
extern void native_fn_0221c8dc(void);


asm u32 native_ov000_0221cdcc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #24
    ldr r6, [sp, #0x44]
    ldr r7, [sp, #0x40]
    mov r10, r1
    str r0, [sp, #0x14]
    mov r9, r2
    mov r8, r3
    bl native_fn_0221c658
    add r1, r6, #2
    str r7, [sp]
    and r1, r1, #255
    str r1, [sp, #0x4]
    mov r1, r10, lsl #1
    add r1, r1, #2
    and r1, r1, #255
    str r1, [sp, #0x8]
    mov r1, #1
    str r1, [sp, #0xc]
    mov r1, #0
    str r1, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, #9
    mov r2, #12
    mov r3, r8
    bl native_fn_0221c758
    add r0, r8, #1
    and r8, r0, #255
    add r0, r7, #1
    cmp r10, #0
    and r7, r0, #255
    mov r4, #0
    bls ov000_0221cdcc_Lfc
    mov r11, #1
ov000_0221cdcc_L88:
    add r5, r4, #26
    bl native_fn_0221c658
    add r1, r7, r4, lsl #1
    and r1, r1, #255
    stmia sp, {r1, r6}
    mov r1, #2
    str r1, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    str r11, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, r5, lsl #24
    mov r0, r0, asr #24
    mov r2, r11
    mov r3, r8
    bl native_fn_0221c758
    mov r1, #16
    str r1, [sp]
    mov r3, r4, lsl #1
    mov r0, r5, lsl #24
    ldrh r3, [r9, r3]
    mov r0, r0, asr #24
    mov r1, #9
    mov r2, #0
    bl native_fn_0221c938
    add r0, r4, #1
    and r4, r0, #255
    cmp r4, r10
    blo ov000_0221cdcc_L88
ov000_0221cdcc_Lfc:
    cmp r10, #6
    movlo r3, r10
    mov r2, #0
    movhs r3, #6
    str r2, [sp]
    mov r4, #1
    and r2, r3, #255
    ldr r0, [sp, #0x14]
    mov r1, r10
    mov r3, #26
    str r4, [sp, #0x4]
    bl native_fn_0221c8dc
    ldr r0, =0x022461c4
    strb r8, [r0, #0x5]
    strb r7, [r0, #0x1]
    strb r6, [r0]
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
