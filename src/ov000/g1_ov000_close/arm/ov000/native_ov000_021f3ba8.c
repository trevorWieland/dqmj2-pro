/* ov000 row 0x021f3ba8: 136 bytes.
 *
 * What it does: 32 instructions; 4 call(s) to 0x021dffb4, 0x020430b4, 0x021f3bfc, +1 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x80 -> constant 0x0000ffff (image word 0x0000ffff)
 *   pool +0x84 -> constant 0x0000019a (image word 0x0000019a)
 *   branch +0x18 -> +0x78
 *   branch +0x30 -> +0x54
 *   branch +0x38 -> +0x54
 *   test +0x14 cmp r0, #0
 *   test +0x2c cmp r1, r0
 *   test +0x34 cmp r1, #0
 *   2 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f3ba8; the literal pool and
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

extern void native_fn_021dffb4(void);
extern void native_fn_020430b4(void);
extern void native_fn_0220a30c(void);


asm u32 native_ov000_021f3ba8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r2, #0
    mov r5, r0
    mov r4, r1
    bl native_fn_021dffb4
    cmp r0, #0
    beq ov000_021f3ba8_L78
    mov r0, r4
    bl native_fn_020430b4
    ldrh r1, [r0]
    ldr r0, =0x0000ffff
    cmp r1, r0
    beq ov000_021f3ba8_L54
    cmp r1, #0
    ble ov000_021f3ba8_L54
    ldr r2, =0x0000019a
    mov r0, r5
    str r2, [r5, #0x7c]
    str r2, [r5, #0x80]
    str r2, [r5, #0x84]
    bl native_fn_0220a30c
ov000_021f3ba8_L54:
    add r0, r5, #112
    add r3, r5, #272
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #1
    strb r0, [r5, #0x15c]
    mov r1, #0
    strb r1, [r5, #0x274]
    ldmia sp!, {r3, r4, r5, pc}
ov000_021f3ba8_L78:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
