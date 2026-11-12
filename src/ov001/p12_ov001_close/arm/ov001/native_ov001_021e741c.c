/* ov001 row 0x021e741c: 104 bytes.
 *
 * What it does: 25 instructions; 1 call(s) to 0x02044414; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (25 instructions, 1 call, 0 branches, 1 back edge, 1 literal slot).
 *
 *   pool +0x64 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   test +0x38 cmp r2, #1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e741c; the literal pool and
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

extern void native_fn_02044414(void);


asm u32 native_ov001_021e741c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, r3
    bl native_fn_02044414
    ldr r2, =0x2aaaaaab
    mov r3, #6
    smull r1, r12, r2, r0
    add r12, r12, r0, lsr #31
    smull r1, r2, r3, r12
    sub r12, r0, r1
    ldr r3, [r5, #0x1e8]
    ldrb r2, [r5, #0x31e]
    add r0, r3, r12
    ldrb r0, [r0, #0x8]
    cmp r2, #1
    moveq r2, #0
    strh r0, [r4]
    ldr r1, [sp, #0x10]
    movne r2, #1
    strb r2, [r1]
    ldr r0, [sp, #0x14]
    mov r1, #0
    strb r1, [r0]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
}
