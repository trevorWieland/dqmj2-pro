/* ov000 row 0x021e61f8: 128 bytes.
 *
 * What it does: 31 instructions; 3 call(s) to 0x021e6214, 0x021e6268, 0x0203d294; loops (back edge at +0x44); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x7c -> constant 0x02232568 (image word 0x02232568)
 *   branch +0x24 -> +0x38
 *   back edge +0x44 -> +0x1c
 *   branch +0x4c -> +0x70
 *   test +0x20 cmp r3, #0
 *   test +0x2c cmp r3, r1
 *   test +0x3c cmp r12, #16
 *   test +0x48 cmp r0, #0
 *   2 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e61f8; the literal pool and
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

extern void native_fn_0203d294(void);


asm u32 native_ov000_021e61f8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #64
    mov r4, r0
    mov r0, #0
    ldr r5, =0x02232568
    mov r12, r0
    add r2, sp, #0
ov000_021e61f8_L1c:
    ldrb r3, [r5]
    cmp r3, #0
    beq ov000_021e61f8_L38
    ldrb r3, [r5, #0x1]
    cmp r3, r1
    streq r12, [r2, r0, lsl #2]
    addeq r0, r0, #1
ov000_021e61f8_L38:
    add r12, r12, #1
    cmp r12, #16
    add r5, r5, #16
    blt ov000_021e61f8_L1c
    cmp r0, #0
    ble ov000_021e61f8_L70
    bl native_fn_0203d294
    add r2, sp, #0
    ldr r1, =0x02232568
    ldr lr, [r2, r0, lsl #2]
    add r0, r1, lr, lsl #4
    add r0, r0, #4
    ldmia r0, {r0, r1, r2}
    stmia r4, {r0, r1, r2}
ov000_021e61f8_L70:
    mov r0, lr
    add sp, sp, #64
    ldmia sp!, {r3, r4, r5, pc}
}
