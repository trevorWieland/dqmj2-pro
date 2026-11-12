/* ov006 row 0x021f5aa4: 152 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x70 -> native_data_0220b556 (image word 0x0220b556)
 *   pool +0x74 -> native_data_0220db98 (image word 0x0220db98)
 *   pool +0x78 -> constant 0x02004fd8 (image word 0x02004fd8)
 *   pool +0x7c -> native_data_0220dbb0 (image word 0x0220dbb0)
 *   pool +0x80 -> constant 0x020048a0 (image word 0x020048a0)
 *   pool +0x84 -> native_data_0220dbc8 (image word 0x0220dbc8)
 *   pool +0x88 -> constant 0x02004cd8 (image word 0x02004cd8)
 *   pool +0x8c -> constant 0x0221c09c (image word 0x0221c09c)
 *   pool +0x90 -> constant 0x04001008 (image word 0x04001008)
 *   pool +0x94 -> constant 0x0400000a (image word 0x0400000a)
 *   back edge +0x14 -> +0x0a
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5aa4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b556[];
extern u8 native_data_0220db98[];
extern void native_fn_021f27d4(void);
extern u8 native_data_0220dbb0[];
extern u8 native_data_0220dbc8[];
extern void native_fn_021f2798(void);
extern void native_fn_02202a80(void);


asm u32 native_ov006_021f5aa4 (register u32 a0)
{
    push {r3, lr}
    sub sp, #0x18
    ldr r3, =native_data_0220b556
    add r2, sp, #0x0
    mov r1, #0x16
ov006_021f5aa4_La:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021f5aa4_La
    ldr r0, =native_data_0220db98
    ldr r1, =0x02004fd8
    bl native_fn_021f27d4
    ldr r0, =native_data_0220dbb0
    ldr r1, =0x020048a0
    bl native_fn_021f27d4
    ldr r0, =native_data_0220dbc8
    ldr r1, =0x02004cd8
    bl native_fn_021f27d4
    add r0, sp, #0x0
    bl native_fn_021f2798
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c09c
    ldr r3, =0x04001008
    str r0, [r1, #0x4]
    ldrh r2, [r3, #0]
    mov r0, #0x3
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
    mov r8, r8
}
