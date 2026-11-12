/* ov000 row 0x022166dc: 204 bytes.
 *
 * What it does: 50 instructions; 3 call(s) to 0x02216260, 0x02216260, 0x02216260; loops (back edge at +0x48); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xc8 -> constant 0x0224536c (image word 0x0224536c)
 *   2 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022166dc; the literal pool and
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

extern void native_fn_02216260(void);


asm u32 native_ov000_022166dc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #20
    mov r6, r1
    mov r5, r2
    str r6, [sp]
    mov r7, r0
    mov r4, r3
    str r5, [sp, #0x4]
    str r4, [sp, #0x8]
    mov r0, #1
    str r0, [sp, #0xc]
    mov r0, #0
    str r0, [sp, #0x10]
    ldr r1, =0x0224536c
    ldrsb r0, [sp, #52]
    ldrsb r1, [r1, #16]
    ldrsb r2, [sp, #64]
    mov r3, r7
    bl native_fn_02216260
    ldrb r1, [sp, #0x28]
    str r6, [sp]
    ldrsb r0, [sp, #44]
    stmib sp, {r1, r4}
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    ldr r1, =0x0224536c
    ldrsb r0, [sp, #56]
    ldrsb r1, [r1, #16]
    mov r2, #127
    mov r3, r7
    bl native_fn_02216260
    ldrb r2, [sp, #0x28]
    str r6, [sp]
    ldrsb r1, [sp, #48]
    add r3, r7, r2
    sub r2, r5, r2
    and r2, r2, #255
    stmib sp, {r2, r4}
    str r1, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    ldr r1, =0x0224536c
    ldrsb r0, [sp, #60]
    ldrsb r1, [r1, #16]
    and r3, r3, #255
    mov r2, #127
    bl native_fn_02216260
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, pc}
}
