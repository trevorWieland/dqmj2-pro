/* ov006 row 0x021fa2b4: 324 bytes.
 *
 * What it does: 115 instructions; 13 call(s) to 0x021f27d4, 0x021f27d4, 0x021f27d4, +10 more; loops (back edge at +0x16); returns through pop {r3, r4, pc}; 17 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x100 -> native_data_0220b77b (image word 0x0220b77b)
 *   pool +0x104 -> native_data_0220b750 (image word 0x0220b750)
 *   pool +0x108 -> native_data_0220b765 (image word 0x0220b765)
 *   pool +0x10c -> constant 0x0400000c (image word 0x0400000c)
 *   pool +0x110 -> constant 0x00000e18 (image word 0x00000e18)
 *   pool +0x114 -> native_data_0220de78 (image word 0x0220de78)
 *   pool +0x118 -> constant 0x0200494c (image word 0x0200494c)
 *   pool +0x11c -> native_data_0220de8c (image word 0x0220de8c)
 *   pool +0x120 -> constant 0x02005098 (image word 0x02005098)
 *   pool +0x124 -> native_data_0220dea4 (image word 0x0220dea4)
 *   pool +0x128 -> constant 0x02004fd8 (image word 0x02004fd8)
 *   pool +0x12c -> constant 0x020048a0 (image word 0x020048a0)
 *   pool +0x130 -> native_data_0220debc (image word 0x0220debc)
 *   pool +0x134 -> constant 0x02004d98 (image word 0x02004d98)
 *   pool +0x138 -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   pool +0x13c -> constant 0x04001008 (image word 0x04001008)
 *   pool +0x140 -> constant 0x04000008 (image word 0x04000008)
 *   back edge +0x16 -> +0x0c
 *   back edge +0x2a -> +0x20
 *   back edge +0x3c -> +0x32
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fa2b4; the literal pool and
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

extern u8 native_data_0220b77b[];
extern u8 native_data_0220b750[];
extern u8 native_data_0220b765[];
extern u8 native_data_0220de78[];
extern void native_fn_021f27d4(void);
extern u8 native_data_0220de8c[];
extern u8 native_data_0220dea4[];
extern u8 native_data_0220debc[];
extern void native_fn_021f2798(void);
extern void native_fn_02202a80(void);
extern void native_fn_021fe49c(void);
extern void native_fn_021fe4fc(void);


asm u32 native_ov006_021fa2b4 (register u32 a0)
{
    push {r3, r4, lr}
    sub sp, #0x44
    add r2, sp, #0x28
    ldr r3, =native_data_0220b77b
    add r2, #0x3
    mov r1, #0x17
ov006_021fa2b4_Lc:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021fa2b4_Lc
    add r2, sp, #0x14
    ldr r3, =native_data_0220b750
    add r2, #0x2
    mov r1, #0x15
ov006_021fa2b4_L20:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021fa2b4_L20
    ldr r3, =native_data_0220b765
    add r2, sp, #0x0
    mov r1, #0x16
ov006_021fa2b4_L32:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021fa2b4_L32
    ldr r2, =0x0400000c
    mov r0, #0x43
    ldrh r1, [r2, #0]
    and r1, r0
    ldr r0, =0x00000e18
    orr r0, r1
    strh r0, [r2, #0]
    ldr r0, =native_data_0220de78
    ldr r1, =0x0200494c
    bl native_fn_021f27d4
    ldr r0, =native_data_0220de8c
    ldr r1, =0x02005098
    bl native_fn_021f27d4
    ldr r0, =native_data_0220dea4
    ldr r1, =0x02004fd8
    bl native_fn_021f27d4
    add r0, sp, #0x14
    ldr r1, =0x020048a0
    add r0, #0x2
    bl native_fn_021f27d4
    ldr r0, =native_data_0220debc
    ldr r1, =0x02004d98
    bl native_fn_021f27d4
    add r0, sp, #0x28
    add r0, #0x3
    bl native_fn_021f2798
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c0ec
    ldr r2, [r1, #0x8]
    str r0, [r2, #0x8]
    ldr r0, [r1, #0x8]
    ldr r0, [r0, #0x8]
    bl native_fn_021fe49c
    bl native_fn_021fe4fc
    add r0, sp, #0x14
    add r0, #0x2
    bl native_fn_021f2798
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c0ec
    ldr r1, [r1, #0x8]
    str r0, [r1, #0xc]
    add r0, sp, #0x0
    bl native_fn_021f2798
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c0ec
    mov r2, #0x3
    ldr r1, [r1, #0x8]
    mov r3, #0x3
    str r0, [r1, #0x10]
    ldr r1, =0x04001008
    ldrh r0, [r1, #0]
    bic r0, r2
    orr r0, r3
    strh r0, [r1, #0]
    ldrh r0, [r1, #0x2]
    bic r0, r2
    orr r0, r3
    strh r0, [r1, #0x2]
    ldr r0, =0x04000008
    ldrh r1, [r0, #0]
    bic r1, r2
    orr r1, r3
    strh r1, [r0, #0]
    ldrh r4, [r0, #0x2]
    mov r1, #0x2
    bic r4, r2
    orr r4, r1
    strh r4, [r0, #0x2]
    ldrh r4, [r0, #0x4]
    bic r4, r2
    orr r3, r4
    strh r3, [r0, #0x4]
    ldrh r3, [r0, #0x6]
    bic r3, r2
    orr r1, r3
    strh r1, [r0, #0x6]
    add sp, #0x44
    pop {r3, r4, pc}
}
