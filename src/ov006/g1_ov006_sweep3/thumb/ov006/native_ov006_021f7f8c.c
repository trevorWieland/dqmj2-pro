/* ov006 row 0x021f7f8c: 196 bytes.
 *
 * What it does: 77 instructions; 7 call(s) to 0x021f27d4, 0x021f2798, 0x02202a80, +4 more; loops (back edge at +0x16); returns through pop {r4, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xa8 -> native_data_0220b5eb (image word 0x0220b5eb)
 *   pool +0xac -> native_data_0220b5d5 (image word 0x0220b5d5)
 *   pool +0xb0 -> native_data_0220dd60 (image word 0x0220dd60)
 *   pool +0xb4 -> constant 0x02004d98 (image word 0x02004d98)
 *   pool +0xb8 -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   pool +0xbc -> constant 0x04001008 (image word 0x04001008)
 *   pool +0xc0 -> constant 0x04000008 (image word 0x04000008)
 *   back edge +0x16 -> +0x0c
 *   back edge +0x28 -> +0x1e
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f7f8c; the literal pool and
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

extern u8 native_data_0220b5eb[];
extern u8 native_data_0220b5d5[];
extern u8 native_data_0220dd60[];
extern void native_fn_021f27d4(void);
extern void native_fn_021f2798(void);
extern void native_fn_02202a80(void);
extern void native_fn_021fe49c(void);
extern void native_fn_021fe4fc(void);


asm u32 native_ov006_021f7f8c (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x30
    add r2, sp, #0x14
    ldr r3, =native_data_0220b5eb
    add r2, #0x2
    mov r1, #0x19
ov006_021f7f8c_Lc:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021f7f8c_Lc
    ldr r3, =native_data_0220b5d5
    add r2, sp, #0x0
    mov r1, #0x16
ov006_021f7f8c_L1e:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021f7f8c_L1e
    ldr r0, =native_data_0220dd60
    ldr r1, =0x02004d98
    bl native_fn_021f27d4
    add r0, sp, #0x14
    add r0, #0x2
    bl native_fn_021f2798
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c0d8
    ldr r2, [r1, #0x4]
    str r0, [r2, #0x4]
    ldr r0, [r1, #0x4]
    ldr r0, [r0, #0x4]
    bl native_fn_021fe49c
    bl native_fn_021fe4fc
    add r0, sp, #0x0
    bl native_fn_021f2798
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c0d8
    ldr r3, =0x04001008
    ldr r1, [r1, #0x4]
    mov r2, #0x3
    str r0, [r1, #0x8]
    ldrh r0, [r3, #0]
    mov r1, #0x3
    bic r0, r2
    orr r0, r1
    strh r0, [r3, #0]
    ldrh r0, [r3, #0x2]
    bic r0, r2
    orr r0, r1
    strh r0, [r3, #0x2]
    ldr r0, =0x04000008
    ldrh r3, [r0, #0]
    bic r3, r2
    orr r3, r1
    strh r3, [r0, #0]
    ldrh r4, [r0, #0x2]
    mov r3, #0x2
    bic r4, r2
    orr r4, r3
    strh r4, [r0, #0x2]
    ldrh r4, [r0, #0x4]
    bic r4, r2
    orr r1, r4
    strh r1, [r0, #0x4]
    ldrh r1, [r0, #0x6]
    bic r1, r2
    orr r1, r3
    strh r1, [r0, #0x6]
    add sp, #0x30
    pop {r4, pc}
    mov r8, r8
}
