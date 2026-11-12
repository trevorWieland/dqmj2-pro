/* ov001 row 0x02204d60: 144 bytes.
 *
 * What it does: 36 instructions; 1 call(s) to 0x02204d74; loops (back edge at +0x84); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 1 call (36 instructions, 1 call, 1 branch, 1 back edge, 0 literal slots).
 *
 *   branch +0x1c -> +0x70
 *   back edge +0x84 -> +0x14
 *   test +0x18 cmp r4, lr
 *   test +0x34 cmp r1, #0
 *   test +0x7c cmp r12, #20
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204d60; the literal pool and
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



asm u32 native_ov001_02204d60 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r5, [r0, #0x40]
    mov r12, #0
    mov r6, r5
    mvn lr, #0
ov001_02204d60_L14:
    ldrsb r4, [r6]
    cmp r4, lr
    bne ov001_02204d60_L70
    mov lr, #12
    mul r4, r12, r14
    strb r1, [r5, r4]
    ldr r1, [r0, #0x38]
    add lr, r5, r4
    cmp r1, #0
    movne r2, #0
    strb r2, [lr, #0x1]
    ldrsh r1, [sp, #16]
    strb r3, [lr, #0x2]
    ldrsh r2, [sp, #20]
    strh r1, [lr, #8]
    ldrb r1, [sp, #0x18]
    strh r2, [lr, #10]
    strb r1, [lr, #0x3]
    ldrsb r1, [r0, #36]
    add r1, r1, #1
    strb r1, [r0, #0x24]
    mov r0, r12
    ldmia sp!, {r4, r5, r6, pc}
ov001_02204d60_L70:
    add r12, r12, #1
    mov r12, r12, lsl #24
    mov r12, r12, asr #24
    cmp r12, #20
    add r6, r6, #12
    blt ov001_02204d60_L14
    mvn r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
