/* ov000 row 0x021f2fcc: 280 bytes.
 *
 * What it does: 69 instructions; 5 call(s) to 0x021f2d24, 0x021f30a4, 0x021f2d24, +2 more; loops (back edge at +0x68); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x114 -> constant 0x02236dbc (image word 0x02236dbc)
 *   branch +0x84 -> +0xd8
 *   back edge +0xd4 -> +0x94
 *   test +0x14 cmp r0, r2
 *   test +0x74 cmp r7, #0
 *   test +0xd0 cmp r6, r7
 *   1 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f2fcc; the literal pool and
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

extern void native_fn_021f2d24(void);
extern void native_fn_021f2df4(void);


asm u32 native_ov000_021f2fcc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    str r1, [sp, #0x18]
    str r0, [sp, #0x14]
    mov r0, r1
    cmp r0, r2
    movlo r2, r0
    and r7, r2, #255
    ldr r8, [sp, #0x44]
    ldr r9, [sp, #0x40]
    add r2, r8, #2
    mov r0, r7, lsl #1
    add r1, r0, #2
    mov r10, r3
    str r9, [sp]
    and r2, r2, #255
    str r2, [sp, #0x4]
    and r1, r1, #255
    mov r0, #1
    str r1, [sp, #0x8]
    mov r1, r0
    mov r3, r10
    str r0, [sp, #0xc]
    mov r4, #0
    mov r2, #12
    str r4, [sp, #0x10]
    bl native_fn_021f2d24
    add r1, r10, #1
    add r0, r9, #1
    cmp r7, #0
    and r10, r1, #255
    and r9, r0, #255
    mov r6, r4
    bls ov000_021f2fcc_Ld8
    mov r11, r4
    mov r5, #2
    mov r4, #1
ov000_021f2fcc_L94:
    add r0, r9, r6, lsl #1
    and r0, r0, #255
    stmia sp, {r0, r8}
    add r0, r6, #3
    str r5, [sp, #0x8]
    mov r0, r0, lsl #24
    str r11, [sp, #0xc]
    mov r1, r4
    mov r2, r4
    mov r3, r10
    mov r0, r0, asr #24
    str r4, [sp, #0x10]
    bl native_fn_021f2d24
    add r0, r6, #1
    and r6, r0, #255
    cmp r6, r7
    blo ov000_021f2fcc_L94
ov000_021f2fcc_Ld8:
    ldr r1, [sp, #0x18]
    mov r3, #0
    str r3, [sp]
    mov r4, #1
    ldr r0, [sp, #0x14]
    mov r2, r7
    mov r3, #3
    str r4, [sp, #0x4]
    bl native_fn_021f2df4
    ldr r0, =0x02236dbc
    strb r10, [r0, #0x1]
    strb r9, [r0, #0x2]
    strb r8, [r0]
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
