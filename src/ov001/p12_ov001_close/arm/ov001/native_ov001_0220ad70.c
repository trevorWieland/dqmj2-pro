/* ov001 row 0x0220ad70: 400 bytes.
 *
 * What it does: 98 instructions; 4 call(s) to 0x02068de0, 0x02068de0, 0x02068de0, +1 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill (98 instructions, 4 calls, 0 branches, 4 back edges, 2 literal slots).
 *
 *   pool +0x188 -> constant 0x0223df3c (image word 0x0223df3c)
 *   pool +0x18c -> constant 0x0223df44 (image word 0x0223df44)
 *   1 block transfer(s), 30 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220ad70; the literal pool and
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
extern void native_fn_02068f70(void);


asm u32 native_ov001_0220ad70 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #32
    mov r2, #1
    str r2, [sp]
    mov r1, #4
    str r1, [sp, #0x4]
    ldr r1, =0x0223df3c
    str r2, [sp, #0x8]
    ldr r1, [r1, #0x4]
    mov r4, r0
    str r1, [sp, #0xc]
    ldrsb r2, [r4, #16]
    mov r0, #2
    mov r1, #0
    mov r3, #127
    bl native_fn_02068de0
    ldr r2, =0x0223df3c
    ldr r3, =0x0223df44
    ldr r1, [r2, #0x4]
    mov r5, #2
    add r0, r1, r0
    str r0, [r2, #0x4]
    ldrsb lr, [r2]
    mov r1, #9
    mov r0, #4
    add r12, lr, #1
    strb r12, [r2]
    strb r5, [r3, lr]
    str r1, [sp]
    str r0, [sp, #0x4]
    mov r1, #1
    str r1, [sp, #0x8]
    ldr r2, [r2, #0x4]
    mov r0, #3
    str r2, [sp, #0xc]
    ldrsb r2, [r4, #16]
    mov r3, #127
    bl native_fn_02068de0
    ldr r2, =0x0223df3c
    ldr r3, =0x0223df44
    ldr r1, [r2, #0x4]
    mov r5, #3
    add r0, r1, r0
    str r0, [r2, #0x4]
    ldrsb lr, [r2]
    mov r1, #17
    mov r0, #4
    add r12, lr, #1
    strb r12, [r2]
    strb r5, [r3, lr]
    str r1, [sp]
    str r0, [sp, #0x4]
    mov r1, #2
    str r1, [sp, #0x8]
    ldr r2, [r2, #0x4]
    mov r3, #127
    str r2, [sp, #0xc]
    ldrsb r2, [r4, #16]
    bl native_fn_02068de0
    ldr r1, =0x0223df3c
    ldr r3, =0x0223df44
    ldr r2, [r1, #0x4]
    mov r12, #4
    add r0, r2, r0
    str r0, [r1, #0x4]
    ldrsb r5, [r1]
    mov r0, #12
    mov r2, #21
    add lr, r5, #1
    strb lr, [r1]
    strb r12, [r3, r5]
    stmia sp, {r0, r2}
    ldr r2, [r1, #0x4]
    mov r1, #5
    str r2, [sp, #0x8]
    str r1, [sp, #0xc]
    str r12, [sp, #0x10]
    mov r1, #2
    str r1, [sp, #0x14]
    mov r1, #24
    str r1, [sp, #0x18]
    mov r3, #1
    str r3, [sp, #0x1c]
    ldrsb r2, [r4, #16]
    mov r1, #0
    bl native_fn_02068f70
    ldr r1, =0x0223df3c
    ldr r2, =0x0223df44
    ldr r4, [r1, #0x4]
    mov r3, #12
    add r0, r4, r0
    str r0, [r1, #0x4]
    ldrsb r4, [r1]
    add r0, r4, #1
    strb r0, [r1]
    strb r3, [r2, r4]
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, pc}
}
