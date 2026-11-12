/* ov006 row 0x021f91f4: 148 bytes.
 *
 * What it does: 65 instructions; 4 call(s) to 0x0220383c, 0x022037c0, 0x021f9226, +1 more; loops (back edge at +0x76); returns through pop {r4, r5, r6, r7, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x88 -> constant 0x0221c0e0 (image word 0x0221c0e0)
 *   pool +0x8c -> constant 0x0000e01d (image word 0x0000e01d)
 *   pool +0x90 -> native_data_0220b678 (image word 0x0220b678)
 *   branch +0x34 -> +0x3a
 *   branch +0x44 -> +0x4a
 *   branch +0x48 -> +0x4a
 *   back edge +0x76 -> +0x32
 *   test +0x32 cmp r5, #0x10
 *   test +0x42 cmp r1, #0x20
 *   test +0x74 cmp r5, #0x20
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f91f4; the literal pool and
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

extern void native_fn_0220383c(void);
extern u8 native_data_0220b678[];
extern void native_fn_022037c0(void);
extern void native_fn_022038ac(void);


asm u32 native_ov006_021f91f4 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x1c
    add r0, sp, #0x14
    mov r1, #0x0
    strh r1, [r0, #0]
    strh r1, [r0, #0x2]
    strh r1, [r0, #0x4]
    strh r1, [r0, #0x6]
    mov r2, #0x20
    add r0, sp, #0x10
    strh r2, [r0, #0x6]
    mov r2, #0xe
    strh r2, [r0, #0x8]
    mov r2, #0x10
    strh r2, [r0, #0xa]
    ldr r0, =0x0221c0e0
    ldr r0, [r0, #0]
    ldr r0, [r0, #0]
    bl native_fn_0220383c
    mov r5, #0x0
    add r6, sp, #0x10
    strh r5, [r6, #0x2]
    add r4, r5, #0x0
    mov r7, #0x31
ov006_021f91f4_L32:
    cmp r5, #0x10
    bne ov006_021f91f4_L3a
    strh r7, [r6, #0x6]
    mov r4, #0x0
ov006_021f91f4_L3a:
    ldr r0, =0x0221c0e0
    ldr r0, [r0, #0]
    add r1, r0, r5
    ldrb r1, [r1, #0x8]
    cmp r1, #0x20
    bne ov006_021f91f4_L4a
    ldr r1, =0x0000e01d
    b ov006_021f91f4_L4a
ov006_021f91f4_L4a:
    strh r1, [r6, #0]
    ldr r1, =native_data_0220b678
    ldrb r1, [r1, r4]
    strh r1, [r6, #0x4]
    ldrh r1, [r6, #0xa]
    str r1, [sp]
    mov r1, #0x2
    str r1, [sp, #0x4]
    mov r1, #0x12
    lsl r1, r1, #0x6
    str r1, [sp, #0x8]
    add r1, sp, #0x10
    str r1, [sp, #0xc]
    ldrh r1, [r6, #0x4]
    ldrh r2, [r6, #0x6]
    ldrh r3, [r6, #0x8]
    ldr r0, [r0, #0]
    bl native_fn_022037c0
    add r5, r5, #0x1
    add r4, r4, #0x1
    cmp r5, #0x20
    blt ov006_021f91f4_L32
    ldr r0, =0x0221c0e0
    ldr r0, [r0, #0]
    ldr r0, [r0, #0]
    bl native_fn_022038ac
    add sp, #0x1c
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
}
