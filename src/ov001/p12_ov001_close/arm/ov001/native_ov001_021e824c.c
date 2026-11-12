/* ov001 row 0x021e824c: 96 bytes.
 *
 * What it does: 20 instructions; 1 call(s) to 0x021e8294; no back edge; returns through pop {r3, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: call sequence (20 instructions, 1 call, 0 branches, 0 back edges, 4 literal slots).
 *
 *   pool +0x50 -> constant 0x02238d2e (image word 0x02238d2e)
 *   pool +0x54 -> constant 0x02238d30 (image word 0x02238d30)
 *   pool +0x58 -> constant 0x02238d31 (image word 0x02238d31)
 *   pool +0x5c -> constant 0x02238d32 (image word 0x02238d32)
 *   branch +0x08 -> +0x48
 *   test +0x04 cmp r1, #0
 *   test +0x18 cmp r3, #4
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e824c; the literal pool and
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



asm u32 native_ov001_021e824c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    cmp r1, #0
    blt ov001_021e824c_L48
    mov r12, #6
    mul r14, r0, r12
    ldr r12, =0x02238d2e
    cmp r3, #4
    strh r1, [r12, lr]
    ldr r0, =0x02238d30
    ldr r12, =0x02238d31
    strb r2, [r0, lr]
    moveq r3, #0
    ldr r1, [sp, #0x8]
    ldr r0, =0x02238d32
    strb r3, [r12, lr]
    strb r1, [r0, lr]
    mov r0, #1
    ldmia sp!, {r3, pc}
ov001_021e824c_L48:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
