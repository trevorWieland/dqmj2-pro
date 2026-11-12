/* ov000 row 0x0221cc4c: 384 bytes.
 *
 * What it does: 94 instructions; 5 call(s) to 0x02068de0, 0x02068de0, 0x02068de0, +2 more; loops (back edge at +0x3c); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x178 -> constant 0x022461c4 (image word 0x022461c4)
 *   pool +0x17c -> constant 0x022461d4 (image word 0x022461d4)
 *   0 block transfer(s), 29 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221cc4c; the literal pool and
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

extern void native_fn_02068de0(void);
extern void native_fn_02068fcc(void);
extern void native_fn_02068f70(void);


asm u32 native_ov000_0221cc4c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #32
    mov r2, #1
    str r2, [sp]
    mov r1, #4
    str r1, [sp, #0x4]
    ldr r1, =0x022461c4
    str r2, [sp, #0x8]
    ldr r1, [r1, #0x8]
    mov r4, r0
    str r1, [sp, #0xc]
    ldrsb r2, [r4, #16]
    mov r0, #10
    mov r1, #0
    mov r3, #127
    bl native_fn_02068de0
    ldr r0, =0x022461c4
    ldr r1, =0x022461d4
    ldr r12, [r0, #0xc]
    mov r2, #10
    add r3, r12, #1
    str r3, [r0, #0xc]
    strb r2, [r1, r12]
    mov r1, #9
    str r1, [sp]
    mov r1, #4
    str r1, [sp, #0x4]
    mov r1, #1
    str r1, [sp, #0x8]
    ldr r2, [r0, #0x8]
    mov r0, #11
    str r2, [sp, #0xc]
    ldrsb r2, [r4, #16]
    mov r3, #127
    bl native_fn_02068de0
    ldr r0, =0x022461c4
    ldr r1, =0x022461d4
    ldr r3, [r0, #0xc]
    mov r2, #11
    strb r2, [r1, r3]
    add r1, r3, #1
    str r1, [r0, #0xc]
    mov r1, #17
    str r1, [sp]
    mov r1, #4
    str r1, [sp, #0x4]
    mov r1, #2
    str r1, [sp, #0x8]
    ldr r2, [r0, #0x8]
    mov r0, #12
    str r2, [sp, #0xc]
    ldrsb r2, [r4, #16]
    mov r3, #127
    bl native_fn_02068de0
    ldr r0, =0x022461c4
    mov r2, #12
    ldr r12, [r0, #0xc]
    ldr r1, =0x022461d4
    add r3, r12, #1
    strb r2, [r1, r12]
    str r3, [r0, #0xc]
    bl native_fn_02068fcc
    mov r0, #12
    str r0, [sp]
    mov r0, #21
    str r0, [sp, #0x4]
    ldr r0, =0x022461c4
    mov r2, #9
    ldr r0, [r0, #0x8]
    mov r1, #0
    str r0, [sp, #0x8]
    str r2, [sp, #0xc]
    str r1, [sp, #0x10]
    mov r0, #20
    str r0, [sp, #0x14]
    mov r0, #24
    str r0, [sp, #0x18]
    mov r3, #1
    str r3, [sp, #0x1c]
    ldrsb r2, [r4, #16]
    mov r0, #14
    bl native_fn_02068f70
    ldr r1, =0x022461c4
    ldr r2, =0x022461d4
    ldr r4, [r1, #0x8]
    mov r3, #14
    add r0, r4, r0
    str r0, [r1, #0x8]
    ldr r4, [r1, #0xc]
    add r0, r4, #1
    str r0, [r1, #0xc]
    strb r3, [r2, r4]
    add sp, sp, #32
    ldmia sp!, {r4, pc}
}
