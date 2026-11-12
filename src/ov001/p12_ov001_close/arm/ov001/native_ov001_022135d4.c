/* ov001 row 0x022135d4: 92 bytes.
 *
 * What it does: 22 instructions; 1 call(s) to 0x022135f0; loops (back edge at +0x3c); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (22 instructions, 1 call, 1 branch, 1 back edge, 1 literal slot).
 *
 *   pool +0x58 -> native_data_0222f180 (image word 0x0222f180)
 *   branch +0x2c -> +0x40
 *   back edge +0x3c -> +0x1c
 *   test +0x24 cmp r3, r6
 *   test +0x34 cmp r12, #7
 *   test +0x44 cmp r1, r4
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022135d4; the literal pool and
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

extern u8 native_data_0222f180[];


asm u32 native_ov001_022135d4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov lr, #0
    ldr r6, [r0, #0x30]
    ldr r5, =native_data_0222f180
    mov r4, lr
    mov r12, lr
    mov r1, #10
ov001_022135d4_L1c:
    ldrsb r2, [r5]
    mul r3, r2, r1
    cmp r3, r6
    movge r4, r12
    bge ov001_022135d4_L40
    add r12, r12, #1
    cmp r12, #7
    add r5, r5, #1
    blt ov001_022135d4_L1c
ov001_022135d4_L40:
    ldr r1, [r0, #0x38]
    cmp r1, r4
    movne lr, #1
    strne r4, [r0, #0x38]
    mov r0, lr
    ldmia sp!, {r4, r5, r6, pc}
}
