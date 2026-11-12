/* ov006 row 0x021f65d4: 260 bytes.
 *
 * What it does: 101 instructions; 12 call(s) to 0x021f27d4, 0x021f27d4, 0x021f2798, +9 more; loops (back edge at +0x16); returns through pop {r3, r4, r5, r6, r7, pc}; 9 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xe0 -> native_data_0220b574 (image word 0x0220b574)
 *   pool +0xe4 -> native_data_0220b58a (image word 0x0220b58a)
 *   pool +0xe8 -> native_data_0220dc60 (image word 0x0220dc60)
 *   pool +0xec -> constant 0x02004fd8 (image word 0x02004fd8)
 *   pool +0xf0 -> native_data_0220dc78 (image word 0x0220dc78)
 *   pool +0xf4 -> constant 0x02004cd8 (image word 0x02004cd8)
 *   pool +0xf8 -> constant 0x0221c0a8 (image word 0x0221c0a8)
 *   pool +0xfc -> constant 0x04001008 (image word 0x04001008)
 *   pool +0x100 -> constant 0x0400000a (image word 0x0400000a)
 *   back edge +0x16 -> +0x0c
 *   back edge +0x28 -> +0x1e
 *   branch +0x72 -> +0x94
 *   back edge +0x92 -> +0x80
 *   test +0x90 cmp r6, #0x2
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f65d4; the literal pool and
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

extern u8 native_data_0220b574[];
extern u8 native_data_0220b58a[];
extern u8 native_data_0220dc60[];
extern void native_fn_021f27d4(void);
extern u8 native_data_0220dc78[];
extern void native_fn_021f2798(void);
extern void native_fn_02202a80(void);
extern void native_fn_020a4660(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02007308(void);
extern void native_fn_020048a0(void);
extern void native_fn_02202b24(void);


asm u32 native_ov006_021f65d4 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x48
    add r2, sp, #0x2c
    ldr r3, =native_data_0220b574
    add r2, #0x3
    mov r1, #0x16
ov006_021f65d4_Lc:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021f65d4_Lc
    ldr r3, =native_data_0220b58a
    add r2, sp, #0x18
    mov r1, #0x17
ov006_021f65d4_L1e:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021f65d4_L1e
    ldr r0, =native_data_0220dc60
    ldr r1, =0x02004fd8
    bl native_fn_021f27d4
    ldr r0, =native_data_0220dc78
    ldr r1, =0x02004cd8
    bl native_fn_021f27d4
    add r0, sp, #0x18
    bl native_fn_021f2798
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c0a8
    str r0, [r1, #0x4]
    add r0, sp, #0x2c
    add r0, #0x3
    bl native_fn_021f2798
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    str r0, [sp]
    add r0, sp, #0x4
    bl native_fn_020a4660
    ldr r3, [sp, #0x4]
    mov r0, #0x0
    ldr r2, [sp, #0x8]
    mov r1, #0x0
    eor r1, r2
    eor r0, r3
    orr r0, r1
    bne ov006_021f65d4_L94
    ldr r4, [sp]
    ldr r5, [sp]
    add r4, #0xc0
    add r5, #0x40
    mov r6, #0x0
    mov r7, #0x20
ov006_021f65d4_L80:
    add r0, r4, #0x0
    add r1, r5, #0x0
    add r2, r7, #0x0
    blx native_fn_02008e0c
    add r6, r6, #0x1
    add r4, #0x20
    add r5, #0x20
    cmp r6, #0x2
    blt ov006_021f65d4_L80
ov006_021f65d4_L94:
    mov r1, #0x2
    ldr r0, [sp]
    lsl r1, r1, #0x8
    blx native_fn_02007308
    mov r2, #0x2
    ldr r0, [sp]
    mov r1, #0x0
    lsl r2, r2, #0x8
    blx native_fn_020048a0
    ldr r0, [sp]
    bl native_fn_02202b24
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
    add sp, #0x48
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
