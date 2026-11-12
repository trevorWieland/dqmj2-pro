/* ov006 row 0x021fc8b8: 176 bytes.
 *
 * What it does: 57 instructions; 7 call(s) to 0x021f27d4, 0x021f27d4, 0x021f27d4, +4 more; loops (back edge at +0x14); returns through pop {r3, pc}; 12 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x80 -> native_data_0220b814 (image word 0x0220b814)
 *   pool +0x84 -> native_data_0220e000 (image word 0x0220e000)
 *   pool +0x88 -> constant 0x0200494c (image word 0x0200494c)
 *   pool +0x8c -> native_data_0220e014 (image word 0x0220e014)
 *   pool +0x90 -> constant 0x02004fd8 (image word 0x02004fd8)
 *   pool +0x94 -> native_data_0220e02c (image word 0x0220e02c)
 *   pool +0x98 -> constant 0x020048a0 (image word 0x020048a0)
 *   pool +0x9c -> native_data_0220e044 (image word 0x0220e044)
 *   pool +0xa0 -> constant 0x02004cd8 (image word 0x02004cd8)
 *   pool +0xa4 -> constant 0x0221c10c (image word 0x0221c10c)
 *   pool +0xa8 -> constant 0x04001008 (image word 0x04001008)
 *   pool +0xac -> constant 0x0400000a (image word 0x0400000a)
 *   back edge +0x14 -> +0x0a
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fc8b8; the literal pool and
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

extern u8 native_data_0220b814[];
extern u8 native_data_0220e000[];
extern void native_fn_021f27d4(void);
extern u8 native_data_0220e014[];
extern u8 native_data_0220e02c[];
extern u8 native_data_0220e044[];
extern void native_fn_021f2798(void);
extern void native_fn_02202a80(void);
extern void native_fn_02203908(void);


asm u32 native_ov006_021fc8b8 (register u32 a0)
{
    push {r3, lr}
    sub sp, #0x18
    ldr r3, =native_data_0220b814
    add r2, sp, #0x0
    mov r1, #0x16
ov006_021fc8b8_La:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021fc8b8_La
    ldr r0, =native_data_0220e000
    ldr r1, =0x0200494c
    bl native_fn_021f27d4
    ldr r0, =native_data_0220e014
    ldr r1, =0x02004fd8
    bl native_fn_021f27d4
    ldr r0, =native_data_0220e02c
    ldr r1, =0x020048a0
    bl native_fn_021f27d4
    ldr r0, =native_data_0220e044
    ldr r1, =0x02004cd8
    bl native_fn_021f27d4
    add r0, sp, #0x0
    bl native_fn_021f2798
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c10c
    ldr r1, [r1, #0x4]
    str r0, [r1, #0]
    mov r0, #0x1
    mov r1, #0x10
    bl native_fn_02203908
    ldr r3, =0x04001008
    mov r0, #0x3
    ldrh r2, [r3, #0]
    mov r1, #0x3
    bic r2, r0
    orr r2, r1
    strh r2, [r3, #0]
    ldrh r2, [r3, #0x2]
    bic r2, r0
    orr r2, r1
    strh r2, [r3, #0x2]
    ldr r3, =0x0400000a
    ldrh r2, [r3, #0]
    bic r2, r0
    orr r2, r1
    strh r2, [r3, #0]
    ldrh r2, [r3, #0x2]
    bic r2, r0
    add r0, r2, #0x0
    orr r0, r1
    strh r0, [r3, #0x2]
    add sp, #0x18
    pop {r3, pc}
}
