/* ov000 row 0x021d7ef8: 88 bytes.
 *
 * Decoded shape: loop with no calls.
 *
 *   pool +0x50 -> native_data_022300c0 (image word 0x022300c0)
 *   pool +0x54 -> native_data_02230120 (image word 0x02230120)
 *   back edge +0x48 -> +0x1c
 *   test +0x10 cmp lr, #0
 *   test +0x24 cmp r1, #0x60
 *   test +0x44 cmp ip, lr
 *   memory +0x0c ldrb lr, [r1]
 *   memory +0x1c ldr r2, [r3, ip, lsl #3]
 *   memory +0x20 ldr r1, [r2, #0x70]
 *   memory +0x2c ldrlt r1, [r1, #4]
 *   memory +0x38 ldrge r1, [r1, #4]
 *   memory +0x40 str r1, [r2, #0x6c]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: count load and table base load ordered against the image
 * (47-byte diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d7ef8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_022300c0[];
extern u8 native_data_02230120[];


asm u32 native_ov000_021d7ef8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, =native_data_022300c0
    mov ip, #0
    ldrb lr, [r1]
    cmp lr, #0
    ldmleia sp!, {r3, pc}
    ldr r3, =native_data_02230120
ov000_021d7ef8_L1c:
    ldr r2, [r3, ip, lsl #3]
    ldr r1, [r2, #0x70]
    cmp r1, #0x60
    add r1, r3, ip, lsl #3
    ldrlt r1, [r1, #4]
    add ip, ip, #1
    sublt r1, r1, r0
    ldrge r1, [r1, #4]
    addge r1, r0, r1
    str r1, [r2, #0x6c]
    cmp ip, lr
    blt ov000_021d7ef8_L1c
    ldmia sp!, {r3, pc}
}
