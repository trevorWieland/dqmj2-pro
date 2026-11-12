/* ov000 row 0x022093ec: 252 bytes.
 *
 * What it does: 61 instructions; 3 call(s) to 0x02046120, 0x02046138, 0x020270c0; loops (back edge at +0x48); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xf4 -> constant 0x02238520 (image word 0x02238520)
 *   pool +0xf8 -> constant 0x02238514 (image word 0x02238514)
 *   branch +0x1c -> +0x84
 *   branch +0x34 -> +0x40
 *   branch +0x80 -> +0xe4
 *   branch +0x98 -> +0xa4
 *   test +0x08 cmp r0, #0
 *   test +0x18 cmp r0, #0
 *   test +0x2c cmp r4, #256
 *   test +0x38 cmp r4, #0
 *   test +0x90 cmp r4, #256
 *   test +0x9c cmp r4, #0
 *   2 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022093ec; the literal pool and
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

extern void native_fn_02046120(void);
extern void native_fn_02046138(void);
extern void native_fn_020270c0(void);


asm u32 native_ov000_022093ec (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #8
    cmp r0, #0
    ldrlt r0, =0x02238520
    mov r6, r1
    ldrltsb r0, [r0, #8]
    cmp r0, #0
    bne ov000_022093ec_L84
    ldr r0, =0x02238520
    ldrh r5, [r0, #4]
    add r4, r5, r6
    cmp r4, #256
    subge r4, r4, #256
    bge ov000_022093ec_L40
    cmp r4, #0
    addlt r4, r4, #256
ov000_022093ec_L40:
    mov r0, r4, lsl #16
    mov r0, r0, lsr #16
    bl native_fn_02046120
    ldr r0, =0x02238514
    ldr r1, =0x02238520
    ldr r0, [r0, #0x4]
    strh r4, [r1, #4]
    ldr r0, [r0, #0x44]
    mov r1, #256
    stmia sp, {r1, r6}
    ldr r2, [r0, #0x14]
    mov r1, #0
    ldr r6, [r2, #0x8]
    mov r2, r1
    mov r3, r5
    blx r6
    b ov000_022093ec_Le4
ov000_022093ec_L84:
    ldr r0, =0x02238520
    ldrh r5, [r0, #6]
    add r4, r5, r6
    cmp r4, #256
    subge r4, r4, #256
    bge ov000_022093ec_La4
    cmp r4, #0
    addlt r4, r4, #256
ov000_022093ec_La4:
    mov r0, r4, lsl #16
    mov r0, r0, lsr #16
    bl native_fn_02046138
    ldr r0, =0x02238514
    ldr r1, =0x02238520
    ldr r0, [r0]
    strh r4, [r1, #6]
    ldr r0, [r0, #0x44]
    mov r1, #256
    stmia sp, {r1, r6}
    ldr r2, [r0, #0x14]
    mov r1, #0
    ldr r6, [r2, #0x8]
    mov r2, r1
    mov r3, r5
    blx r6
ov000_022093ec_Le4:
    bl native_fn_020270c0
    mov r0, r4
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, pc}
}
