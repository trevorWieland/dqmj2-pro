/* ov001 row 0x021d8eb4: 84 bytes.
 *
 * What it does: 20 instructions; no calls; no back edge; returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: straight-line scalar (20 instructions, 0 calls, 0 branches, 0 back edges, 1 literal slot).
 *
 *   pool +0x50 -> constant 0x02233500 (image word 0x02233500)
 *   test +0x04 cmp r0, #0
 *   test +0x08 cmpgt r1, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d8eb4; the literal pool and
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



asm u32 native_ov001_021d8eb4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    cmp r0, #0
    cmpgt r1, #0
    movle r0, #0
    ldmleia sp!, {r3, pc}
    sub r1, r1, #1
    mov lr, r1, lsl #1
    mov r2, lr, asr #2
    ldr r3, =0x02233500
    sub r12, r0, #1
    mov r1, lr, lsr #31
    rsb r0, r1, lr, lsl #29
    add r1, r1, r0, ror #29
    add r2, lr, r2, lsr #29
    add r3, r3, r12, lsl #4
    ldrb r2, [r3, r2, asr #3]
    mov r0, #3
    and r0, r2, r0, lsl r1
    mov r0, r0, asr r1
    ldmia sp!, {r3, pc}
}
