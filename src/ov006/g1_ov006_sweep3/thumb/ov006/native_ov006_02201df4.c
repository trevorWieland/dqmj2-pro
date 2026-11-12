/* ov006 row 0x02201df4: 192 bytes.
 *
 * What it does: 80 instructions; 6 call(s) to 0x02200a7c, 0x022026a8, 0x02007a9c, +3 more; loops (back edge at +0x0e); returns through pop {r4, r5, r6, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xac -> constant 0x0221c16c (image word 0x0221c16c)
 *   pool +0xb0 -> constant 0x00000648 (image word 0x00000648)
 *   pool +0xb4 -> constant 0x00000ab4 (image word 0x00000ab4)
 *   pool +0xb8 -> constant 0x0000064c (image word 0x0000064c)
 *   pool +0xbc -> constant 0x00000aa4 (image word 0x00000aa4)
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02201df4; the literal pool and
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

extern void native_fn_02200a7c(void);
extern void native_fn_022026a8(void);
extern void native_fn_02007a9c(void);
extern void native_fn_020a47cc(void);
extern void native_fn_021ff434(void);


asm u32 native_ov006_02201df4 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r4, r1, #0x0
    ldr r1, =0x0221c16c
    str r0, [r1, #0]
    mov r1, #0xb
    lsl r1, r1, #0x8
    add r0, r0, r1
    bl native_fn_02200a7c
    ldr r0, =0x0221c16c
    mov r5, #0xa9
    ldr r3, [r0, #0]
    ldr r1, =0x00000648
    mov r2, #0x0
    strh r2, [r3, r1]
    ldr r3, [r0, #0]
    add r1, r1, #0x2
    strh r2, [r3, r1]
    ldr r3, [r0, #0]
    mov r1, #0x1
    lsl r5, r5, #0x4
    strb r1, [r3, r5]
    add r3, r5, #0x1
    ldr r6, [r0, #0]
    add r5, #0xc
    strb r1, [r6, r3]
    ldr r0, [r0, #0]
    str r2, [r0, r5]
    bl native_fn_022026a8
    ldr r1, =0x0221c16c
    ldr r3, [r4, #0]
    ldr r2, [r1, #0]
    ldr r0, =0x00000ab4
    str r3, [r2, r0]
    ldr r5, [r4, #0x4]
    ldr r3, [r1, #0]
    add r2, r0, #0x4
    str r5, [r3, r2]
    add r2, r0, #0x0
    ldr r5, [r4, #0x8]
    ldr r3, [r1, #0]
    add r2, #0x8
    str r5, [r3, r2]
    add r2, r0, #0x0
    ldr r5, [r4, #0xc]
    ldr r3, [r1, #0]
    add r2, #0xc
    str r5, [r3, r2]
    add r2, r0, #0x0
    ldr r5, [r4, #0x10]
    ldr r3, [r1, #0]
    add r2, #0x10
    str r5, [r3, r2]
    add r2, r0, #0x0
    ldr r5, [r4, #0x14]
    ldr r3, [r1, #0]
    add r2, #0x14
    str r5, [r3, r2]
    add r2, r0, #0x0
    ldrb r4, [r4, #0x18]
    ldr r3, [r1, #0]
    sub r2, #0x22
    strb r4, [r3, r2]
    ldr r1, [r1, #0]
    mov r2, #0x2
    add r0, #0x18
    strb r2, [r1, r0]
    blx native_fn_02007a9c
    ldr r0, =0x0221c16c
    ldr r1, [r0, #0]
    ldr r0, =0x0000064c
    add r0, r1, r0
    bl native_fn_020a47cc
    blx native_fn_02007a9c
    bl native_fn_021ff434
    ldr r1, =0x0221c16c
    ldr r2, [r1, #0]
    ldr r1, =0x00000aa4
    str r0, [r2, r1]
    pop {r4, r5, r6, pc}
    mov r8, r8
}
