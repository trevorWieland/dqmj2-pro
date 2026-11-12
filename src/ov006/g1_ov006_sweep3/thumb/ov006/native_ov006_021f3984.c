/* ov006 row 0x021f3984: 100 bytes.
 *
 * What it does: 41 instructions; 4 call(s) to 0x021f37f0, 0x021f399e, 0x021f39e8, +1 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x58 -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x5c -> native_data_0220b1b4 (image word 0x0220b1b4)
 *   pool +0x60 -> constant 0x0000011d (image word 0x0000011d)
 *   back edge +0x2e -> +0x1a
 *   branch +0x32 -> +0x3a
 *   branch +0x38 -> +0x42
 *   branch +0x3c -> +0x42
 *   test +0x2c cmp r4, #0x4
 *   test +0x30 cmp r6, #0x2
 *   test +0x3a cmp r6, #0x1
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f3984; the literal pool and
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

extern u8 native_data_0220b1b4[];
extern void native_fn_021f37f0(void);
extern void native_fn_021f39e8(void);


asm u32 native_ov006_021f3984 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    add r6, r0, #0x0
    mov r0, #0x0
    str r0, [sp, #0x4]
    str r0, [sp]
    ldr r0, =0x0221c05c
    ldr r7, =native_data_0220b1b4
    ldr r1, [r0, #0]
    ldr r0, =0x0000011d
    strb r6, [r1, r0]
    ldr r4, [sp, #0x4]
    add r5, r4, #0x0
ov006_021f3984_L1a:
    lsl r2, r5, #0x2
    add r2, r7, r2
    ldrh r2, [r2, #0x2]
    add r0, r6, #0x0
    add r1, r4, #0x0
    bl native_fn_021f37f0
    add r4, r4, #0x1
    add r5, #0xc
    cmp r4, #0x4
    blt ov006_021f3984_L1a
    cmp r6, #0x2
    bne ov006_021f3984_L3a
    mov r0, #0x1
    str r0, [sp, #0x4]
    b ov006_021f3984_L42
ov006_021f3984_L3a:
    cmp r6, #0x1
    bne ov006_021f3984_L42
    mov r0, #0x1
    str r0, [sp]
ov006_021f3984_L42:
    ldr r1, [sp, #0x4]
    mov r0, #0x2f
    bl native_fn_021f39e8
    ldr r1, [sp]
    mov r0, #0x30
    bl native_fn_021f39e8
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
