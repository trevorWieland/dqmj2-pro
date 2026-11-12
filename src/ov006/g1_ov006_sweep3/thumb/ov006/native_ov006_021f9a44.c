/* ov006 row 0x021f9a44: 128 bytes.
 *
 * What it does: 55 instructions; 4 call(s) to 0x0220383c, 0x022037c0, 0x021f9a7a, +1 more; loops (back edge at +0x64); returns through pop {r4, r5, r6, r7, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x74 -> native_data_0220b688 (image word 0x0220b688)
 *   pool +0x78 -> constant 0x0221c0e4 (image word 0x0221c0e4)
 *   pool +0x7c -> native_data_0220b6c8 (image word 0x0220b6c8)
 *   back edge +0x64 -> +0x36
 *   test +0x62 cmp r4, #0xc
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f9a44; the literal pool and
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

extern u8 native_data_0220b688[];
extern void native_fn_0220383c(void);
extern u8 native_data_0220b6c8[];
extern void native_fn_022037c0(void);
extern void native_fn_022038ac(void);


asm u32 native_ov006_021f9a44 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x1c
    ldr r1, =native_data_0220b688
    add r0, sp, #0x10
    ldrh r2, [r1, #0xe]
    strh r2, [r0, #0x4]
    ldrh r2, [r1, #0x10]
    strh r2, [r0, #0x6]
    ldrh r2, [r1, #0x12]
    ldrh r1, [r1, #0x14]
    strh r2, [r0, #0x8]
    strh r1, [r0, #0xa]
    mov r1, #0xb
    strh r1, [r0, #0x8]
    mov r1, #0x10
    strh r1, [r0, #0xa]
    ldr r0, =0x0221c0e4
    mov r1, #0x0
    ldr r0, [r0, #0]
    ldr r0, [r0, #0]
    bl native_fn_0220383c
    mov r4, #0x0
    add r6, sp, #0x10
    ldr r5, =native_data_0220b6c8
    strh r4, [r6, #0x2]
    mov r7, #0x2
ov006_021f9a44_L36:
    ldr r0, =0x0221c0e4
    ldr r0, [r0, #0]
    add r1, r0, r4
    ldrb r1, [r1, #0x8]
    strh r1, [r6, #0]
    ldrb r1, [r5, #0]
    strh r1, [r6, #0x4]
    ldrh r2, [r6, #0xa]
    str r2, [sp]
    mov r2, #0x12
    str r7, [sp, #0x4]
    lsl r2, r2, #0x6
    str r2, [sp, #0x8]
    add r2, sp, #0x10
    str r2, [sp, #0xc]
    ldrh r2, [r6, #0x6]
    ldrh r3, [r6, #0x8]
    ldr r0, [r0, #0]
    bl native_fn_022037c0
    add r4, r4, #0x1
    add r5, r5, #0x1
    cmp r4, #0xc
    blt ov006_021f9a44_L36
    ldr r0, =0x0221c0e4
    ldr r0, [r0, #0]
    ldr r0, [r0, #0]
    bl native_fn_022038ac
    add sp, #0x1c
    pop {r4, r5, r6, r7, pc}
}
